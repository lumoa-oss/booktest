<!-- markdownlint-disable -->

<a href="../../booktest/reporting/output.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reporting.output`
Base output interface for test case writing and review. 

This module provides a common interface for writing output in both regular test cases (TestCaseRun) and GPT-assisted reviews (GptReview). 

The architecture uses a small set of primitive abstract methods (t, i, fail, h) and builds all other methods on top of these primitives. 



---

<a href="../../booktest/reporting/output.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OutputWriter`
Abstract base class for output writing. 

Provides common methods for writing markdown-formatted output including: 
- Headers (h1, h2, h3) - built on h() 
- Text output (tln, iln, key, anchor, assertln) - built on t(), i(), fail() 
- Tables and dataframes (ttable, tdf, itable, idf) - built on t(), i() via _table() 
- Code blocks (tcode, icode) - built on tln(), iln() 
- Images (timage, iimage) - implemented in TestCaseRun 

Subclasses must implement: 
- h(level, title): Write a header 
- t(text): Write tested text inline (compared against snapshots) 
- i(text): Write info text inline (not tested, but shown in diffs) 
- fail(): Mark current line as failed 
- diff(): Mark current line as different 




---

<a href="../../booktest/reporting/output.py#L513"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `anchor`

```python
anchor(anchor: str)
```

Create an anchor point for non-linear snapshot comparison. Default implementation just writes the anchor text. 

Note: TestCaseRun overrides this to add seek_prefix() functionality. 

---

<a href="../../booktest/reporting/output.py#L523"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `assertln`

```python
assertln(cond: bool, error_message: Optional[str] = None)
```

Assert a condition and print ok/FAILED. Built on i(), fail() primitives. 

---

<a href="../../booktest/reporting/output.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `diff`

```python
diff()
```

Flags the current line as different for review purposes. 

This is a primitive method that must be implemented by subclasses. Returns self for method chaining. 

---

<a href="../../booktest/reporting/output.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `diff_token`

```python
diff_token()
```

Flags the previous token as different for review purposes. 

This is a primitive method that must be implemented by subclasses. Returns self for method chaining. 

---

<a href="../../booktest/reporting/output.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `f`

```python
f(text: str)
```

Write failed text inline (no newline), marking it as failed. 

This is a primitive method that must be implemented by subclasses. In TestCaseRun, this feeds text and marks each token as failed (red). In GptReview, this is added to buffer and delegated to TestCaseRun. 

---

<a href="../../booktest/reporting/output.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fail`

```python
fail()
```

Mark the current line as failed. 

This is a primitive method that must be implemented by subclasses. Returns self for method chaining. 

---

<a href="../../booktest/reporting/output.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fail_token`

```python
fail_token()
```

Mark the previous token as failed. 

This is a primitive method that must be implemented by subclasses. Returns self for method chaining. 

---

<a href="../../booktest/reporting/output.py#L184"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `failln`

```python
failln(text: str = '')
```

Write a line of failed text, marking the entire line as failed (red). Built on f() and fail() primitives. 

All text in the line will be colored red in the output. The line will be marked as failed, causing the test to fail. 

---

<a href="../../booktest/reporting/output.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `fln`

```python
fln(text: str = '')
```

Write failed tokens based on f() primitive 

---

<a href="../../booktest/reporting/output.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `h`

```python
h(level: int, title: str)
```

Write a header at the specified level. 

This is a primitive method that must be implemented by subclasses. TestCaseRun uses header() which includes anchoring logic. GptReview writes directly to buffer and delegates to TestCaseRun. 

---

<a href="../../booktest/reporting/output.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `h1`

```python
h1(title: str)
```

Write a level 1 header. 

---

<a href="../../booktest/reporting/output.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `h2`

```python
h2(title: str)
```

Write a level 2 header. 

---

<a href="../../booktest/reporting/output.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `h3`

```python
h3(title: str)
```

Write a level 3 header. 

---

<a href="../../booktest/reporting/output.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `h4`

```python
h4(title: str)
```

Write a level 4 header. 

---

<a href="../../booktest/reporting/output.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `h5`

```python
h5(title: str)
```

Write a level 4 header. 

---

<a href="../../booktest/reporting/output.py#L226"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `header`

```python
header(header)
```

creates a header line that also operates as an anchor. 

the only difference between this method and anchorln() method is that the header is preceded and followed by an empty line. 

---

<a href="../../booktest/reporting/output.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `i`

```python
i(text: str)
```

Write info text inline (no newline, not compared against snapshots). 

This is a primitive method that must be implemented by subclasses. In TestCaseRun, this bypasses snapshot comparison but still shows differences in 'new | old' format for AI review context. In GptReview, this is added to buffer and delegated to TestCaseRun. 

---

<a href="../../booktest/reporting/output.py#L651"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `icode`

```python
icode(code: str, lang: str = '')
```

Write a code block (info - not tested). Built on iln() primitive. 



**Args:**
 
 - <b>`code`</b>:  The code content 
 - <b>`lang`</b>:  Optional language identifier for syntax highlighting 

---

<a href="../../booktest/reporting/output.py#L668"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `icodeln`

```python
icodeln(code: str, lang: str = '')
```

Alias for icode for backwards compatibility. 

---

<a href="../../booktest/reporting/output.py#L621"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `idf`

```python
idf(df: Any)
```

Write a pandas dataframe as a markdown table (info - not tested). Built on _table() helper and i() primitive. 

Like tdf() but for diagnostic/info output. Changes in DataFrame content are shown in 'new | old' format for AI review but don't fail tests. 



**Args:**
 
 - <b>`df`</b>:  pandas DataFrame or compatible object with .columns and .index 

---

<a href="../../booktest/reporting/output.py#L457"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ifloatln`

```python
ifloatln(value: float, unit: str = None)
```

Write a float value as info with optional delta from previous value. Built on i() and iln() primitives, using _get_expected_token() for comparison. 

If a previous value exists in snapshot, shows: "0.850 (was 0.820)" Otherwise shows: "0.850" 



**Args:**
 
 - <b>`value`</b>:  Float value to display 
 - <b>`unit`</b>:  Optional unit string (e.g., "%", "ms") 



**Example:**
 t.ifloatln(0.973, "%")  # Output: "0.973% (was 0.950%)" 

---

<a href="../../booktest/reporting/output.py#L289"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `iimage`

```python
iimage(file, alt_text=None)
```

Adds a markdown image in the info stream (not tested). 

Like timage() but for diagnostic/info output. Changes in image paths are shown in 'new | old' format for AI review but don't fail tests. 

Useful for plots, charts, and visualizations that help understand test behavior but shouldn't cause test failure if they change. 



**Args:**
 
 - <b>`file`</b>:  Path to the image file 
 - <b>`alt_text`</b>:  Optional alt text for the image (defaults to filename) 



**Example:**
 t.iimage("plots/accuracy_curve.png", "Training Accuracy") 

---

<a href="../../booktest/reporting/output.py#L331"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ilist`

```python
ilist(list, prefix=' * ')
```

Writes the list into test stream. By default, the list is prefixed by markdown ' * ' list expression. 

For example following call: 

```python
t.tlist(["a", "b", "c"])
``` 

will produce: 

* a * b * c 

---

<a href="../../booktest/reporting/output.py#L171"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `iln`

```python
iln(text: str = '')
```

Write a line of info text (not compared against snapshots). Built on i() primitive. 

Info output appears in test results and is written to both old and new output files. When content changes, it shows in 'new | old' format for AI review without marking the test as failed. 

---

<a href="../../booktest/reporting/output.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `imsln`

```python
imsln(f)
```

runs the function f and measures the time milliseconds it took. the measurement is printed in the test stream and compared into previous result in the snaphost file. 

This method also prints a new line after the measurements. 

NOTE: unline tmsln(), this method never fails or marks a difference. 

---

<a href="../../booktest/reporting/output.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `info_token`

```python
info_token()
```

Flags the previous token as different in non-breaking way for review purposes. 

This is a primitive method that must be implemented by subclasses. Returns self for method chaining. 

---

<a href="../../booktest/reporting/output.py#L427"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `it`

```python
it(name, it)
```

Creates TestIt class around the `it` object named with `name` 

This can be used for assertions as in: 

```python
result = [1, 2]
t.it("result", result).must_be_a(list).must_contain(1).must_contain(2)
``` 

---

<a href="../../booktest/reporting/output.py#L607"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `itable`

```python
itable(table: dict)
```

Write a markdown table from a dictionary of columns (info - not tested). Built on _table() helper. 

Like ttable() but for diagnostic/info output. Changes in table content are shown in 'new | old' format for AI review but don't fail tests. 



**Example:**
  t.itable({"metric": ["accuracy", "f1"], "value": [0.95, 0.92]}) 

---

<a href="../../booktest/reporting/output.py#L487"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ivalueln`

```python
ivalueln(value: Any, unit: str = None)
```

Write any value as info with optional delta from previous value. Built on i() and iln() primitives, using _get_expected_token() for comparison. 

If a previous value exists in snapshot, shows: "42 (was 38)" Otherwise shows: "42" 



**Args:**
 
 - <b>`value`</b>:  Value to display (converted to string) 
 - <b>`unit`</b>:  Optional unit string (e.g., "items", "users") 



**Example:**
 t.ivalueln(1000, "users")  # Output: "1000 users (was 950 users)" 

---

<a href="../../booktest/reporting/output.py#L453"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `key`

```python
key(key)
```

Override key() to add anchor() functionality specific to TestCaseRun. 

---

<a href="../../booktest/reporting/output.py#L216"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `keyvalueln`

```python
keyvalueln(key: str, value: str)
```

Write a key-value pair on a single line. Built on key() and tln() primitives. 



**Example:**
  t.keyvalueln("Name:", "Alice")  # Output: "Name: Alice" 

---

<a href="../../booktest/reporting/output.py#L387"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `must_apply`

```python
must_apply(it, title, cond, error_message=None)
```

Assertions with decoration for testing, whether `it` fulfills a condition. 

Maily used by TestIt class 

---

<a href="../../booktest/reporting/output.py#L415"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `must_be_a`

```python
must_be_a(it, typ)
```

Assertions with decoration for testing, whether `it` is of specific type. 

Maily used by TestIt class 

---

<a href="../../booktest/reporting/output.py#L397"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `must_contain`

```python
must_contain(it, member)
```

Assertions with decoration for testing, whether `it` contains a member. 

Maily used by TestIt class 

---

<a href="../../booktest/reporting/output.py#L406"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `must_equal`

```python
must_equal(it, value)
```

Assertions with decoration for testing, whether `it` equals something. 

Maily used by TestIt class 

---

<a href="../../booktest/reporting/output.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `t`

```python
t(text: str)
```

Write tested text inline (no newline). 

This is a primitive method that must be implemented by subclasses. In TestCaseRun, this is compared against snapshots. In GptReview, this is added to buffer and delegated to TestCaseRun. 

---

<a href="../../booktest/reporting/output.py#L634"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tcode`

```python
tcode(code: str, lang: str = '')
```

Write a code block (tested). Built on tln() primitive. 



**Args:**
 
 - <b>`code`</b>:  The code content 
 - <b>`lang`</b>:  Optional language identifier for syntax highlighting 

---

<a href="../../booktest/reporting/output.py#L672"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tcodeln`

```python
tcodeln(code: str, lang: str = '')
```

Alias for tcode. 

---

<a href="../../booktest/reporting/output.py#L597"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tdf`

```python
tdf(df: Any)
```

Write a pandas dataframe as a markdown table (tested). Built on _table() helper and t() primitive. 



**Args:**
 
 - <b>`df`</b>:  pandas DataFrame or compatible object with .columns and .index 

---

<a href="../../booktest/reporting/output.py#L441"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tformat`

```python
tformat(value)
```

Converts the value into json like structure containing only the value types. 

Prints a json containing the value types. 

Mainly used for getting snapshot of a e.g. Json response format. 

---

<a href="../../booktest/reporting/output.py#L276"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `timage`

```python
timage(file, alt_text=None)
```

Adds a markdown image in the test stream (tested). 



**Args:**
 
 - <b>`file`</b>:  Path to the image file 
 - <b>`alt_text`</b>:  Optional alt text for the image (defaults to filename) 

---

<a href="../../booktest/reporting/output.py#L311"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tlist`

```python
tlist(list, prefix=' * ')
```

Writes the list into test stream. By default, the list is prefixed by markdown ' * ' list expression. 

For example following call: 

```python
t.tlist(["a", "b", "c"])
``` 

will produce: 

* a * b * c 

---

<a href="../../booktest/reporting/output.py#L162"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tln`

```python
tln(text: str = '')
```

Write a line of tested text (compared against snapshots). Built on t() primitive. 

---

<a href="../../booktest/reporting/output.py#L759"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tmetric_pct`

```python
tmetric_pct(
    value: float,
    tolerance_pct: float,
    unit: str = None,
    direction: str = None
)
```

Test metric with percentage-based tolerance. 

Instead of absolute tolerance, uses percentage of baseline value. For example, tolerance_pct=5 means accept ±5% change from baseline. 



**Args:**
 
 - <b>`value`</b>:  Current value 
 - <b>`tolerance_pct`</b>:  Acceptable percentage change (e.g., 5 for ±5%) 
 - <b>`unit`</b>:  Optional display unit 
 - <b>`direction`</b>:  Optional constraint ">=" or "<=" 



**Example:**
 # 100 → 95: 5% drop → within 5% → OK # 100 → 90: 10% drop → exceeds 5% → FAIL t.tmetric_pct(95, tolerance_pct=5, unit="ms") 

---

<a href="../../booktest/reporting/output.py#L676"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tmetricln`

```python
tmetricln(
    value: float,
    tolerance: float,
    unit: str = None,
    direction: str = None
)
```

Test a metric value with tolerance for acceptable variation, ending with newline. 

Compares current metric against snapshot value and accepts changes within tolerance. Useful for ML metrics that naturally fluctuate (accuracy, F1, etc). 



**Args:**
 
 - <b>`value`</b>:  Current metric value 
 - <b>`tolerance`</b>:  Acceptable absolute difference from baseline 
 - <b>`unit`</b>:  Optional unit for display (e.g., "%", "ms", "sec") 
 - <b>`direction`</b>:  Optional constraint: 
        - ">=" : Only fail on drops (value < baseline - tolerance) 
        - "<=" : Only fail on increases (value > baseline + tolerance) 
        - None : Fail if abs(value - baseline) > tolerance 

Behavior: 
    - If no snapshot exists: Record as baseline 
    - If within tolerance: Show delta but mark OK 
    - If exceeds tolerance: Mark as FAIL (using fail() primitive) 



**Example:**
 t.tmetricln(0.973, tolerance=0.02)  # Accuracy ±2% t.tmetricln(97.3, tolerance=2, unit="%")  # Same, with units t.tmetricln(0.973, tolerance=0.02, direction=">=")  # Only fail on drops t.tmetricln(latency_ms, tolerance=5, unit="ms", direction="<=")  # No increases 

Output examples: 0.973 (baseline)                           # First run 0.973 (was 0.950, Δ+0.023)                # DIFF within tolerance → OK 0.920 (was 0.950, Δ-0.030)                # Exceeds tolerance → FAIL 97.3% (was 95.0%, Δ+2.3%)                 # With units 

---

<a href="../../booktest/reporting/output.py#L241"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tmsln`

```python
tmsln(f, max_ms)
```

runs the function f and measures the time milliseconds it took. the measurement is printed in the test stream and compared into previous result in the snaphost file. 

This method also prints a new line after the measurements. 

NOTE: if max_ms is defined, this line will fail, if the test took more than max_ms milliseconds. 

---

<a href="../../booktest/reporting/output.py#L351"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `tset`

```python
tset(items, prefix=' * ')
```

This method used to print and compare a set of items to expected set in out of order fashion. It will first scan the next elements based on prefix. After this step, it will check whether the items were in the list. 

NOTE: this method may be slow, if the set order is unstable. 

---

<a href="../../booktest/reporting/output.py#L586"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `ttable`

```python
ttable(table: dict)
```

Write a markdown table from a dictionary of columns (tested). Built on _table() helper. 



**Example:**
  t.ttable({"x": [1, 2, 3], "y": [2, 3, 4]}) 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
