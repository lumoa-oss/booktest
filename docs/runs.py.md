<!-- markdownlint-disable -->

<a href="../booktest/runs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `runs.py`




**Global Variables**
---------------
- **DEFAULT_TIMEOUT**

---

<a href="../booktest/runs.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `batch_dir`

```python
batch_dir(out_dir: str)
```






---

<a href="../booktest/runs.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `prepare_batch_dir`

```python
prepare_batch_dir(out_dir: str)
```






---

<a href="../booktest/runs.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `case_batch_dir_and_report_file`

```python
case_batch_dir_and_report_file(batches_dir, name)
```






---

<a href="../booktest/runs.py#L382"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/runs.py#L517"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/runs.py#L539"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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




<a href="../booktest/runs.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/runs.py#L239"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `abort`

```python
abort()
```





---

<a href="../booktest/runs.py#L334"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `batch_dirs`

```python
batch_dirs()
```





---

<a href="../booktest/runs.py#L344"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `done_reports`

```python
done_reports()
```





---

<a href="../booktest/runs.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `has_next`

```python
has_next()
```





---

<a href="../booktest/runs.py#L243"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `log`

```python
log(message)
```





---

<a href="../booktest/runs.py#L348"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `next_report`

```python
next_report()
```





---

<a href="../booktest/runs.py#L207"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plan`

```python
plan(todo)
```





---

<a href="../booktest/runs.py#L248"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `thread_function`

```python
thread_function()
```






---

## <kbd>class</kbd> `RunBatch`




<a href="../booktest/runs.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(exp_dir: str, out_dir: str, tests, config: dict, setup: BookTestSetup)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
