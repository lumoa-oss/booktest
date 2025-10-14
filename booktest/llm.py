"""
LLM abstraction for booktest.

This module provides an abstract LLM interface and implementations for
different LLM providers. The default LLM can be configured globally.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional


class Llm(ABC):
    """
    Abstract base class for LLM providers.

    Subclasses must implement the prompt() method to interact with their
    specific LLM backend.
    """

    @abstractmethod
    def prompt(self, request: str) -> str:
        """
        Send a prompt to the LLM and get a response.

        Args:
            request: The prompt text to send to the LLM

        Returns:
            The LLM's response as a string
        """
        pass


class GptLlm(Llm):
    """
    GPT/Azure OpenAI implementation of the LLM interface.

    Requires environment variables:
    - OPENAI_API_KEY: API key for OpenAI/Azure
    - OPENAI_API_BASE: API endpoint (for Azure)
    - OPENAI_MODEL: Model name
    - OPENAI_DEPLOYMENT: Deployment name (for Azure)
    - OPENAI_API_VERSION: API version (for Azure)
    - OPENAI_COMPLETION_MAX_TOKENS: Max tokens (default: 1024)
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

    def prompt(self, request: str) -> str:
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
            max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", "1024")),
            seed=0)

        return response.choices[0].message.content


# Global default LLM instance
_default_llm: Optional[Llm] = None


def get_llm() -> Llm:
    """
    Get the default LLM instance.

    Returns the global default LLM, creating a GptLlm instance if none is set.

    Returns:
        The default LLM instance
    """
    global _default_llm
    if _default_llm is None:
        _default_llm = GptLlm()
    return _default_llm


def set_llm(llm: Llm):
    """
    Set the global default LLM instance.

    Args:
        llm: The LLM instance to use as default
    """
    global _default_llm
    _default_llm = llm


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
