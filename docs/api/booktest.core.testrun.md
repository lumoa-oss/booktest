<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.core.testrun`





---

## <kbd>function</kbd> `method_identity`

```python
method_identity(method)
```






---

## <kbd>function</kbd> `match_method`

```python
match_method(matcher, method)
```






---

## <kbd>class</kbd> `TestRun`
Runs a selection of test cases from the test-object 

### <kbd>method</kbd> `__init__`

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
    preallocations=None,
    batch_dir=None
)
```








---

### <kbd>method</kbd> `get_test_result`

```python
get_test_result(case, method)
```





---

### <kbd>method</kbd> `print`

```python
print(*args, sep=' ', end='\n')
```





---

### <kbd>method</kbd> `run`

```python
run()
```





---

### <kbd>method</kbd> `run_async`

```python
run_async()
```





---

### <kbd>method</kbd> `run_case`

```python
run_case(
    case_path,
    case,
    title=None
) → (<enum 'TestResult'>, <enum 'UserRequest'>, <class 'float'>)
```





---

### <kbd>method</kbd> `save_test_result`

```python
save_test_result(case_path, result)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
