<!-- markdownlint-disable -->

<a href="../booktest/testrun.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `testrun.py`





---

<a href="../booktest/testrun.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `method_identity`

```python
method_identity(method)
```






---

<a href="../booktest/testrun.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `match_method`

```python
match_method(matcher, method)
```






---

## <kbd>class</kbd> `TestRun`
Runs a selection of test cases from the test-object 

<a href="../booktest/testrun.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    exp_dir,
    out_dir,
    report_dir,
    tests,
    selected_cases,
    config,
    cache,
    output=None,
    allocations=None,
    preallocations=None
)
```








---

<a href="../booktest/testrun.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_test_result`

```python
get_test_result(case, method)
```





---

<a href="../booktest/testrun.py#L118"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `print`

```python
print(*args, sep=' ', end='\n')
```





---

<a href="../booktest/testrun.py#L202"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `run`

```python
run()
```





---

<a href="../booktest/testrun.py#L121"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `run_async`

```python
run_async()
```





---

<a href="../booktest/testrun.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `run_case`

```python
run_case(
    case_path,
    case,
    title=None
) → (<enum 'TestResult'>, <enum 'UserRequest'>, <class 'float'>)
```





---

<a href="../booktest/testrun.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `save_test_result`

```python
save_test_result(case_path, result)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
