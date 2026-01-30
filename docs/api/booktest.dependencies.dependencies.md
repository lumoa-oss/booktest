<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.dependencies.dependencies`





---

## <kbd>function</kbd> `port_range`

```python
port_range(begin: int, end: int)
```






---

## <kbd>function</kbd> `port`

```python
port(value: int)
```

Generates a resource for given port. A special identifier is generated in order to not mix the port with other resource integers 


---

## <kbd>function</kbd> `get_decorated_attr`

```python
get_decorated_attr(method, attr)
```






---

## <kbd>function</kbd> `remove_decoration`

```python
remove_decoration(method)
```






---

## <kbd>function</kbd> `bind_dependent_method_if_unbound`

```python
bind_dependent_method_if_unbound(method, dependency)
```






---

## <kbd>function</kbd> `release_dependencies`

```python
release_dependencies(name, dependencies, resolved, allocations)
```

Releases all dependencies 


---

## <kbd>function</kbd> `call_test`

```python
call_test(method_caller, dependencies, func, case, kwargs)
```






---

## <kbd>function</kbd> `call_class_method_test`

```python
call_class_method_test(dependencies, func, case, kwargs)
```






---

## <kbd>function</kbd> `call_function_test`

```python
call_function_test(dependencies, func, case, kwargs)
```






---

## <kbd>function</kbd> `depends_on`

```python
depends_on(*dependencies)
```

This method depends on a method on this object. 


---

## <kbd>class</kbd> `ResourceAllocator`
Allocators are used to allocate resources for tests. 

The big theme with python testing is that in parallel runs, resources need to preallocated in main thread, before these resource allocations get passed to the actual test cases. 




---

### <kbd>method</kbd> `allocate`

```python
allocate(
    allocation_id: <built-in function any>,
    allocations: set[tuple],
    preallocations: dict[any, any]
) → (<built-in function any>, set[tuple], dict[any, any])
```





---

### <kbd>method</kbd> `deallocate`

```python
deallocate(allocations: set[tuple], allocation) → set[tuple]
```






---

## <kbd>class</kbd> `SingleResourceAllocator`
Allocators are used to allocate resources for tests. 

The big theme with python testing is that in parallel runs, resources need to preallocated in main thread, before these resource allocations get passed to the actual test cases. 


---

#### <kbd>property</kbd> identity

The identity of the resource. This needs to be something that can be stored in a set 



---

### <kbd>method</kbd> `allocate`

```python
allocate(
    allocation_id: <built-in function any>,
    allocations: set[tuple],
    preallocations: dict[any, any]
) → (<built-in function any>, set[any, any], dict[any, (<built-in function any>, <built-in function any>)])
```

Allocates a resource and returns it. If resource cannot be allocated, returns None. 

allocation_id - unique identifier for this allocation, used for preallocations allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these preallocated resources - is a map from allocation_name to resource. use these to guide allocation 

---

### <kbd>method</kbd> `deallocate`

```python
deallocate(allocations: set[tuple], allocation) → set[tuple]
```

Deallocates a resource and returns it. If resource cannot be deallocated, returns None. 

allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these allocation - is the allocation to deallocate 

---

### <kbd>method</kbd> `do_allocate`

```python
do_allocate(allocations: set[tuple]) → Optional[<built-in function any>]
```

Allocates a resource and returns it. If resource cannot be allocated, returns None. 

allocation_name - unique name for this allocation, that for preallocations allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these preallocated resources - is a map from allocation_name to resource. use these to guide allocation 


---

## <kbd>class</kbd> `Resource`
Represents an exclusive resources, which must not be shared simultaneously by several parallel tests 

Such a resource can be a specific port, file system resource, some global state or excessive use of RAM or GPU, that prohibits parallel run. 

### <kbd>method</kbd> `__init__`

```python
__init__(value, identity=None)
```






---

#### <kbd>property</kbd> identity

The identity of the resource 



---

### <kbd>method</kbd> `allocate`

```python
allocate(
    allocation_id: <built-in function any>,
    allocations: set[tuple],
    preallocations: dict[any, any]
) → (<built-in function any>, set[any, any], dict[any, (<built-in function any>, <built-in function any>)])
```

Allocates a resource and returns it. If resource cannot be allocated, returns None. 

allocation_id - unique identifier for this allocation, used for preallocations allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these preallocated resources - is a map from allocation_name to resource. use these to guide allocation 

---

### <kbd>method</kbd> `deallocate`

```python
deallocate(allocations: set[tuple], allocation) → set[tuple]
```

Deallocates a resource and returns it. If resource cannot be deallocated, returns None. 

allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these allocation - is the allocation to deallocate 

---

### <kbd>method</kbd> `do_allocate`

```python
do_allocate(allocations: set[tuple]) → <built-in function any>
```

Allocates a resource and returns it :return: 


---

## <kbd>class</kbd> `Pool`
A pool of resource like ports, that must not be used simultaneously. 

### <kbd>method</kbd> `__init__`

```python
__init__(identity, resources)
```






---

#### <kbd>property</kbd> identity

The identity of the resource 



---

### <kbd>method</kbd> `allocate`

```python
allocate(
    allocation_id: <built-in function any>,
    allocations: set[tuple],
    preallocations: dict[any, any]
) → (<built-in function any>, set[any, any], dict[any, (<built-in function any>, <built-in function any>)])
```

Allocates a resource and returns it. If resource cannot be allocated, returns None. 

allocation_id - unique identifier for this allocation, used for preallocations allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these preallocated resources - is a map from allocation_name to resource. use these to guide allocation 

---

### <kbd>method</kbd> `deallocate`

```python
deallocate(allocations: set[tuple], allocation) → set[tuple]
```

Deallocates a resource and returns it. If resource cannot be deallocated, returns None. 

allocations - is a set consisting of (identity, resource) tuples. DO NOT double allocate these allocation - is the allocation to deallocate 

---

### <kbd>method</kbd> `do_allocate`

```python
do_allocate(allocations: set[tuple]) → <built-in function any>
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
