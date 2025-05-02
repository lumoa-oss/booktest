<!-- markdownlint-disable -->

<a href="../booktest/functions.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `functions.py`





---

<a href="../booktest/functions.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `set_function`

```python
set_function(func, value)
```






---

<a href="../booktest/functions.py#L238"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `snapshot_functions`

```python
snapshot_functions(*snapshot_funcs)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list 


---

<a href="../booktest/functions.py#L295"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `mock_functions`

```python
mock_functions(mock_funcs)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list 


---

## <kbd>class</kbd> `FunctionCall`




<a href="../booktest/functions.py#L18"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(json_object)
```








---

<a href="../booktest/functions.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `args`

```python
args()
```





---

<a href="../booktest/functions.py#L46"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_properties`

```python
from_properties(func, args, kwargs)
```





---

<a href="../booktest/functions.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `func`

```python
func()
```





---

<a href="../booktest/functions.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `kwargs`

```python
kwargs()
```





---

<a href="../booktest/functions.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_json_object`

```python
to_json_object(hide_details)
```






---

## <kbd>class</kbd> `FunctionCallSnapshot`




<a href="../booktest/functions.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(call, result)
```








---

<a href="../booktest/functions.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_json_object`

```python
from_json_object(json_object)
```





---

<a href="../booktest/functions.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `func`

```python
func()
```





---

<a href="../booktest/functions.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `hash`

```python
hash()
```





---

<a href="../booktest/functions.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `json_object`

```python
json_object()
```





---

<a href="../booktest/functions.py#L67"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `match`

```python
match(call: FunctionCall)
```






---

## <kbd>class</kbd> `FunctionSnapshotter`




<a href="../booktest/functions.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(t: TestCaseRun, func)
```









---

## <kbd>class</kbd> `MockFunctions`




<a href="../booktest/functions.py#L261"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(mock_funcs: dict = None)
```








---

<a href="../booktest/functions.py#L268"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start()
```





---

<a href="../booktest/functions.py#L280"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `stop`

```python
stop()
```






---

## <kbd>class</kbd> `SnapshotFunctions`




<a href="../booktest/functions.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(t: TestCaseRun, snapshot_funcs: list = None)
```








---

<a href="../booktest/functions.py#L137"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `snapshot`

```python
snapshot(func, *args, **kwargs)
```





---

<a href="../booktest/functions.py#L161"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start()
```





---

<a href="../booktest/functions.py#L188"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `stop`

```python
stop()
```





---

<a href="../booktest/functions.py#L206"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `t_snapshots`

```python
t_snapshots()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
