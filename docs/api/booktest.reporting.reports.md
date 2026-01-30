<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.reporting.reports`





---

## <kbd>function</kbd> `test_result_to_exit_code`

```python
test_result_to_exit_code(test_result)
```

Convert test result to exit code (supports both legacy and new format) 


---

## <kbd>function</kbd> `write_lines`

```python
write_lines(path, file, lines)
```






---

## <kbd>function</kbd> `read_lines`

```python
read_lines(path, filename=None)
```






---

## <kbd>class</kbd> `TestResult`
Legacy single-dimensional test result (for backward compatibility) 





---

## <kbd>class</kbd> `SuccessState`
Test logic outcome - independent of snapshot management 





---

## <kbd>class</kbd> `SnapshotState`
Snapshot integrity outcome - independent of test logic 





---

## <kbd>class</kbd> `TwoDimensionalTestResult`
Two-dimensional test result separating logic success from snapshot management 




---

### <kbd>method</kbd> `can_auto_approve`

```python
can_auto_approve() → bool
```

Check if this result can be auto-approved without human review 

---

### <kbd>method</kbd> `is_success`

```python
is_success() → bool
```

Check if the test logic succeeded (regardless of snapshots) 

---

### <kbd>method</kbd> `requires_review`

```python
requires_review() → bool
```

Check if this result requires human review 

---

### <kbd>method</kbd> `to_legacy_result`

```python
to_legacy_result() → <enum 'TestResult'>
```

Convert to legacy single-dimensional result for backward compatibility 


---

## <kbd>class</kbd> `UserRequest`








---

## <kbd>class</kbd> `Metrics`
Stores the top level test metrics/results 

### <kbd>method</kbd> `__init__`

```python
__init__(took_ms)
```








---

### <kbd>method</kbd> `of_dir`

```python
of_dir(dir)
```





---

### <kbd>method</kbd> `of_file`

```python
of_file(path)
```





---

### <kbd>method</kbd> `to_dir`

```python
to_dir(dir)
```





---

### <kbd>method</kbd> `to_file`

```python
to_file(path)
```






---

## <kbd>class</kbd> `CaseReports`
This class manages the saved case specific metrics/results. 

Supports both legacy text format (cases.txt) and new JSON format (cases.json). The JSON format includes AI review results which are invalidated when tests rerun. 

### <kbd>method</kbd> `__init__`

```python
__init__(cases, ai_reviews=None)
```

Initialize CaseReports. 



**Args:**
 
 - <b>`cases`</b>:  List of (case_name, result, duration) tuples 
 - <b>`ai_reviews`</b>:  Optional dict mapping case_name to AIReviewResult 




---

### <kbd>method</kbd> `by_name`

```python
by_name(name)
```





---

### <kbd>method</kbd> `cases_to_done_and_todo`

```python
cases_to_done_and_todo(cases, config)
```





---

### <kbd>method</kbd> `failed`

```python
failed()
```





---

### <kbd>method</kbd> `failed_with_details`

```python
failed_with_details()
```

Return failed test cases with their result type and duration. 

---

### <kbd>method</kbd> `get_ai_review`

```python
get_ai_review(case_name)
```

Get AI review for a specific test case, if available. 

---

### <kbd>method</kbd> `make_case`

```python
make_case(case_name, res: TestResult, duration)
```





---

### <kbd>method</kbd> `of_dir`

```python
of_dir(out_dir)
```

Load case reports from directory. 

Prefers cases.ndjson (NDJSON) if it exists, falls back to cases.txt for backward compatibility. 

---

### <kbd>method</kbd> `of_file`

```python
of_file(file_name)
```





---

### <kbd>method</kbd> `of_jsonl_file`

```python
of_jsonl_file(file_name)
```

Load case reports from NDJSON file (newline-delimited JSON). 

---

### <kbd>method</kbd> `passed`

```python
passed()
```





---

### <kbd>method</kbd> `set_ai_review`

```python
set_ai_review(case_name, ai_review)
```

Set AI review for a specific test case. 



**Args:**
 
 - <b>`case_name`</b>:  Test case name 
 - <b>`ai_review`</b>:  AIReviewResult object or None to remove 

---

### <kbd>method</kbd> `to_dir`

```python
to_dir(out_dir)
```

Save case reports to directory (uses NDJSON format). 

---

### <kbd>method</kbd> `to_file`

```python
to_file(file)
```

Save to legacy text format (for backward compatibility). 

---

### <kbd>method</kbd> `to_jsonl_file`

```python
to_jsonl_file(file_name)
```

Save case reports to NDJSON file (newline-delimited JSON). 

---

### <kbd>method</kbd> `write_case`

```python
write_case(file_handle, case_name, res: TestResult, duration)
```





---

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
