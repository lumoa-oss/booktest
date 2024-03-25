<!-- markdownlint-disable -->

<a href="../booktest/requests.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `requests.py`





---

<a href="../requests/py/threading_rlock#L180"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `threading_rlock`

```python
threading_rlock(timeout)
```






---

<a href="../booktest/requests.py#L312"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `snapshot_requests`

```python
snapshot_requests(lose_request_details=True, ignore_headers=True)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list 


---

## <kbd>class</kbd> `RequestKey`




<a href="../booktest/requests.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(json_object, ignore_headers=True)
```








---

<a href="../booktest/requests.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_properties`

```python
from_properties(url, method, headers, body, ignore_headers)
```





---

<a href="../booktest/requests.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_request`

```python
from_request(request: PreparedRequest, ignore_headers=True)
```





---

<a href="../booktest/requests.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_json_object`

```python
to_json_object(hide_details)
```





---

<a href="../booktest/requests.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `url`

```python
url()
```






---

## <kbd>class</kbd> `RequestSnapshot`




<a href="../booktest/requests.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(request: RequestKey, response: Response)
```








---

<a href="../booktest/requests.py#L105"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_json_object`

```python
from_json_object(json_object, ignore_headers=True)
```





---

<a href="../booktest/requests.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `hash`

```python
hash()
```





---

<a href="../booktest/requests.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `json_object`

```python
json_object(hide_details)
```





---

<a href="../booktest/requests.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `match`

```python
match(request: RequestKey)
```






---

## <kbd>class</kbd> `SnapshotAdapter`
A fake adapter than can return predefined responses. 

<a href="../booktest/requests.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(snapshots, capture_snapshots, ignore_headers)
```








---

<a href="../booktest/requests.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `send`

```python
send(request, **kwargs)
```






---

## <kbd>class</kbd> `SnapshotRequests`




<a href="../booktest/requests.py#L223"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(t: TestCaseRun, lose_request_details=True, ignore_headers=True)
```








---

<a href="../booktest/requests.py#L251"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start()
```

Start mocking requests.  



---

<a href="../booktest/requests.py#L281"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `stop`

```python
stop()
```

Stop mocking requests. 

This should have no impact if mocking has not been started. When nesting mockers, make sure to stop the innermost first. 

---

<a href="../booktest/requests.py#L299"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `t_snapshots`

```python
t_snapshots()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
