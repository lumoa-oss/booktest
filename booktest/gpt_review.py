"""
GPT-assisted review functionality for booktest.

This module provides GptReview class for using GPT models to automatically
review test outputs and validate results against expectations.
"""

import os
from typing import TYPE_CHECKING, Optional, List

from booktest.output import OutputWriter

if TYPE_CHECKING:
    from booktest.testcaserun import TestCaseRun


class GptReview(OutputWriter):
    """
    GPT-assisted review for test outputs.

    GptReview accumulates test output in a buffer and uses GPT to answer
    questions about the output, enabling automated validation of complex
    test results that would be difficult to assert programmatically.

    Example usage:
        def test_gpt_output(t: bt.TestCaseRun):
            r = t.start_review()

            r.h1("Generated Code:")
            r.icode(generated_code, "python")

            r.h1("Output:")
            r.iln(program_output)

            r.start_review()
            r.reviewln("Does the code follow PEP8?", "Yes", "No")
            r.reviewln("Are comments helpful?", "Yes", "No")
            r.assertln("Does code run without errors?", no_errors)

    Requires:
        - openai package
        - Environment variables:
            - OPENAI_API_KEY: API key for OpenAI/Azure
            - OPENAI_API_BASE: API endpoint (for Azure)
            - OPENAI_MODEL: Model name
            - OPENAI_DEPLOYMENT: Deployment name (for Azure)
            - OPENAI_API_VERSION: API version (for Azure)
            - OPENAI_COMPLETION_MAX_TOKENS: Max tokens (default: 1024)
    """

    def __init__(self, test_case_run: 'TestCaseRun', client=None):
        """
        Initialize GPT review.

        Args:
            test_case_run: Parent TestCaseRun instance
            client: Optional OpenAI client. If None, creates AzureOpenAI client
                   from environment variables.
        """
        self.t = test_case_run
        self.buffer = ""

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
        Use GPT to review accumulated output and validate against expected answer.

        Args:
            prompt: Question to ask about the output (e.g., "Does code follow PEP8?")
            expected: Expected answer (e.g., "Yes")
            *fail_options: Alternative answers that indicate failure (e.g., "No", "Partial")

        The GPT is asked to choose one of the options based on the accumulated buffer
        content. The test asserts that the GPT's answer matches the expected answer.

        Example:
            r.reviewln("Is code well documented?", "Yes", "No", "Partial")
        """
        system_prompt = '''You are an expert reviewer for test results. You are given question in format:

Question? (optionA|optionB|optionC|...)

reviewed material

Respond only with the exact option that best answers the question! Do not produce any
other text or explanation! Only respond with one of the options given in the parentheses.'''

        options = [expected] + list(fail_options)

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{prompt} ({'|'.join(options)})\n\n{self.buffer}"}
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", "1024")),
            seed=0)

        result = response.choices[0].message.content

        self.t.anchor(f" * {prompt} ").i(result).i(" - ").assertln(result == expected)
        return self

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
