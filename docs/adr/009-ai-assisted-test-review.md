# ADR 009: AI-Assisted Test Review

## Status

Proposed

## Context

Manual test review can be time-consuming, especially when dealing with large test outputs or numerous tests with differences. While human judgment is crucial for final decisions, an AI can help by:

1. Quickly analyzing test output differences
2. Categorizing changes by significance
3. Identifying likely issues that need human attention
4. Providing initial recommendations with rationale
5. Suggesting test improvements for easier review

This would complement the existing LLM-based test evaluation (from ADR 006) which generates test output, by adding AI-assisted review of differences.

## Decision

We will implement AI-assisted test review that analyzes tests marked as DIFF and provides recommendations in 5 categories:

### 1. Classification Categories

1. **FAIL** (1) - Automatic failure
   - Clear regressions detected
   - Critical errors introduced
   - Expected outputs completely wrong

2. **RECOMMEND FAIL** (2) - Suggest rejection with human review
   - Likely regressions
   - Suspicious changes
   - Quality degradation

3. **UNSURE** (3) - Requires human judgment
   - Complex changes
   - Ambiguous differences
   - Missing context for decision

4. **RECOMMEND ACCEPT** (4) - Suggest acceptance with human review
   - Minor formatting changes
   - Expected improvements
   - Non-functional differences

5. **ACCEPT** (5) - Automatic acceptance
   - No significant changes
   - Clear improvements
   - Intentional refactoring reflected correctly

### 2. AI Review Input

The AI will receive:
- Test description and purpose (from test code)
- Previous test output (expected)
- Current test output (actual)
- Diff between outputs
- Test context (file path, test name, etc.)
- Review instructions specific to booktest

### 3. AI Review Output

For each reviewed test, the AI provides:

```python
@dataclass
class AIReviewResult:
    category: int  # 1-5
    rationale: str  # Why this classification
    summary: str  # One-line summary for reports
    issues: List[str]  # Specific line numbers/issues
    suggestions: List[str]  # How to improve the test
    confidence: float  # 0-1, how confident in the decision
    flags_for_human: bool  # Should human definitely review this
```

### 4. Command Line Interface

```bash
# Enable AI review for all DIFF tests
booktest -g

# Enable AI review and run interactively
booktest -g -i

# Only run AI review on failed tests
booktest -c -g

# Verbose mode shows full AI analysis
booktest -g -v
```

### 5. Interactive Mode Integration

During interactive review (`-i` mode), users can:
- Press `g` to request AI review for current test
- See AI recommendation with rationale
- Choose to accept/reject AI suggestion
- View full analysis in verbose mode

Example interaction:
```
test/sentiment_test.py::test_sentiment_analysis - DIFF

? positive: 0.85 -> 0.82                                | positive: 0.85
? negative: 0.10 -> 0.15                                | negative: 0.10
? neutral: 0.05 -> 0.03                                 | neutral: 0.05

AI recommends FAIL (confidence: 0.92):
  Regression detected: Negative sentiment increased significantly

  Issue on line 43: "I wasn't impressed" now classified as neutral (0.45)
  instead of negative (0.75)

  Suggestion: Add ground truth labels and accuracy metrics to test output
  to make review more objective

Accept changes? [y/n/g for AI review/v for verbose]:
```

### 6. Report Integration

AI notes appear inline in reports:

**Compact format** (default):
```
test/api_test.py::test_response - OK (no significant changes)
test/sentiment_test.py::test_analysis - FAIL (regression in negative sentiment)
test/format_test.py::test_output - ACCEPT (formatting improved)
```

**Verbose format** (`-v`):
```
test/sentiment_test.py::test_sentiment_analysis - FAIL

AI Review (confidence: 0.92):
  Category: FAIL

  Rationale:
  The test shows a regression in sentiment classification accuracy.
  The model previously correctly identified "I wasn't impressed" as
  negative (0.75) but now classifies it as neutral (0.45).

  Issues:
  - Line 43: Sentiment changed from negative to neutral
  - Overall negative sentiment increased from 0.10 to 0.15
  - Positive sentiment decreased from 0.85 to 0.82

  Suggestions:
  - Add ground truth labels to test data
  - Calculate and display accuracy metrics
  - Include confusion matrix in output
  - Set tolerance thresholds for acceptable variation
```

### 7. Storage and History

AI review results stored alongside test results:

```
books/
  test/
    sentiment_test.py/
      test_sentiment_analysis.md       # Test output
      test_sentiment_analysis.ai.json  # AI review result
```

This allows:
- Reviewing AI decisions later
- Improving AI prompts based on accuracy
- Tracking AI confidence over time
- Debugging incorrect AI classifications

### 8. Configuration

In `booktest.ini`:

```ini
[ai_review]
# Enable AI review by default
enabled = false

# LLM provider (uses same config as llm section)
provider = gpt

# Confidence threshold for auto-accept/reject
auto_accept_threshold = 0.95
auto_reject_threshold = 0.95

# Categories that can be auto-accepted
auto_accept_categories = 5

# Categories that can be auto-rejected
auto_reject_categories = 1

# Always flag certain test patterns for human review
require_human_review = **/security_*.py, **/payment_*.py
```

### 9. Implementation Strategy

1. **Phase 1**: Basic AI review with manual invocation (`-g` flag)
2. **Phase 2**: Interactive mode integration (press `g` during review)
3. **Phase 3**: Automatic review with confidence thresholds
4. **Phase 4**: Learning from human corrections

### 10. Prompt Engineering

The AI prompt will include:

```
You are reviewing a test output for a data science/ML application.

Context:
- Test: {test_name}
- Purpose: {test_description}
- Previous output: {expected}
- Current output: {actual}
- Diff: {diff}

Your task:
1. Classify the changes into one of 5 categories (1=fail, 5=accept)
2. Provide a clear rationale
3. Flag specific issues with line numbers
4. Suggest test improvements

Guidelines:
- FAIL (1): Clear regressions, critical errors, wrong results
- RECOMMEND FAIL (2): Suspicious changes, likely issues
- UNSURE (3): Need human judgment, complex changes
- RECOMMEND ACCEPT (4): Minor changes, likely acceptable
- ACCEPT (5): No significant changes, clear improvements

Consider:
- Are numerical changes within reasonable tolerance?
- Do error messages make sense?
- Are formatting changes cosmetic or meaningful?
- Does the test provide clear success criteria?
- Would a human be able to make a confident decision?

Format your response as JSON:
{
  "category": 1-5,
  "confidence": 0.0-1.0,
  "summary": "one-line summary",
  "rationale": "detailed explanation",
  "issues": ["line X: issue description"],
  "suggestions": ["how to improve test"],
  "flags_for_human": true/false
}
```

### 11. Privacy and Security

- AI review is opt-in (requires `-g` flag or config)
- Test outputs may contain sensitive data - warn users
- Support local LLM providers for sensitive environments
- Add option to redact patterns before sending to AI
- Log what data is sent to external AI services

## Consequences

### Positive

- **Faster reviews**: AI handles obvious cases immediately
- **Better focus**: Humans focus on truly ambiguous cases
- **Consistency**: AI applies same criteria across all tests
- **Learning**: AI suggestions help improve test quality
- **Traceability**: Full review history with rationale
- **Scalability**: Can review hundreds of tests efficiently

### Negative

- **AI errors**: Wrong classifications possible, need human oversight
- **Privacy concerns**: Test data sent to external AI services
- **Cost**: API calls for AI review (can be significant)
- **Complexity**: Additional component to maintain
- **Over-reliance**: Risk of blindly accepting AI recommendations
- **False confidence**: AI may be confident but wrong

### Mitigation

- Keep confidence thresholds high for auto-accept/reject
- Always show AI rationale, not just decision
- Allow easy override of AI decisions
- Track AI accuracy and improve prompts
- Support local LLM deployment
- Make AI review opt-in, not default
- Clear warnings about data sent to AI

## Alternatives Considered

### 1. Rule-Based Heuristics

Use simple rules like "accept if diff < 1%".

**Rejected**: Too rigid, can't handle semantic changes, misses context.

### 2. ML Model Trained on Historical Reviews

Train a custom model on past human review decisions.

**Rejected**: Requires large training dataset, complex to maintain, less flexible than LLM.

### 3. AI Generates Expected Output Instead of Reviewing

Have AI predict expected output, compare with actual.

**Rejected**: Doesn't help with reviewing differences, just moves the problem.

### 4. Mandatory AI Review

Require AI review for all DIFF tests automatically.

**Rejected**: Privacy concerns, costs, and risk of over-reliance on AI.

## Related

- ADR 006: LLM-Assisted Test Evaluation (AI generates output)
- ADR 004: Git-Based Snapshot Storage (review integration)
- This ADR focuses on AI reviewing differences, not generating output

## Implementation Notes

Key files to modify:
- `booktest/reporting/review.py` - Add AI review integration
- `booktest/llm/llm_review.py` - Implement AI review logic
- `booktest/core/tests.py` - Add `-g` flag handling
- `booktest/reporting/reports.py` - Store AI review results
- `booktest/config/config.py` - Add AI review configuration

Integration points:
- Reuse existing LLM infrastructure from ADR 006
- Store AI reviews alongside test results
- Display AI feedback in review UI
- Allow overriding AI decisions

Example usage in code:

```python
from booktest import LlmReview

# During test execution with -g flag
if config.get('ai_review_enabled'):
    review = LlmReview()
    result = review.review_test_diff(
        test_name=test_name,
        expected=expected_output,
        actual=actual_output,
        diff=diff_output
    )

    if result.category == 1 and result.confidence > 0.95:
        # Auto-fail
        mark_test_failed(test_name, result.summary)
    elif result.category == 5 and result.confidence > 0.95:
        # Auto-accept
        mark_test_passed(test_name, result.summary)
    else:
        # Human review required
        prompt_human_review(test_name, result)
```

## Future Enhancements

1. **Learn from corrections**: Track when humans override AI decisions, improve prompts
2. **Test-specific prompts**: Customize AI instructions per test or test suite
3. **Confidence calibration**: Adjust confidence based on historical accuracy
4. **Multi-LLM voting**: Use multiple LLMs, combine their recommendations
5. **Incremental review**: Review only changed sections of large outputs
6. **Natural language queries**: "Show me tests where AI was unsure about performance"
