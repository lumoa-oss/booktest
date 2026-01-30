<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.utils.utils`





---

## <kbd>function</kbd> `accept_all`

```python
accept_all(_)
```






---

## <kbd>function</kbd> `path_to_module_resource`

```python
path_to_module_resource(path: str)
```

DEPRECATED: Old API that doesn't handle dots in filenames. Use open_file_or_resource() with files() API instead. 


---

## <kbd>function</kbd> `open_file_or_resource`

```python
open_file_or_resource(path: str, is_resource: bool)
```

Open a file or resource for reading. 

Uses modern importlib.resources.files() API which handles paths with dots correctly. Assumes first path component is the root Python package (e.g., 'books'). 



**Args:**
 
 - <b>`path`</b>:  Path like 'books/test/test_hello.py/test_hello.md' 
 - <b>`is_resource`</b>:  Whether to use Pants resource system 



**Returns:**
 File-like object opened for text reading 


---

## <kbd>function</kbd> `file_or_resource_exists`

```python
file_or_resource_exists(path: str, is_resource: bool)
```

Check if a file or resource exists. 

Uses modern importlib.resources.files() API which handles paths with dots correctly. Assumes first path component is the root Python package (e.g., 'books'). 



**Args:**
 
 - <b>`path`</b>:  Path like 'books/test/test_hello.py/test_hello.md' 
 - <b>`is_resource`</b>:  Whether to use Pants resource system 



**Returns:**
 True if the file/resource exists 


---

## <kbd>function</kbd> `setup_teardown`

```python
setup_teardown(setup_teardown_generator)
```






---

## <kbd>function</kbd> `combine_decorators`

```python
combine_decorators(*decorators)
```






---

## <kbd>class</kbd> `SetupTeardown`




### <kbd>method</kbd> `__init__`

```python
__init__(setup_teardown_generator)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
