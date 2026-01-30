<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.reporting.review`




**Global Variables**
---------------
- **BOOK_TEST_PREFIX**

---

## <kbd>function</kbd> `perform_ai_review`

```python
perform_ai_review(
    exp_file_name: str,
    out_file_name: str,
    case_name: str
) → Optional[ForwardRef('AIReviewResult')]
```

Perform AI review of test differences. 



**Args:**
 
 - <b>`exp_file_name`</b>:  Path to expected output file 
 - <b>`out_file_name`</b>:  Path to actual output file 
 - <b>`case_name`</b>:  Test case name 



**Returns:**
 AIReviewResult or None if review fails 


---

## <kbd>function</kbd> `print_ai_review_result`

```python
print_ai_review_result(result: 'AIReviewResult', verbose: bool = False)
```

Print AI review result to console. 



**Args:**
 
 - <b>`result`</b>:  The AI review result to print 
 - <b>`verbose`</b>:  Whether to print full details or summary 


---

## <kbd>function</kbd> `run_tool`

```python
run_tool(config, tool, args)
```

Run a tool used in reviews  


---

## <kbd>function</kbd> `interact`

```python
interact(
    exp_dir,
    out_dir,
    case_name,
    test_result,
    config,
    existing_ai_result=None
)
```






---

## <kbd>function</kbd> `freeze_case`

```python
freeze_case(exp_dir, out_dir, case_name)
```






---

## <kbd>function</kbd> `case_review`

```python
case_review(exp_dir, out_dir, case_name, test_result, config)
```






---

## <kbd>function</kbd> `start_report`

```python
start_report(printer)
```






---

## <kbd>function</kbd> `report_case_begin`

```python
report_case_begin(printer, case_name, title, verbose)
```






---

## <kbd>function</kbd> `report_case_result`

```python
report_case_result(
    printer,
    case_name,
    result,
    took_ms,
    verbose,
    out_dir=None,
    case_reports=None
)
```






---

## <kbd>function</kbd> `maybe_print_logs`

```python
maybe_print_logs(printer, config, out_dir, case_name)
```






---

## <kbd>function</kbd> `report_case`

```python
report_case(printer, exp_dir, out_dir, case_name, result, took_ms, config)
```






---

## <kbd>function</kbd> `end_report`

```python
end_report(printer, failed, tests, took_ms)
```

Print end of test run summary. 



**Args:**
 
 - <b>`printer`</b>:  Function to print output 
 - <b>`failed`</b>:  List of failed test names OR list of (name, result, duration) tuples 
 - <b>`tests`</b>:  Total number of tests 
 - <b>`took_ms`</b>:  Total time taken in milliseconds 


---

## <kbd>function</kbd> `create_index`

```python
create_index(dir, case_names)
```






---

## <kbd>function</kbd> `review`

```python
review(exp_dir, out_dir, config, passed, cases=None)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
