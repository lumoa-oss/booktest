<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.core.runs`




**Global Variables**
---------------
- **DEFAULT_TIMEOUT**

---

## <kbd>function</kbd> `batch_dir`

```python
batch_dir(out_dir: str)
```






---

## <kbd>function</kbd> `prepare_batch_dir`

```python
prepare_batch_dir(out_dir: str)
```






---

## <kbd>function</kbd> `case_batch_dir_and_report_file`

```python
case_batch_dir_and_report_file(batches_dir, name)
```






---

## <kbd>function</kbd> `parallel_run_tests`

```python
parallel_run_tests(
    exp_dir,
    out_dir,
    tests,
    cases: list,
    config: dict,
    setup: BookTestSetup
)
```






---

## <kbd>function</kbd> `run_tests`

```python
run_tests(
    exp_dir,
    out_dir,
    tests,
    cases: list,
    config: dict,
    cache,
    setup: BookTestSetup
)
```






---

## <kbd>function</kbd> `run_tests_async`

```python
run_tests_async(
    exp_dir,
    out_dir,
    tests,
    cases: list,
    config: dict,
    cache,
    setup: BookTestSetup
)
```






---

## <kbd>class</kbd> `RunBatch`




### <kbd>method</kbd> `__init__`

```python
__init__(exp_dir: str, out_dir: str, tests, config: dict, setup: BookTestSetup)
```









---

## <kbd>class</kbd> `ParallelRunner`




### <kbd>method</kbd> `__init__`

```python
__init__(
    exp_dir,
    out_dir,
    tests,
    cases: list,
    config: dict,
    setup,
    reports: CaseReports
)
```








---

### <kbd>method</kbd> `abort`

```python
abort()
```





---

### <kbd>method</kbd> `batch_dirs`

```python
batch_dirs()
```





---

### <kbd>method</kbd> `done_reports`

```python
done_reports()
```





---

### <kbd>method</kbd> `has_next`

```python
has_next()
```





---

### <kbd>method</kbd> `log`

```python
log(message)
```





---

### <kbd>method</kbd> `next_report`

```python
next_report()
```





---

### <kbd>method</kbd> `plan`

```python
plan(todo, plan_target)
```





---

### <kbd>method</kbd> `thread_function`

```python
thread_function()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
