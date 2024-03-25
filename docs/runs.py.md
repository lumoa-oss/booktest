<!-- markdownlint-disable -->

<a href="../booktest/runs.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `runs.py`





---

<a href="../booktest/runs.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `case_batch_dir_and_report_file`

```python
case_batch_dir_and_report_file(batches_dir, name)
```






---

<a href="../booktest/runs.py#L246"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parallel_run_tests`

```python
parallel_run_tests(exp_dir, out_dir, tests, cases: list, config: dict)
```






---

<a href="../booktest/runs.py#L337"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run_tests`

```python
run_tests(exp_dir, out_dir, tests, cases: list, config: dict, cache)
```






---

## <kbd>class</kbd> `ParallelRunner`




<a href="../booktest/runs.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    exp_dir,
    out_dir,
    tests,
    cases: list,
    config: dict,
    reports: CaseReports
)
```








---

<a href="../booktest/runs.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `abort`

```python
abort()
```





---

<a href="../booktest/runs.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `batch_dirs`

```python
batch_dirs()
```





---

<a href="../booktest/runs.py#L211"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `has_next`

```python
has_next()
```





---

<a href="../booktest/runs.py#L215"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `next_report`

```python
next_report()
```





---

<a href="../booktest/runs.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `plan`

```python
plan(todo)
```





---

<a href="../booktest/runs.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `thread_function`

```python
thread_function()
```






---

## <kbd>class</kbd> `RunBatch`




<a href="../booktest/runs.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(exp_dir: str, out_dir: str, tests, config: dict)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
