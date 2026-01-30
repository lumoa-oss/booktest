<!-- markdownlint-disable -->

<a href="../../booktest/reporting/reports.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reporting.reports`





---

<a href="../../booktest/reporting/reports.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `test_result_to_exit_code`

```python
test_result_to_exit_code(test_result)
```

Convert test result to exit code (supports both legacy and new format) 


---

<a href="../../booktest/reporting/reports.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `write_lines`

```python
write_lines(path, file, lines)
```






---

<a href="../../booktest/reporting/reports.py#L95"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `read_lines`

```python
read_lines(path, filename=None)
```






---

<a href="../../booktest/reporting/reports.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TestResult`
Legacy single-dimensional test result (for backward compatibility) 





---

<a href="../../booktest/reporting/reports.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SuccessState`
Test logic outcome - independent of snapshot management 





---

<a href="../../booktest/reporting/reports.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SnapshotState`
Snapshot integrity outcome - independent of test logic 





---

<a href="../../booktest/reporting/reports.py#L35"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TwoDimensionalTestResult`
Two-dimensional test result separating logic success from snapshot management 




---

<a href="../../booktest/reporting/reports.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `can_auto_approve`

```python
can_auto_approve() → bool
```

Check if this result can be auto-approved without human review 

---

<a href="../../booktest/reporting/reports.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_success`

```python
is_success() → bool
```

Check if the test logic succeeded (regardless of snapshots) 

---

<a href="../../booktest/reporting/reports.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `requires_review`

```python
requires_review() → bool
```

Check if this result requires human review 

---

<a href="../../booktest/reporting/reports.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_legacy_result`

```python
to_legacy_result() → <enum 'TestResult'>
```

Convert to legacy single-dimensional result for backward compatibility 


---

<a href="../../booktest/reporting/reports.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `UserRequest`








---

<a href="../../booktest/reporting/reports.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Metrics`
Stores the top level test metrics/results 

<a href="../../booktest/reporting/reports.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(took_ms)
```








---

<a href="../../booktest/reporting/reports.py#L139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `of_dir`

```python
of_dir(dir)
```





---

<a href="../../booktest/reporting/reports.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `of_file`

```python
of_file(path)
```





---

<a href="../../booktest/reporting/reports.py#L136"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dir`

```python
to_dir(dir)
```





---

<a href="../../booktest/reporting/reports.py#L124"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_file`

```python
to_file(path)
```






---

<a href="../../booktest/reporting/reports.py#L144"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CaseReports`
This class manages the saved case specific metrics/results. 

Supports both legacy text format (cases.txt) and new JSON format (cases.json). The JSON format includes AI review results which are invalidated when tests rerun. 

<a href="../../booktest/reporting/reports.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(cases, ai_reviews=None)
```

Initialize CaseReports. 



**Args:**
 
 - <b>`cases`</b>:  List of (case_name, result, duration) tuples 
 - <b>`ai_reviews`</b>:  Optional dict mapping case_name to AIReviewResult 




---

<a href="../../booktest/reporting/reports.py#L173"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `by_name`

```python
by_name(name)
```





---

<a href="../../booktest/reporting/reports.py#L193"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `cases_to_done_and_todo`

```python
cases_to_done_and_todo(cases, config)
```





---

<a href="../../booktest/reporting/reports.py#L166"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `failed`

```python
failed()
```





---

<a href="../../booktest/reporting/reports.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `failed_with_details`

```python
failed_with_details()
```

Return failed test cases with their result type and duration. 

---

<a href="../../booktest/reporting/reports.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ai_review`

```python
get_ai_review(case_name)
```

Get AI review for a specific test case, if available. 

---

<a href="../../booktest/reporting/reports.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `make_case`

```python
make_case(case_name, res: TestResult, duration)
```





---

<a href="../../booktest/reporting/reports.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `of_dir`

```python
of_dir(out_dir)
```

Load case reports from directory. 

Prefers cases.ndjson (NDJSON) if it exists, falls back to cases.txt for backward compatibility. 

---

<a href="../../booktest/reporting/reports.py#L225"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `of_file`

```python
of_file(file_name)
```





---

<a href="../../booktest/reporting/reports.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `of_jsonl_file`

```python
of_jsonl_file(file_name)
```

Load case reports from NDJSON file (newline-delimited JSON). 

---

<a href="../../booktest/reporting/reports.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `passed`

```python
passed()
```





---

<a href="../../booktest/reporting/reports.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_ai_review`

```python
set_ai_review(case_name, ai_review)
```

Set AI review for a specific test case. 



**Args:**
 
 - <b>`case_name`</b>:  Test case name 
 - <b>`ai_review`</b>:  AIReviewResult object or None to remove 

---

<a href="../../booktest/reporting/reports.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_dir`

```python
to_dir(out_dir)
```

Save case reports to directory (uses NDJSON format). 

---

<a href="../../booktest/reporting/reports.py#L272"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_file`

```python
to_file(file)
```

Save to legacy text format (for backward compatibility). 

---

<a href="../../booktest/reporting/reports.py#L336"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `to_jsonl_file`

```python
to_jsonl_file(file_name)
```

Save case reports to NDJSON file (newline-delimited JSON). 

---

<a href="../../booktest/reporting/reports.py#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_case`

```python
write_case(file_handle, case_name, res: TestResult, duration)
```





---

<a href="../../booktest/reporting/reports.py#L364"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `write_case_jsonl`

```python
write_case_jsonl(
    file_handle,
    case_name,
    res: TestResult,
    duration,
    ai_review=None
)
```

Write a single case to NDJSON file. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
