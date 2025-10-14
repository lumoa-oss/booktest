"""
LLM-assisted review functionality for booktest.

This module provides LlmReview class for using LLM models to automatically
review test outputs and validate results against expectations.
"""

import os
from typing import TYPE_CHECKING, Optional

from booktest.output import OutputWriter
from booktest.llm import Llm, get_llm

if TYPE_CHECKING:
    from booktest.testcaserun import TestCaseRun


class LlmReview(OutputWriter):
    """
    LLM-assisted review for test outputs.

    LlmReview accumulates test output in a buffer and uses an LLM to answer
    questions about the output, enabling automated validation of complex
    test results that would be difficult to assert programmatically.

    Example usage:
        def test_llm_output(t: bt.TestCaseRun):
            r = t.start_review()

            r.h1("Generated Code:")
            r.icode(generated_code, "python")

            r.h1("Output:")
            r.iln(program_output)

            r.start_review()
            r.reviewln("Does the code follow PEP8?", "Yes", "No")
            r.reviewln("Are comments helpful?", "Yes", "No")
            r.assertln("Does code run without errors?", no_errors)

    The LLM used can be configured:
    - Pass llm parameter to __init__()
    - Use set_llm() to change the global default
    - Use LlmSentry context manager for temporary changes

    For GPT/Azure OpenAI (default), requires environment variables:
        - OPENAI_API_KEY: API key for OpenAI/Azure
        - OPENAI_API_BASE: API endpoint (for Azure)
        - OPENAI_MODEL: Model name
        - OPENAI_DEPLOYMENT: Deployment name (for Azure)
        - OPENAI_API_VERSION: API version (for Azure)
        - OPENAI_COMPLETION_MAX_TOKENS: Max tokens (default: 1024)
    """

    def __init__(self, test_case_run: 'TestCaseRun', llm: Optional[Llm] = None):
        """
        Initialize LLM review.

        Args:
            test_case_run: Parent TestCaseRun instance
            llm: Optional LLM instance. If None, uses get_llm() default.
        """
        self.t = test_case_run
        self.buffer = ""
        self.llm = llm if llm is not None else get_llm()

    # ========== Primitive methods implementation ==========

    def h(self, level: int, title: str):
        """Write a header at the specified level (primitive method)."""
        label = "#" * level + " " + title
        self.buffer += f"\n{label}\n"
        self.t.h(level, title)
        return self

    def t(self, text: str):
        """Write tested text inline (primitive method)."""
        self.buffer += text
        self.t.t(text)
        return self

    def i(self, text: str):
        """Write info text inline (primitive method)."""
        self.buffer += text
        self.t.i(text)
        return self

    def diff(self):
        """Mark the test as different (primitive method)."""
        self.t.diff()
        return self

    def fail(self):
        """Mark the test as failed (primitive method)."""
        self.t.fail()
        return self

    def start_review(self):
        """Start the review section."""
        self.t.h1("review:")
        return self

    def reviewln(self, prompt: str, expected: str, *fail_options: str):
        """
        Use LLM to review accumulated output and validate against expected answer.

        Args:
            prompt: Question to ask about the output (e.g., "Does code follow PEP8?")
            expected: Expected answer (e.g., "Yes")
            *fail_options: Alternative answers that indicate failure (e.g., "No", "Partial")

        The LLM is asked to choose one of the options based on the accumulated buffer
        content. The test asserts that the LLM's answer matches the expected answer.

        Example:
            r.reviewln("Is code well documented?", "Yes", "No", "Partial")
        """
        system_prompt = '''You are an expert reviewer for test results. You are given question in format:

Question? (optionA|optionB|optionC|...)

reviewed material

Respond only with the exact option that best answers the question! Do not produce any
other text or explanation! Only respond with one of the options given in the parentheses.'''

        options = [expected] + list(fail_options)

        request = f"{system_prompt}\n\n{prompt} ({'|'.join(options)})\n\n{self.buffer}"
        result = self.llm.prompt(request)

        self.t.anchor(f" * {prompt} ").i(result).i(" - ").assertln(result == expected)
        return self

    def ireviewln(self, prompt: str, expected: str, *fail_options: str) -> str:
        """
        Use LLM to review accumulated output WITHOUT failing the test.

        Returns the LLM's answer for later evaluation. Unlike reviewln(), this does
        not assert - it just records the answer as info output.

        Args:
            prompt: Question to ask about the output
            expected: Expected answer (for display/context)
            *fail_options: Alternative answers (for display/context)

        Returns:
            The LLM's response

        Example:
            result = r.ireviewln("Is code well documented?", "Yes", "No")
            # Test continues regardless of result
        """
        system_prompt = '''You are an expert reviewer for test results. You are given question in format:

Question? (optionA|optionB|optionC|...)

reviewed material

Respond only with the exact option that best answers the question! Do not produce any
other text or explanation! Only respond with one of the options given in the parentheses.'''

        options = [expected] + list(fail_options)

        request = f"{system_prompt}\n\n{prompt} ({'|'.join(options)})\n\n{self.buffer}"
        result = self.llm.prompt(request)

        # Just output the result, don't assert
        self.t.anchor(f" * {prompt} ").iln(result)
        return result

    def treviewln(self, prompt: str, expected: str, *fail_options: str) -> str:
        """
        Use LLM to review accumulated output and snapshot the result (tested output).

        Like ireviewln() but writes to tested output (tln) instead of info output (iln).
        Still does not fail - just records for later evaluation.

        Args:
            prompt: Question to ask about the output
            expected: Expected answer (for display/context)
            *fail_options: Alternative answers (for display/context)

        Returns:
            The LLM's response

        Example:
            result = r.treviewln("Is code well documented?", "Yes", "No")
            # Test continues regardless of result
        """
        system_prompt = '''You are an expert reviewer for test results. You are given question in format:

Question? (optionA|optionB|optionC|...)

reviewed material

Respond only with the exact option that best answers the question! Do not produce any
other text or explanation! Only respond with one of the options given in the parentheses.'''

        options = [expected] + list(fail_options)

        request = f"{system_prompt}\n\n{prompt} ({'|'.join(options)})\n\n{self.buffer}"
        result = self.llm.prompt(request)

        # Write to tested output so it's compared against snapshot
        self.t.anchor(f" * {prompt} ").tln(result)
        return result

    def assertln(self, title: str, condition: bool):
        """
        Assert a condition with a descriptive title.

        Args:
            title: Description of what is being asserted
            condition: Boolean condition to assert

        Example:
            r.assertln("Code runs without errors", exception is None)
        """
        self.t.anchor(f" * {title} ").assertln(condition)
        return self


# Backwards compatibility alias
GptReview = LlmReview
