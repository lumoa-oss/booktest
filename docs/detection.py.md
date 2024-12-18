<!-- markdownlint-disable -->

<a href="../booktest/detection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `detection.py`




**Global Variables**
---------------
- **BOOKTEST_SETUP_MODULE**
- **BOOKTEST_SETUP_FILENAME**
- **PROCESS_SETUP_TEARDOWN**

---

<a href="../booktest/detection.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `empty_setup_teardown`

```python
empty_setup_teardown()
```






---

<a href="../booktest/detection.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_booktest_setup_module`

```python
parse_booktest_setup_module(module)
```






---

<a href="../booktest/detection.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_booktest_setup`

```python
parse_booktest_setup(root, f)
```






---

<a href="../booktest/detection.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_module_tests`

```python
get_module_tests(test_suite_name, module_name)
```






---

<a href="../booktest/detection.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_file_tests`

```python
get_file_tests(root, f)
```






---

<a href="../booktest/detection.py#L108"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `include_sys_path`

```python
include_sys_path(python_path: str)
```






---

<a href="../booktest/detection.py#L114"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_setup`

```python
detect_setup(path)
```






---

<a href="../booktest/detection.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_module_setup`

```python
detect_module_setup(module_name)
```






---

<a href="../booktest/detection.py#L139"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_tests`

```python
detect_tests(path)
```

Detects tests in a file system path 


---

<a href="../booktest/detection.py#L157"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_test_suite`

```python
detect_test_suite(path)
```






---

<a href="../booktest/detection.py#L163"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_module_tests`

```python
detect_module_tests(module_name)
```

Detects tests in a module. This is needed e.g. in pants, where original FS is not easily accessible  


---

<a href="../booktest/detection.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_module_test_suite`

```python
detect_module_test_suite(path)
```






---

## <kbd>class</kbd> `BookTestSetup`




<a href="../booktest/detection.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(setup_teardown=None)
```








---

<a href="../booktest/detection.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `setup_teardown`

```python
setup_teardown()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
