"""
LLM abstraction for booktest.

This module provides an abstract LLM interface and implementations for
different LLM providers. The default LLM can be configured globally.
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Optional, Any, List, Callable


class Llm(ABC):
    """
    Abstract base class for LLM providers.

    Subclasses must implement the prompt() method to interact with their
    specific LLM backend.
    """

    @abstractmethod
    def prompt(self, request: str, max_completion_tokens: int = 2048) -> str:
        """
        Send a prompt to the LLM and get a response.

        Args:
            request: The prompt text to send to the LLM
            max_completion_tokens: Maximum tokens for the LLM's response

        Returns:
            The LLM's response as a string
        """
        pass

    def prompt_json(
        self,
        request: str,
        required_fields: List[str] = None,
        validator: Callable[[dict], bool] = None,
        max_retries: int = 3,
        max_completion_tokens: int = 4 * 1024
    ) -> dict:
        """
        Send a prompt and parse the response as JSON with validation and retry.

        Note: Retries use the same request to preserve HTTP snapshot compatibility.
        The request is not modified between retries.

        Args:
            request: The prompt text (should instruct LLM to respond with JSON)
            required_fields: List of field names that must be present in response
            validator: Optional function to validate parsed JSON, returns True if valid
            max_retries: Number of retry attempts on parse/validation failure
            max_completion_tokens: Maximum tokens for the LLM's response

        Returns:
            Parsed JSON as a dictionary

        Raises:
            ValueError: If JSON parsing or validation fails after all retries
        """
        last_error = None
        last_response = None

        for attempt in range(max_retries):
            try:
                response = self.prompt(request, max_completion_tokens)
                last_response = response

                # Try to extract JSON from response (LLM might add extra text)
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    response = response[json_start:json_end]

                parsed = json.loads(response)

                # Validate required fields
                if required_fields:
                    missing = [f for f in required_fields if f not in parsed]
                    if missing:
                        raise ValueError(f"Missing required fields: {missing}")

                # Run custom validator
                if validator and not validator(parsed):
                    raise ValueError("Custom validation failed")

                return parsed

            except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
                last_error = e
                # Don't modify request - retries use same request for snapshot compatibility

        raise ValueError(
            f"Failed to get valid JSON after {max_retries} attempts. "
            f"Last error: {last_error}. Last response: {last_response[:500] if last_response else 'None'}"
        )


class GptLlm(Llm):
    """
    GPT/Azure OpenAI implementation of the LLM interface.

    Requires environment variables:
    - OPENAI_API_KEY: API key for OpenAI/Azure
    - OPENAI_API_BASE: API endpoint (for Azure)
    - OPENAI_MODEL: Model name
    - OPENAI_DEPLOYMENT: Deployment name (for Azure)
    - OPENAI_API_VERSION: API version (for Azure)
    - OPENAI_COMPLETION_MAX_TOKENS: Max tokens (default: 2048)
    """

    def __init__(self, client=None):
        """
        Initialize GPT LLM.

        Args:
            client: Optional OpenAI client. If None, creates AzureOpenAI client
                   from environment variables.
        """
        if client is None:
            from openai import AzureOpenAI
            self.client = AzureOpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                azure_endpoint=os.getenv("OPENAI_API_BASE"),
                azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
                api_version=os.getenv("OPENAI_API_VERSION"),
                max_retries=5)
        else:
            self.client = client

    def prompt(self, request: str, max_completion_tokens: int = 2048) -> str:
        """
        Send a prompt to GPT and get a response.

        Args:
            request: The prompt text to send to GPT

        Returns:
            GPT's response as a string
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": request}
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=max_completion_tokens,
            seed=0)

        return response.choices[0].message.content


class ClaudeLlm(Llm):
    """
    Anthropic Claude implementation of the LLM interface.

    Requires:
    - anthropic package: pip install anthropic
    - ANTHROPIC_API_KEY environment variable

    Optional environment variables:
    - ANTHROPIC_MODEL: Model name (default: claude-sonnet-4-20250514)
    """

    def __init__(self, client=None):
        """
        Initialize Claude LLM.

        Args:
            client: Optional Anthropic client. If None, creates client
                   from ANTHROPIC_API_KEY environment variable.
        """
        if client is None:
            from anthropic import Anthropic
            self.client = Anthropic()  # Uses ANTHROPIC_API_KEY automatically
        else:
            self.client = client

    def prompt(self, request: str, max_completion_tokens: int = 2048) -> str:
        """
        Send a prompt to Claude and get a response.

        Args:
            request: The prompt text to send to Claude
            max_completion_tokens: Maximum tokens for Claude's response

        Returns:
            Claude's response as a string
        """
        message = self.client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            max_tokens=max_completion_tokens,
            messages=[{"role": "user", "content": request}]
        )
        return message.content[0].text


class OllamaLlm(Llm):
    """
    Ollama implementation of the LLM interface for local LLMs.

    Requires:
    - Ollama running locally (default: http://localhost:11434)

    Optional environment variables:
    - OLLAMA_HOST: Ollama server URL (default: http://localhost:11434)
    - OLLAMA_MODEL: Model name (default: llama3.2)
    """

    def __init__(self, host: str = None, model: str = None):
        """
        Initialize Ollama LLM.

        Args:
            host: Ollama server URL. If None, uses OLLAMA_HOST env var
                  or defaults to http://localhost:11434.
            model: Model name. If None, uses OLLAMA_MODEL env var
                   or defaults to llama3.2.
        """
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")

    def prompt(self, request: str, max_completion_tokens: int = 2048) -> str:
        """
        Send a prompt to Ollama and get a response.

        Args:
            request: The prompt text to send to Ollama
            max_completion_tokens: Maximum tokens for Ollama's response

        Returns:
            Ollama's response as a string
        """
        import requests
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": request,
                "stream": False,
                "options": {"num_predict": max_completion_tokens}
            }
        )
        response.raise_for_status()
        return response.json()["response"]


# Global LLM configuration
_llm_factory: Optional[Callable[[], Llm]] = None
_default_llm: Optional[Llm] = None


def _auto_detect_llm() -> Llm:
    """Create LLM based on environment variables."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return ClaudeLlm()
    elif os.getenv("OLLAMA_HOST") or os.getenv("OLLAMA_MODEL"):
        return OllamaLlm()
    else:
        return GptLlm()


def get_llm() -> Llm:
    """
    Get the default LLM instance.

    The instance is cached for efficiency. To reset the cache (e.g., after
    environment variables change), call set_llm(None).

    Auto-detects the LLM provider based on environment variables:
    1. ANTHROPIC_API_KEY -> ClaudeLlm
    2. OLLAMA_HOST or OLLAMA_MODEL -> OllamaLlm
    3. Otherwise -> GptLlm (Azure OpenAI)

    You can override with set_llm_factory() to use a specific LLM class.

    Returns:
        The cached LLM instance
    """
    global _default_llm, _llm_factory
    if _default_llm is None:
        if _llm_factory is not None:
            _default_llm = _llm_factory()
        else:
            _default_llm = _auto_detect_llm()
    return _default_llm


def set_llm(llm: Optional[Llm]):
    """
    Set a specific LLM instance to use globally.

    Args:
        llm: The LLM instance to use, or None to reset cache
    """
    global _default_llm
    _default_llm = llm


def set_llm_factory(factory: Optional[Callable[[], Llm]]):
    """
    Set which LLM class to use without creating an instance immediately.

    The factory is called once when get_llm() is first invoked (after any
    cache reset). The created instance is then cached.

    Args:
        factory: A callable that returns an Llm (e.g., bt.GptLlm, bt.ClaudeLlm),
                 or None to reset to auto-detection

    Example:
        # Use GPT regardless of environment
        bt.set_llm_factory(bt.GptLlm)

        # Use Claude
        bt.set_llm_factory(bt.ClaudeLlm)

        # Custom configuration
        bt.set_llm_factory(lambda: bt.OllamaLlm(model="codellama"))
    """
    global _llm_factory, _default_llm
    _llm_factory = factory
    _default_llm = None  # Reset cache so factory is used on next get_llm()


class LlmSentry:
    """
    Context manager for temporarily switching the default LLM.

    Example:
        with LlmSentry(my_custom_llm):
            # Code here uses my_custom_llm as default
            r = t.start_review()
            r.reviewln("Is output correct?", "Yes", "No")
        # Original LLM is restored
    """

    def __init__(self, llm: Llm):
        """
        Initialize the sentry with a temporary LLM.

        Args:
            llm: The LLM to use temporarily
        """
        self.llm = llm
        self.previous_llm = None

    def __enter__(self):
        """Enter the context and save the previous LLM."""
        global _default_llm
        self.previous_llm = _default_llm
        _default_llm = self.llm
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and restore the previous LLM."""
        global _default_llm
        _default_llm = self.previous_llm
        return False


def use_llm(llm: Llm):
    """
    Decorator to set the LLM for a specific test function.

    This decorator temporarily sets the default LLM for the duration of the test,
    then restores the previous default when the test completes. Works with both
    sync and async test functions.

    Args:
        llm: The LLM instance to use for this test

    Example:
        @bt.use_llm(my_custom_llm)
        def test_agent(t: bt.TestCaseRun):
            r = t.start_review()
            r.reviewln("Is output correct?", "Yes", "No")

        @bt.use_llm(my_custom_llm)
        async def test_async_agent(t: bt.TestCaseRun):
            r = t.start_review()
            r.reviewln("Is output correct?", "Yes", "No")
    """
    def decorator(func):
        # Check if function is async
        import asyncio

        if asyncio.iscoroutinefunction(func):
            # Async wrapper
            async def async_wrapper(*args, **kwargs):
                with LlmSentry(llm):
                    return await func(*args, **kwargs)

            # Preserve function metadata
            async_wrapper.__name__ = func.__name__
            async_wrapper.__doc__ = func.__doc__
            async_wrapper.__module__ = func.__module__
            async_wrapper.__qualname__ = func.__qualname__

            return async_wrapper
        else:
            # Sync wrapper
            def sync_wrapper(*args, **kwargs):
                with LlmSentry(llm):
                    return func(*args, **kwargs)

            # Preserve function metadata
            sync_wrapper.__name__ = func.__name__
            sync_wrapper.__doc__ = func.__doc__
            sync_wrapper.__module__ = func.__module__
            sync_wrapper.__qualname__ = func.__qualname__

            return sync_wrapper

    return decorator
