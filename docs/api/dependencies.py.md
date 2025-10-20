<!-- markdownlint-disable -->

<a href="../booktest/dependencies.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `dependencies.py`





---

<a href="../booktest/dependencies.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `port_range`

```python
port_range(begin: int, end: int)
```






---

<a href="../booktest/dependencies.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `port`

```python
port(value: int)
```

Generates a resource for given port. A special identifier is generated in order to not mix the port with other resource integers 


---

<a href="../booktest/dependencies.py#L145"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `get_decorated_attr`

```python
get_decorated_attr(method, attr)
```






---

<a href="../booktest/dependencies.py#L155"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `remove_decoration`

```python
remove_decoration(method)
```






---

<a href="../booktest/dependencies.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `bind_dependent_method_if_unbound`

```python
bind_dependent_method_if_unbound(method, dependency)
```






---

<a href="../booktest/dependencies.py#L170"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `release_dependencies`

```python
release_dependencies(dependencies, resolved, allocations)
```

Releases all dependencies 


---

<a href="../booktest/dependencies.py#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `call_class_method_test`

```python
call_class_method_test(dependencies, func, case, kwargs)
```






---

<a href="../booktest/dependencies.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `call_function_test`

```python
call_function_test(dependencies, func, case, kwargs)
```






---

<a href="../booktest/dependencies.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `depends_on`

```python
depends_on(*dependencies)
```

This method depends on a method on this object. 


---

## <kbd>class</kbd> `Allocator`
Allocators are used to allocate resources for tests. 

The big theme with python testing is that in parallel runs, resources need to preallocated in main thread, before these resource allocations get passed to the actual test cases. 


---

#### <kbd>property</kbd> identity

The identity of the resource. This needs to be something that can be stored in a set 



---

<a href="../booktest/dependencies.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `allocate`

```python
allocate(
    allocations: set[tuple],
    preallocations: dict[any, any]
) → Optional[<built-in function any>]
```

Allocates a resource and returns it. If resource cannot be allocated, returns None. 

allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these preallocated resources - is a map from identity to resource. use these to guide allocation 


---

## <kbd>class</kbd> `Pool`
A pool of resource like ports, that must not be used simultaneously. 

<a href="../booktest/dependencies.py#L111"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(identity, resources)
```






---

#### <kbd>property</kbd> identity

The identity of the resource 



---

<a href="../booktest/dependencies.py#L122"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `allocate`

```python
allocate(
    allocations: set[tuple],
    preallocations: dict[any, any]
) → <built-in function any>
```






---

## <kbd>class</kbd> `Resource`
Represents an exclusive resources, which must not be shared simultaneously by several parallel tests 

Such a resource can be a specific port, file system resource, some global state or excessive use of RAM or GPU, that prohibits parallel run. 

<a href="../booktest/dependencies.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(value, identity=None)
```






---

#### <kbd>property</kbd> identity

The identity of the resource 



---

<a href="../booktest/dependencies.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `allocate`

```python
allocate(
    allocations: set[tuple],
    preallocations: dict[any, any]
) → <built-in function any>
```

Allocates a resource and returns it :return: 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
