<!-- markdownlint-disable -->

<a href="../booktest/tests.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `tests.py`






---

## <kbd>class</kbd> `Tests`




<a href="../booktest/tests.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(cases)
```








---

<a href="../booktest/tests.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `all_method_dependencies`

```python
all_method_dependencies(method, selection, cache_out_dir=None)
```





---

<a href="../booktest/tests.py#L79"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `all_names`

```python
all_names()
```





---

<a href="../booktest/tests.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `case_by_method`

```python
case_by_method(method)
```





---

<a href="../booktest/tests.py#L549"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `exec`

```python
exec(
    root_dir,
    args,
    cache=None,
    extra_default_config: dict = {},
    setup=None
) → int
```

:param root_dir: the directory containing books and .out directory :param args: a string containing command line arguments :param cache: in-memory cache. Can be e.g. dictionary {},  LruCache or NoCache. :return: returns an exit value. 0 for success, 1 for error 

---

<a href="../booktest/tests.py#L343"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `exec_parsed`

```python
exec_parsed(
    root_dir,
    parsed,
    cache=None,
    extra_default_config: dict = {},
    setup=None
) → int
```

:param root_dir:  the directory containing books and .out directory :param parsed: the object containing argparse parsed arguments :param cache: in-memory cache. Can be e.g. dictionary {},  LruCache or NoCache. :return: returns an exit value. 0 for success, 1 for error 

---

<a href="../booktest/tests.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_case`

```python
get_case(case_name)
```





---

<a href="../booktest/tests.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `method_dependencies`

```python
method_dependencies(method, selection, cache_out_dir=None)
```





---

<a href="../booktest/tests.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `method_resources`

```python
method_resources(method)
```





---

<a href="../booktest/tests.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `selected_names`

```python
selected_names(selection, cache_out_dir=None)
```





---

<a href="../booktest/tests.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `setup_parser`

```python
setup_parser(parser)
```





---

<a href="../booktest/tests.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `test_result_exists`

```python
test_result_exists(out_dir, case_path)
```





---

<a href="../booktest/tests.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `test_result_path`

```python
test_result_path(out_dir, case_path)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
