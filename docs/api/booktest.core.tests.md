<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.core.tests`






---

## <kbd>class</kbd> `Tests`




### <kbd>method</kbd> `__init__`

```python
__init__(cases)
```








---

### <kbd>method</kbd> `all_method_dependencies`

```python
all_method_dependencies(method, selection, cache_out_dir=None)
```





---

### <kbd>method</kbd> `all_names`

```python
all_names()
```





---

### <kbd>method</kbd> `case_by_method`

```python
case_by_method(method)
```





---

### <kbd>method</kbd> `exec`

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

### <kbd>method</kbd> `exec_parsed`

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

### <kbd>method</kbd> `get_case`

```python
get_case(case_name)
```





---

### <kbd>method</kbd> `method_dependencies`

```python
method_dependencies(method, selection, cache_out_dir=None)
```





---

### <kbd>method</kbd> `method_resources`

```python
method_resources(method)
```





---

### <kbd>method</kbd> `selected_names`

```python
selected_names(selection, cache_out_dir=None)
```





---

### <kbd>method</kbd> `setup_parser`

```python
setup_parser(parser)
```





---

### <kbd>method</kbd> `test_result_exists`

```python
test_result_exists(out_dir, case_path)
```





---

### <kbd>method</kbd> `test_result_path`

```python
test_result_path(out_dir, case_path)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
