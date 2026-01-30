<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.config.detection`




**Global Variables**
---------------
- **BOOKTEST_SETUP_MODULE**
- **BOOKTEST_SETUP_FILENAME**
- **PROCESS_SETUP_TEARDOWN**

---

## <kbd>function</kbd> `empty_setup_teardown`

```python
empty_setup_teardown()
```






---

## <kbd>function</kbd> `parse_booktest_setup_module`

```python
parse_booktest_setup_module(module)
```






---

## <kbd>function</kbd> `parse_booktest_setup`

```python
parse_booktest_setup(root, f)
```






---

## <kbd>function</kbd> `get_module_tests`

```python
get_module_tests(test_suite_name, module_name)
```






---

## <kbd>function</kbd> `get_file_tests`

```python
get_file_tests(root, f, selection)
```






---

## <kbd>function</kbd> `include_sys_path`

```python
include_sys_path(python_path: str)
```






---

## <kbd>function</kbd> `detect_setup`

```python
detect_setup(path)
```






---

## <kbd>function</kbd> `detect_module_setup`

```python
detect_module_setup(module_name)
```






---

## <kbd>function</kbd> `detect_tests`

```python
detect_tests(path, selection=None)
```

Detects tests in a file system path 


---

## <kbd>function</kbd> `detect_test_suite`

```python
detect_test_suite(path)
```






---

## <kbd>function</kbd> `detect_module_tests`

```python
detect_module_tests(module_name, selection=None)
```

Detects tests in a module. This is needed e.g. in pants, where original FS is not easily accessible  


---

## <kbd>function</kbd> `detect_module_test_suite`

```python
detect_module_test_suite(path, selection=None)
```






---

## <kbd>class</kbd> `BookTestSetup`




### <kbd>method</kbd> `__init__`

```python
__init__(setup_teardown=None)
```








---

### <kbd>method</kbd> `setup_teardown`

```python
setup_teardown()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
