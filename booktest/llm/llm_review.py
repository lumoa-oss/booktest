"""
LLM-assisted review functionality for booktest.

This module provides LlmReview class for using LLM models to automatically
review test outputs and validate results against expectations.
"""

import os
import json
from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING, Optional, List

from booktest.reporting.output import OutputWriter
from booktest.llm.llm import Llm, get_llm

if TYPE_CHECKING:
    from booktest.core.testcaserun import TestCaseRun


@dataclass
class AIReviewResult:
    """
    Result of an AI-assisted test review.

    The AI analyzes test output differences and provides a recommendation
    on whether to accept or reject the changes.
    """
    category: int  # 1=FAIL, 2=RECOMMEND_FAIL, 3=UNSURE, 4=RECOMMEND_ACCEPT, 5=ACCEPT
    confidence: float  # 0.0 to 1.0
    summary: str  # One-line summary for reports
    rationale: str  # Detailed explanation of the decision
    issues: List[str]  # Specific problems identified (e.g., "line 43: regression")
    suggestions: List[str]  # How to improve the test
    flags_for_human: bool  # Should a human definitely review this

    def category_name(self) -> str:
        """Get human-readable category name."""
        names = {
            1: "FAIL",
            2: "RECOMMEND FAIL",
            3: "UNSURE",
            4: "RECOMMEND ACCEPT",
            5: "ACCEPT"
        }
        return names.get(self.category, "UNKNOWN")

    def should_auto_accept(self) -> bool:
        """
        Should this be automatically accepted without user interaction?

        Returns True only for category 5 (ACCEPT) - the AI is confident enough
        to assign this category, so we trust the decision.
        """
        return self.category == 5

    def should_auto_reject(self) -> bool:
        """
        Should this be automatically rejected without user interaction?

        Returns True only for category 1 (FAIL) - the AI is confident enough
        to assign this category, so we trust the decision.
        """
        return self.category == 1

    def should_skip_interactive(self) -> bool:
        """
        Should interactive mode be skipped for this result?

        Returns True for definitive categories (FAIL or ACCEPT) where the AI
        has made a clear decision.
        """
        return self.category == 1 or self.category == 5

    def to_json(self) -> str:
        """Serialize to JSON for storage."""
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'AIReviewResult':
        """Deserialize from JSON."""
        data = json.loads(json_str)
        return cls(**data)


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

    def __init__(self, output: OutputWriter, llm: Optional[Llm] = None):
        """
        Initialize LLM review.

        Args:
            test_case_run: Parent TestCaseRun instance
            llm: Optional LLM instance. If None, uses get_llm() default.
        """
        self.output = output
        self.buffer = ""
        self.llm = llm if llm is not None else get_llm()

    # ========== Primitive methods implementation ==========

    def h(self, level: int, title: str):
        """Write a header at the specified level (primitive method)."""
        label = "#" * level + " " + title
        self.buffer += f"\n{label}\n"
        self.output.h(level, title)
        return self

    def t(self, text: str):
        """Write tested text inline (primitive method)."""
        self.buffer += text
        self.output.t(text)
        return self

    def i(self, text: str):
        """Write info text inline (primitive method)."""
        self.buffer += text
        self.output.i(text)
        return self

    def f(self, text: str):
        """Write failed text inline (primitive method)."""
        self.buffer += text
        self.output.f(text)
        return self

    def info_token(self):
        """Mark the token as different (primitive method)."""
        self.output.info_token()
        return self

    def diff(self):
        """Mark the test as different (primitive method)."""
        self.output.diff()
        return self

    def diff_token(self):
        """Mark the token as different (primitive method)."""
        self.output.diff_token()
        return self

    def fail(self):
        """Mark the test as failed (primitive method)."""
        self.output.fail()
        return self

    def fail_token(self):
        """Mark the token as failed (primitive method)."""
        self.output.fail_token()
        return self

    def start_review(self):
        """Start the review section."""
        self.output.h1("review:")
        return self

    def _reviewln(self, do_assert: bool, prompt: str, expected: str, *fail_options: str):
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

Respond with the following JSON format! "result" field value MUST BE be one of listed options. 
Reasons MUST contain concise explanations for the result in the same language the question and the options were defined. 

{
  "result": "optionA", 
  "why": ["reason1", "reason2"]
}

'''

        options = [expected] + list(fail_options)

        request = f"{system_prompt}\n\n{prompt} ({'|'.join(options)})\n\n{self.buffer}"

        def validate_response(parsed):
            return parsed.get("result") in options

        response = self.llm.prompt_json(
            request,
            required_fields=["result", "why"],
            validator=validate_response
        )

        result = response["result"]
        why = response["why"]

        self.output.anchor(f" * {prompt} ").i(result)
        if do_assert:
            self.output.i(" - ").assertln(result == expected)
        else:
            self.iln()
        for i in why:
            self.output.iln(f"    * {i}")

        return result

    def ireviewln(self, prompt: str, expected: str, *fail_options: str) -> str:
        """
        Use LLM to review accumulated output WITHOUT failing the test.

        Returns the LLM's answer for later evaluation. Unlike treviewln(), this does
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
        return self._reviewln(False, prompt, expected, *fail_options)

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
        return self._reviewln(False, prompt, expected, *fail_options)

    def reviewln(self, prompt: str, expected: str, *fail_options: str) -> str:
        """
        Unlike treviewln, this version returns the review object to allow chaining reviews

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
        self._reviewln(True, prompt, expected, *fail_options)
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
        self.output.anchor(f" * {title} ").assertln(condition)
        return self

    def review_test_diff(
        self,
        test_name: str,
        expected: str,
        actual: str,
        diff: str,
        test_description: Optional[str] = None
    ) -> AIReviewResult:
        """
        Use AI to review test output differences and provide a recommendation.

        Args:
            test_name: Name of the test being reviewed
            expected: Previous/expected test output
            actual: Current/actual test output
            diff: Unified diff between expected and actual
            test_description: Optional description of what the test does

        Returns:
            AIReviewResult with AI's analysis and recommendation

        Example:
            result = review.review_test_diff(
                test_name="test_sentiment_analysis",
                expected=previous_output,
                actual=current_output,
                diff=unified_diff
            )
            if result.should_auto_reject():
                print(f"Auto-rejecting: {result.summary}")
        """
        system_prompt = """You are an expert test reviewer for data science and ML applications.
You will analyze test output differences and provide a recommendation.

Your task is to classify the changes into one of 5 categories. The category you choose determines
how the system behaves:

1. FAIL - Clear regressions, critical errors, completely wrong results
   → System will AUTO-REJECT and skip interactive review (unless forced with -I)
   → Use only when you are CONFIDENT this is a regression/failure

2. RECOMMEND FAIL - Likely regressions, suspicious changes, quality degradation
   → System will show interactive prompt with suggestion to reject
   → Use when you suspect problems but want human confirmation

3. UNSURE - Complex changes requiring human judgment, missing context
   → System will show interactive prompt without recommendation
   → Use when you cannot make a confident assessment

4. RECOMMEND ACCEPT - Minor changes, expected improvements, non-functional differences
   → System will show interactive prompt with suggestion to accept
   → Use when changes look reasonable but you want human confirmation

5. ACCEPT - No significant changes, clear improvements, intentional refactoring
   → System will AUTO-ACCEPT and skip interactive review (unless forced with -I)
   → Use only when you are CONFIDENT this is safe to accept

IMPORTANT: Choose categories based on your confidence level. If you're not confident enough
to auto-accept or auto-reject, use RECOMMEND categories or UNSURE.

Consider:
- Are numerical changes within reasonable tolerance?
- Do error messages make sense?
- Are formatting changes cosmetic or meaningful?
- Does the test provide clear success criteria?
- Would a human be able to make a confident decision?

Respond ONLY with valid JSON in this exact format:
{
  "category": 1-5,
  "confidence": 0.0-1.0,
  "summary": "one-line summary (max 80 chars)",
  "rationale": "detailed explanation",
  "issues": ["line X: specific issue", ...],
  "suggestions": ["how to improve test", ...],
  "flags_for_human": true/false
}"""

        desc_section = f"\nTest Purpose: {test_description}\n" if test_description else ""

        request = f"""{system_prompt}

Test: {test_name}{desc_section}

=== PREVIOUS OUTPUT (EXPECTED) ===
{expected}

=== CURRENT OUTPUT (ACTUAL) ===
{actual}

=== DIFF ===
{diff}

Provide your review as JSON:"""

        def validate_ai_review(parsed):
            # Validate category is 1-5
            cat = parsed.get("category")
            if not isinstance(cat, int) or cat < 1 or cat > 5:
                return False
            # Validate confidence is 0-1
            conf = parsed.get("confidence")
            if not isinstance(conf, (int, float)) or conf < 0 or conf > 1:
                return False
            return True

        try:
            result_data = self.llm.prompt_json(
                request,
                required_fields=[
                    "category", "confidence", "summary",
                    "rationale", "issues", "suggestions", "flags_for_human"
                ],
                validator=validate_ai_review,
                max_retries=3
            )

            return AIReviewResult(
                category=result_data['category'],
                confidence=result_data['confidence'],
                summary=result_data['summary'],
                rationale=result_data['rationale'],
                issues=result_data['issues'],
                suggestions=result_data['suggestions'],
                flags_for_human=result_data['flags_for_human']
            )
        except ValueError as e:
            # If AI response is malformed after retries, return unsure result
            return AIReviewResult(
                category=3,  # UNSURE
                confidence=0.0,
                summary="AI review failed - malformed response",
                rationale=str(e),
                issues=[],
                suggestions=["Fix AI prompt or LLM configuration"],
                flags_for_human=True
            )


# Backwards compatibility alias
GptReview = LlmReview
