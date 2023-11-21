<!-- markdownlint-disable -->

<a href="../booktest/reports.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reports.py`





---

<a href="../booktest/reports.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `test_result_to_exit_code`

```python
test_result_to_exit_code(test_result)
```






---

<a href="../booktest/reports.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `write_lines`

```python
write_lines(path, file, lines)
```






---

<a href="../booktest/reports.py#L44"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `read_lines`

```python
read_lines(path, filename=None)
```






---

## <kbd>class</kbd> `CaseReports`
This class manages the saved case specific metrics/results 

<a href="../booktest/reports.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(cases)
```








---

<a href="../booktest/reports.py#L104"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `failed`

```python
failed()
```





---

<a href="../booktest/reports.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `of_file`

```python
of_file(file_name)
```





---

<a href="../booktest/reports.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `passed`

```python
passed()
```





---

<a href="../booktest/reports.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_file`

```python
to_file(file)
```





---

<a href="../booktest/reports.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `write_case`

```python
write_case(file_handle, case_name, res: TestResult, duration)
```






---

## <kbd>class</kbd> `Metrics`
Stores the top level test metrics/results 

<a href="../booktest/reports.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(took_ms)
```








---

<a href="../booktest/reports.py#L88"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `of_dir`

```python
of_dir(dir)
```





---

<a href="../booktest/reports.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `of_file`

```python
of_file(path)
```





---

<a href="../booktest/reports.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_dir`

```python
to_dir(dir)
```





---

<a href="../booktest/reports.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_file`

```python
to_file(path)
```






---

## <kbd>class</kbd> `TestResult`








---

## <kbd>class</kbd> `UserRequest`










---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
