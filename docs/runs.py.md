<!-- markdownlint-disable -->

<a href="../booktest/runs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `runs.py`





---

<a href="../booktest/runs.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `batch_dir`

```python
batch_dir(out_dir: str)
```






---

<a href="../booktest/runs.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_batch_dir`

```python
prepare_batch_dir(out_dir: str)
```






---

<a href="../booktest/runs.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `case_batch_dir_and_report_file`

```python
case_batch_dir_and_report_file(batches_dir, name)
```






---

<a href="../booktest/runs.py#L285"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/runs.py#L420"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/runs.py#L442"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

## <kbd>class</kbd> `ParallelRunner`




<a href="../booktest/runs.py#L109"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

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

<a href="../booktest/runs.py#L197"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `abort`

```python
abort()
```





---

<a href="../booktest/runs.py#L240"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `batch_dirs`

```python
batch_dirs()
```





---

<a href="../booktest/runs.py#L250"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `done_reports`

```python
done_reports()
```





---

<a href="../booktest/runs.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `has_next`

```python
has_next()
```





---

<a href="../booktest/runs.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `next_report`

```python
next_report()
```





---

<a href="../booktest/runs.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plan`

```python
plan(todo)
```





---

<a href="../booktest/runs.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `thread_function`

```python
thread_function()
```






---

## <kbd>class</kbd> `RunBatch`




<a href="../booktest/runs.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(exp_dir: str, out_dir: str, tests, config: dict, setup: BookTestSetup)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
