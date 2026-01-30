<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.llm.llm_review`
LLM-assisted review functionality for booktest. 

This module provides LlmReview class for using LLM models to automatically review test outputs and validate results against expectations. 

**Global Variables**
---------------
- **TYPE_CHECKING**


---

## <kbd>class</kbd> `AIReviewResult`
Result of an AI-assisted test review. 

The AI analyzes test output differences and provides a recommendation on whether to accept or reject the changes. 

### <kbd>method</kbd> `__init__`

```python
__init__(
    category: int,
    confidence: float,
    summary: str,
    rationale: str,
    issues: List[str],
    suggestions: List[str],
    flags_for_human: bool
) → None
```








---

### <kbd>method</kbd> `category_name`

```python
category_name() → str
```

Get human-readable category name. 

---

### <kbd>classmethod</kbd> `from_json`

```python
from_json(json_str: str) → AIReviewResult
```

Deserialize from JSON. 

---

### <kbd>method</kbd> `should_auto_accept`

```python
should_auto_accept() → bool
```

Should this be automatically accepted without user interaction? 

Returns True only for category 5 (ACCEPT) - the AI is confident enough to assign this category, so we trust the decision. 

---

### <kbd>method</kbd> `should_auto_reject`

```python
should_auto_reject() → bool
```

Should this be automatically rejected without user interaction? 

Returns True only for category 1 (FAIL) - the AI is confident enough to assign this category, so we trust the decision. 

---

### <kbd>method</kbd> `should_skip_interactive`

```python
should_skip_interactive() → bool
```

Should interactive mode be skipped for this result? 

Returns True for definitive categories (FAIL or ACCEPT) where the AI has made a clear decision. 

---

### <kbd>method</kbd> `to_json`

```python
to_json() → str
```

Serialize to JSON for storage. 


---

## <kbd>class</kbd> `LlmReview`
LLM-assisted review for test outputs. 

LlmReview accumulates test output in a buffer and uses an LLM to answer questions about the output, enabling automated validation of complex test results that would be difficult to assert programmatically. 

Example usage:  def test_llm_output(t: bt.TestCaseRun):  r = t.start_review() 

 r.h1("Generated Code:")  r.icode(generated_code, "python") 

 r.h1("Output:")  r.iln(program_output) 

 r.start_review()  r.reviewln("Does the code follow PEP8?", "Yes", "No")  r.reviewln("Are comments helpful?", "Yes", "No")  r.assertln("Does code run without errors?", no_errors) 

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

### <kbd>method</kbd> `__init__`

```python
__init__(output: OutputWriter, llm: Optional[Llm] = None)
```

Initialize LLM review. 



**Args:**
 
 - <b>`test_case_run`</b>:  Parent TestCaseRun instance 
 - <b>`llm`</b>:  Optional LLM instance. If None, uses get_llm() default. 




---

### <kbd>method</kbd> `assertln`

```python
assertln(title: str, condition: bool)
```

Assert a condition with a descriptive title. 



**Args:**
 
 - <b>`title`</b>:  Description of what is being asserted 
 - <b>`condition`</b>:  Boolean condition to assert 



**Example:**
 r.assertln("Code runs without errors", exception is None) 

---

### <kbd>method</kbd> `diff`

```python
diff()
```

Mark the test as different (primitive method). 

---

### <kbd>method</kbd> `diff_token`

```python
diff_token()
```

Mark the token as different (primitive method). 

---

### <kbd>method</kbd> `f`

```python
f(text: str)
```

Write failed text inline (primitive method). 

---

### <kbd>method</kbd> `fail`

```python
fail()
```

Mark the test as failed (primitive method). 

---

### <kbd>method</kbd> `fail_token`

```python
fail_token()
```

Mark the token as failed (primitive method). 

---

### <kbd>method</kbd> `h`

```python
h(level: int, title: str)
```

Write a header at the specified level (primitive method). 

---

### <kbd>method</kbd> `i`

```python
i(text: str)
```

Write info text inline (primitive method). 

---

### <kbd>method</kbd> `info_token`

```python
info_token()
```

Mark the token as different (primitive method). 

---

### <kbd>method</kbd> `ireviewln`

```python
ireviewln(prompt: str, expected: str, *fail_options: str) → str
```

Use LLM to review accumulated output WITHOUT failing the test. 

Returns the LLM's answer for later evaluation. Unlike reviewln(), this does not assert - it just records the answer as info output. 



**Args:**
 
 - <b>`prompt`</b>:  Question to ask about the output 
 - <b>`expected`</b>:  Expected answer (for display/context) 
 - <b>`*fail_options`</b>:  Alternative answers (for display/context) 



**Returns:**
 The LLM's response 



**Example:**
 result = r.ireviewln("Is code well documented?", "Yes", "No") # Test continues regardless of result 

---

### <kbd>method</kbd> `review_test_diff`

```python
review_test_diff(
    test_name: str,
    expected: str,
    actual: str,
    diff: str,
    test_description: Optional[str] = None
) → AIReviewResult
```

Use AI to review test output differences and provide a recommendation. 



**Args:**
 
 - <b>`test_name`</b>:  Name of the test being reviewed 
 - <b>`expected`</b>:  Previous/expected test output 
 - <b>`actual`</b>:  Current/actual test output 
 - <b>`diff`</b>:  Unified diff between expected and actual 
 - <b>`test_description`</b>:  Optional description of what the test does 



**Returns:**
 AIReviewResult with AI's analysis and recommendation 



**Example:**
 result = review.review_test_diff(  test_name="test_sentiment_analysis",  expected=previous_output,  actual=current_output,  diff=unified_diff ) if result.should_auto_reject():  print(f"Auto-rejecting: {result.summary}") 

---

### <kbd>method</kbd> `start_review`

```python
start_review()
```

Start the review section. 

---

### <kbd>method</kbd> `t`

```python
t(text: str)
```

Write tested text inline (primitive method). 

---

### <kbd>method</kbd> `treviewln`

```python
treviewln(prompt: str, expected: str, *fail_options: str) → str
```

Use LLM to review accumulated output and snapshot the result (tested output). 

Like ireviewln() but writes to tested output (tln) instead of info output (iln). Still does not fail - just records for later evaluation. 



**Args:**
 
 - <b>`prompt`</b>:  Question to ask about the output 
 - <b>`expected`</b>:  Expected answer (for display/context) 
 - <b>`*fail_options`</b>:  Alternative answers (for display/context) 



**Returns:**
 The LLM's response 



**Example:**
 result = r.treviewln("Is code well documented?", "Yes", "No") # Test continues regardless of result 


---

## <kbd>class</kbd> `LlmReview`
LLM-assisted review for test outputs. 

LlmReview accumulates test output in a buffer and uses an LLM to answer questions about the output, enabling automated validation of complex test results that would be difficult to assert programmatically. 

Example usage:  def test_llm_output(t: bt.TestCaseRun):  r = t.start_review() 

 r.h1("Generated Code:")  r.icode(generated_code, "python") 

 r.h1("Output:")  r.iln(program_output) 

 r.start_review()  r.reviewln("Does the code follow PEP8?", "Yes", "No")  r.reviewln("Are comments helpful?", "Yes", "No")  r.assertln("Does code run without errors?", no_errors) 

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

### <kbd>method</kbd> `__init__`

```python
__init__(output: OutputWriter, llm: Optional[Llm] = None)
```

Initialize LLM review. 



**Args:**
 
 - <b>`test_case_run`</b>:  Parent TestCaseRun instance 
 - <b>`llm`</b>:  Optional LLM instance. If None, uses get_llm() default. 




---

### <kbd>method</kbd> `assertln`

```python
assertln(title: str, condition: bool)
```

Assert a condition with a descriptive title. 



**Args:**
 
 - <b>`title`</b>:  Description of what is being asserted 
 - <b>`condition`</b>:  Boolean condition to assert 



**Example:**
 r.assertln("Code runs without errors", exception is None) 

---

### <kbd>method</kbd> `diff`

```python
diff()
```

Mark the test as different (primitive method). 

---

### <kbd>method</kbd> `diff_token`

```python
diff_token()
```

Mark the token as different (primitive method). 

---

### <kbd>method</kbd> `f`

```python
f(text: str)
```

Write failed text inline (primitive method). 

---

### <kbd>method</kbd> `fail`

```python
fail()
```

Mark the test as failed (primitive method). 

---

### <kbd>method</kbd> `fail_token`

```python
fail_token()
```

Mark the token as failed (primitive method). 

---

### <kbd>method</kbd> `h`

```python
h(level: int, title: str)
```

Write a header at the specified level (primitive method). 

---

### <kbd>method</kbd> `i`

```python
i(text: str)
```

Write info text inline (primitive method). 

---

### <kbd>method</kbd> `info_token`

```python
info_token()
```

Mark the token as different (primitive method). 

---

### <kbd>method</kbd> `ireviewln`

```python
ireviewln(prompt: str, expected: str, *fail_options: str) → str
```

Use LLM to review accumulated output WITHOUT failing the test. 

Returns the LLM's answer for later evaluation. Unlike reviewln(), this does not assert - it just records the answer as info output. 



**Args:**
 
 - <b>`prompt`</b>:  Question to ask about the output 
 - <b>`expected`</b>:  Expected answer (for display/context) 
 - <b>`*fail_options`</b>:  Alternative answers (for display/context) 



**Returns:**
 The LLM's response 



**Example:**
 result = r.ireviewln("Is code well documented?", "Yes", "No") # Test continues regardless of result 

---

### <kbd>method</kbd> `review_test_diff`

```python
review_test_diff(
    test_name: str,
    expected: str,
    actual: str,
    diff: str,
    test_description: Optional[str] = None
) → AIReviewResult
```

Use AI to review test output differences and provide a recommendation. 



**Args:**
 
 - <b>`test_name`</b>:  Name of the test being reviewed 
 - <b>`expected`</b>:  Previous/expected test output 
 - <b>`actual`</b>:  Current/actual test output 
 - <b>`diff`</b>:  Unified diff between expected and actual 
 - <b>`test_description`</b>:  Optional description of what the test does 



**Returns:**
 AIReviewResult with AI's analysis and recommendation 



**Example:**
 result = review.review_test_diff(  test_name="test_sentiment_analysis",  expected=previous_output,  actual=current_output,  diff=unified_diff ) if result.should_auto_reject():  print(f"Auto-rejecting: {result.summary}") 

---

### <kbd>method</kbd> `start_review`

```python
start_review()
```

Start the review section. 

---

### <kbd>method</kbd> `t`

```python
t(text: str)
```

Write tested text inline (primitive method). 

---

### <kbd>method</kbd> `treviewln`

```python
treviewln(prompt: str, expected: str, *fail_options: str) → str
```

Use LLM to review accumulated output and snapshot the result (tested output). 

Like ireviewln() but writes to tested output (tln) instead of info output (iln). Still does not fail - just records for later evaluation. 



**Args:**
 
 - <b>`prompt`</b>:  Question to ask about the output 
 - <b>`expected`</b>:  Expected answer (for display/context) 
 - <b>`*fail_options`</b>:  Alternative answers (for display/context) 



**Returns:**
 The LLM's response 



**Example:**
 result = r.treviewln("Is code well documented?", "Yes", "No") # Test continues regardless of result 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
