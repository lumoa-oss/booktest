<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.core.testbook`






---

## <kbd>class</kbd> `member_table`




### <kbd>method</kbd> `__init__`

```python
__init__()
```









---

## <kbd>class</kbd> `OrderedClass`








---

## <kbd>class</kbd> `TestBook`
Base class for test book instances 

### <kbd>method</kbd> `__init__`

```python
__init__(full_path=None, name=None)
```

if path is None, a default path is generated. If name is not None, the name is used as a part of the default path name. 

The full_path parameter is aimed for e.g. generating different test cases from the same class, while name is aimed for fixing badly generated names (e.g. caused by all caps abbreviations). 




---

### <kbd>method</kbd> `test_book_path`

```python
test_book_path()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
