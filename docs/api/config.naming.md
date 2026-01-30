<!-- markdownlint-disable -->

<a href="../../booktest/config/naming.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `config.naming`





---

<a href="../../booktest/config/naming.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `camel_case_to_snake_case`

```python
camel_case_to_snake_case(name)
```






---

<a href="../../booktest/config/naming.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_test_postfix`

```python
clean_test_postfix(name)
```






---

<a href="../../booktest/config/naming.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_class_name`

```python
clean_class_name(name: str)
```






---

<a href="../../booktest/config/naming.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `clean_method_name`

```python
clean_method_name(name: str)
```






---

<a href="../../booktest/config/naming.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `class_to_test_path`

```python
class_to_test_path(clazz)
```






---

<a href="../../booktest/config/naming.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `class_to_pytest_name`

```python
class_to_pytest_name(clazz)
```

Convert a test class to pytest-style name. 



**Example:**
  Module: test.examples.foo_test  Class: FooTestBook  Result: test/examples/foo_test.py::FooTestBook 


---

<a href="../../booktest/config/naming.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `method_to_pytest_name`

```python
method_to_pytest_name(clazz, method_name: str)
```

Convert a test method to pytest-style name. 



**Example:**
  Module: test.examples.foo_test  Class: FooTestBook  Method: test_bar  Result: test/examples/foo_test.py::FooTestBook::test_bar 


---

<a href="../../booktest/config/naming.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `function_to_pytest_name`

```python
function_to_pytest_name(module_name: str, function_name: str)
```

Convert a standalone test function to pytest-style name. 



**Example:**
  Module: test.examples.simple_test  Function: test_example  Result: test/examples/simple_test.py::test_example 


---

<a href="../../booktest/config/naming.py#L120"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `to_filesystem_path`

```python
to_filesystem_path(pytest_name: str) → str
```

Convert pytest-style name to safe filesystem path. 

This is the internal representation used for file operations. Replaces :: with / to create a valid filesystem path. 



**Example:**
  Input:  test/foo_test.py::FooTestBook::test_bar  Output: test/foo_test.py/FooTestBook/test_bar 

 Input:  test/simple_test.py::test_example  Output: test/simple_test.py/test_example 


---

<a href="../../booktest/config/naming.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `from_filesystem_path`

```python
from_filesystem_path(fs_path: str) → str
```

Convert filesystem path back to pytest-style name. 

Uses heuristic: if path contains '.py/', convert to '.py::' Otherwise returns as-is for backwards compatibility with old format. 



**Example:**
  Input:  test/foo_test.py/FooTestBook/test_bar  Output: test/foo_test.py::FooTestBook::test_bar 

 Input:  test/foo/bar (old format)  Output: test/foo/bar (unchanged) 


---

<a href="../../booktest/config/naming.py#L165"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_pytest_name`

```python
is_pytest_name(name: str) → bool
```

Check if a name is in pytest format (contains ::). 



**Example:**
  is_pytest_name("test/foo_test.py::test_bar") → True  is_pytest_name("test/foo/bar") → False 


---

<a href="../../booktest/config/naming.py#L176"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `normalize_test_name`

```python
normalize_test_name(name: str) → str
```

Normalize test name to internal filesystem format. 

Accepts both pytest format and legacy format. Returns filesystem-safe path for internal use. 



**Example:**
  Input:  test/foo_test.py::test_bar (pytest format)  Output: test/foo_test.py/test_bar (filesystem) 

 Input:  test/foo/bar (legacy format)  Output: test/foo/bar (unchanged) 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
