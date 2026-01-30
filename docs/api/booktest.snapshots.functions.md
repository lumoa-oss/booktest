<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.snapshots.functions`





---

## <kbd>function</kbd> `set_function`

```python
set_function(func, value)
```






---

## <kbd>function</kbd> `snapshot_functions`

```python
snapshot_functions(*snapshot_funcs)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list 


---

## <kbd>function</kbd> `mock_functions`

```python
mock_functions(mock_funcs)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list 


---

## <kbd>class</kbd> `FunctionCall`




### <kbd>method</kbd> `__init__`

```python
__init__(json_object)
```








---

### <kbd>method</kbd> `args`

```python
args()
```





---

### <kbd>method</kbd> `from_properties`

```python
from_properties(func, args, kwargs)
```





---

### <kbd>method</kbd> `func`

```python
func()
```





---

### <kbd>method</kbd> `kwargs`

```python
kwargs()
```





---

### <kbd>method</kbd> `to_json_object`

```python
to_json_object(hide_details)
```






---

## <kbd>class</kbd> `FunctionCallSnapshot`




### <kbd>method</kbd> `__init__`

```python
__init__(call, result)
```








---

### <kbd>method</kbd> `from_json_object`

```python
from_json_object(json_object)
```





---

### <kbd>method</kbd> `func`

```python
func()
```





---

### <kbd>method</kbd> `hash`

```python
hash()
```





---

### <kbd>method</kbd> `json_object`

```python
json_object()
```





---

### <kbd>method</kbd> `match`

```python
match(call: FunctionCall)
```






---

## <kbd>class</kbd> `FunctionSnapshotter`




### <kbd>method</kbd> `__init__`

```python
__init__(t: TestCaseRun, func)
```









---

## <kbd>class</kbd> `SnapshotFunctions`




### <kbd>method</kbd> `__init__`

```python
__init__(t: TestCaseRun, snapshot_funcs: list = None)
```








---

### <kbd>method</kbd> `snapshot`

```python
snapshot(func, *args, **kwargs)
```





---

### <kbd>method</kbd> `start`

```python
start()
```





---

### <kbd>method</kbd> `stop`

```python
stop()
```





---

### <kbd>method</kbd> `t_snapshots`

```python
t_snapshots()
```

Report snapshot usage to the system instead of printing to test results. 


---

## <kbd>class</kbd> `MockFunctions`




### <kbd>method</kbd> `__init__`

```python
__init__(mock_funcs: dict = None)
```








---

### <kbd>method</kbd> `start`

```python
start()
```





---

### <kbd>method</kbd> `stop`

```python
stop()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
