"""
LLM integration tests for booktest review functionality.

These tests verify that different LLM backends work correctly with
booktest's review system. Tests use static, predictable input to
establish ground truth.

To run with specific backend:
    OLLAMA_MODEL=llama3.2 ./do test llm/test_llm

Environment variables:
    - OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_CONTEXT_SIZE for Ollama
    - OPENAI_* for GPT/Azure
    - ANTHROPIC_API_KEY for Claude
"""
import booktest as bt
import os


def snapshot_ollama():
    """
    Snapshot decorator for Ollama API calls.

    Captures HTTP requests to Ollama for test reproducibility.
    """
    return bt.combine_decorators(
        bt.snapshot_requests(lose_request_details=False),
        bt.snapshot_env(
            "BOOKTEST_LLM",
            "OLLAMA_HOST",
            "OLLAMA_MODEL",
            "OLLAMA_CONTEXT_SIZE"
        )
    )


def snapshot_gpt():
    """Snapshot decorator for GPT/OpenAI API calls."""
    return bt.combine_decorators(
        bt.snapshot_httpx(lose_request_details=False),
        bt.mock_missing_env({"OPENAI_API_KEY": "mock-key"}),
        bt.snapshot_env(
            "BOOKTEST_LLM",
            "OPENAI_API_BASE",
            "OPENAI_MODEL",
            "OPENAI_DEPLOYMENT",
            "OPENAI_API_VERSION",
            "OPENAI_COMPLETION_MAX_TOKENS"
        )
    )


def snapshot_claude():
    """Snapshot decorator for Anthropic Claude API calls."""
    return bt.combine_decorators(
        bt.snapshot_httpx(lose_request_details=False),
        bt.mock_missing_env({"ANTHROPIC_API_KEY": "mock-key"}),
        bt.snapshot_env(
            "BOOKTEST_LLM",
            "ANTHROPIC_MODEL"
        )
    )


# Static test content with objectively verifiable answers
REVIEW_CONTENT = """
# Code Review

## Function Definition

```python
def add_numbers(a, b):
    # Sum two numbers
    return a + b
```

## Test Results

```
>>> add_numbers(2, 3)
5
>>> add_numbers(-1, 1)
0
>>> add_numbers(0, 0)
0
```

All tests passed.
"""

# Ground truth for the static content above
GROUND_TRUTH = {
    "language": "Python",
    "has_docstring": "No",  # Only has a comment, not a docstring
    "tests_pass": "Yes",
    "function_name": "add_numbers",
}


def _run_review_test(t: bt.TestCaseRun, llm: bt.Llm):
    """
    Core review test logic - runs with any LLM backend.

    Uses static content with known ground truth to verify
    that the LLM can correctly answer basic review questions.
    """
    r = t.start_review()

    r.h1("test content:")
    r.iln(REVIEW_CONTENT)

    r.start_review()

    # Test basic comprehension with clear ground truth
    r.reviewln(
        "What programming language is the code written in?",
        GROUND_TRUTH["language"],
        "JavaScript", "Java", "C++"
    )

    r.reviewln(
        "Does the function have a docstring (triple-quoted string)?",
        GROUND_TRUTH["has_docstring"],
        "Yes"
    )

    r.reviewln(
        "Do all the tests pass according to the output?",
        GROUND_TRUTH["tests_pass"],
        "No", "Some fail"
    )


@snapshot_ollama()
def test_ollama_review(t: bt.TestCaseRun):
    """Test review functionality with Ollama backend."""
    llm = bt.OllamaLlm()

    t.h1("Configuration")
    t.iln(f" * model: {llm.model}")
    t.iln(f" * context_size: {llm.context_size}")

    with bt.LlmSentry(llm):
        _run_review_test(t, llm)


# GPT and Claude tests - uncomment when running with appropriate API keys
#
# @snapshot_gpt()
# def test_gpt_review(t: bt.TestCaseRun):
#     """Test review functionality with GPT/Azure backend."""
#     llm = bt.GptLlm()
#     with bt.LlmSentry(llm):
#         _run_review_test(t, llm)
#
# @snapshot_claude()
# def test_claude_review(t: bt.TestCaseRun):
#     """Test review functionality with Claude backend."""
#     llm = bt.ClaudeLlm()
#     with bt.LlmSentry(llm):
#         _run_review_test(t, llm)


# Test for BOOKTEST_LLM selection
def test_booktest_llm_selection(t: bt.TestCaseRun):
    """Verify BOOKTEST_LLM=ollama explicitly selects Ollama."""
    t.h1("BOOKTEST_LLM Selection")

    # Save original
    original_llm = os.environ.get("BOOKTEST_LLM")

    try:
        # Clear any cached LLM
        bt.set_llm(None)

        # Explicitly select Ollama
        os.environ["BOOKTEST_LLM"] = "ollama"

        llm = bt.get_llm()
        t.tln(f" * BOOKTEST_LLM=ollama: {type(llm).__name__}")
        t.key(" * Ollama selected:").assertln(
            isinstance(llm, bt.OllamaLlm))

    finally:
        # Restore original
        bt.set_llm(None)
        if original_llm is not None:
            os.environ["BOOKTEST_LLM"] = original_llm
        elif "BOOKTEST_LLM" in os.environ:
            del os.environ["BOOKTEST_LLM"]


# Test for context size configuration
def test_ollama_context_size(t: bt.TestCaseRun):
    """Verify OLLAMA_CONTEXT_SIZE is read correctly."""
    t.h1("OLLAMA_CONTEXT_SIZE Configuration")

    # Save original
    original = os.environ.get("OLLAMA_CONTEXT_SIZE")

    try:
        # Test default
        if "OLLAMA_CONTEXT_SIZE" in os.environ:
            del os.environ["OLLAMA_CONTEXT_SIZE"]
        llm1 = bt.OllamaLlm()

        t.h2("Default value")
        t.tln(f" * context_size: {llm1.context_size}")
        t.key(" * is 32768:").assertln(llm1.context_size == 32768)

        # Test custom value
        os.environ["OLLAMA_CONTEXT_SIZE"] = "65536"
        llm2 = bt.OllamaLlm()

        t.h2("Custom value (65536)")
        t.tln(f" * context_size: {llm2.context_size}")
        t.key(" * is 65536:").assertln(llm2.context_size == 65536)

    finally:
        # Restore original
        if original is not None:
            os.environ["OLLAMA_CONTEXT_SIZE"] = original
        elif "OLLAMA_CONTEXT_SIZE" in os.environ:
            del os.environ["OLLAMA_CONTEXT_SIZE"]


# Test for basic LLM prompt (no review, just raw prompt)
@snapshot_ollama()
def test_ollama_basic_prompt(t: bt.TestCaseRun):
    """Test basic prompt/response with Ollama."""
    llm = bt.OllamaLlm()

    t.h1("Configuration")
    t.iln(f" * model: {llm.model}")
    t.iln(f" * context_size: {llm.context_size}")

    # Simple factual question with clear answer
    response = llm.prompt(
        "What is 2 + 2? Answer with just the number.",
        max_completion_tokens=32
    )

    t.h1("Response")
    t.iln(f" * response: {response.strip()}")

    t.h1("Validation")
    t.key(" * contains '4':").assertln("4" in response)


@snapshot_ollama()
def test_ollama_json_response(t: bt.TestCaseRun):
    """Test JSON parsing with Ollama - handles verbose models."""
    llm = bt.OllamaLlm()

    t.h1("Configuration")
    t.iln(f" * model: {llm.model}")

    # Request JSON response
    result = llm.prompt_json(
        """Answer this question as JSON:
What is the capital of France?

Respond with: {"answer": "the capital city", "country": "France"}""",
        required_fields=["answer", "country"],
        max_retries=3
    )

    t.h1("Parsed Result")
    t.tln(f" * answer: {result.get('answer')}")
    t.tln(f" * country: {result.get('country')}")

    t.h1("Validation")
    answer = result.get("answer", "").lower()
    t.key(" * answer contains 'paris':").assertln("paris" in answer)
