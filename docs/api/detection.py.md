<!-- markdownlint-disable -->

<a href="../booktest/detection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `detection.py`




**Global Variables**
---------------
- **BOOKTEST_SETUP_MODULE**
- **BOOKTEST_SETUP_FILENAME**
- **PROCESS_SETUP_TEARDOWN**

---

<a href="../booktest/detection.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `empty_setup_teardown`

```python
empty_setup_teardown()
```






---

<a href="../booktest/detection.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_booktest_setup_module`

```python
parse_booktest_setup_module(module)
```






---

<a href="../booktest/detection.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `parse_booktest_setup`

```python
parse_booktest_setup(root, f)
```






---

<a href="../booktest/detection.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_module_tests`

```python
get_module_tests(test_suite_name, module_name)
```






---

<a href="../booktest/detection.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_file_tests`

```python
get_file_tests(root, f, selection)
```






---

<a href="../booktest/detection.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `include_sys_path`

```python
include_sys_path(python_path: str)
```






---

<a href="../booktest/detection.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_setup`

```python
detect_setup(path)
```






---

<a href="../booktest/detection.py#L129"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_module_setup`

```python
detect_module_setup(module_name)
```






---

<a href="../booktest/detection.py#L145"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_tests`

```python
detect_tests(path, selection=None)
```

Detects tests in a file system path 


---

<a href="../booktest/detection.py#L158"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_test_suite`

```python
detect_test_suite(path)
```






---

<a href="../booktest/detection.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_module_tests`

```python
detect_module_tests(module_name, selection=None)
```

Detects tests in a module. This is needed e.g. in pants, where original FS is not easily accessible  


---

<a href="../booktest/detection.py#L184"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `detect_module_test_suite`

```python
detect_module_test_suite(path, selection=None)
```






---

## <kbd>class</kbd> `BookTestSetup`




<a href="../booktest/detection.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(setup_teardown=None)
```








---

<a href="../booktest/detection.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `setup_teardown`

```python
setup_teardown()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
