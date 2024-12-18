<!-- markdownlint-disable -->

<a href="../booktest/dependencies.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dependencies.py`





---

<a href="../booktest/dependencies.py#L30"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `port`

```python
port(value: int)
```

Generates a resource for given port. A special identifier is generated in order to not mix the port with other resource integers 


---

<a href="../booktest/dependencies.py#L39"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_decorated_attr`

```python
get_decorated_attr(method, attr)
```






---

<a href="../booktest/dependencies.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `remove_decoration`

```python
remove_decoration(method)
```






---

<a href="../booktest/dependencies.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bind_dependent_method_if_unbound`

```python
bind_dependent_method_if_unbound(method, dependency)
```






---

<a href="../booktest/dependencies.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `call_class_method_test`

```python
call_class_method_test(dependencies, func, case, kwargs)
```






---

<a href="../booktest/dependencies.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `call_function_test`

```python
call_function_test(methods, func, case, kwargs)
```






---

<a href="../booktest/dependencies.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `depends_on`

```python
depends_on(*dependencies)
```

This method depends on a method on this object. 


---

## <kbd>class</kbd> `Resource`
Represents an exclusive resources, which must not be shared simultaneously by several parallel tests 

Such a resource can be a specific port, file system resource, some global state or excessive use of RAM or GPU, that prohibits parallel run. 

<a href="../booktest/dependencies.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(value, identifier=None)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
