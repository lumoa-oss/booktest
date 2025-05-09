<!-- markdownlint-disable -->

<a href="../booktest/requests.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `requests.py`





---

<a href="../booktest/requests.py#L22"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `json_to_sha1`

```python
json_to_sha1(json_object)
```






---

<a href="../booktest/requests.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `default_encode_body`

```python
default_encode_body(body, _url, _method)
```






---

<a href="../requests/py/threading_rlock#L252"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `threading_rlock`

```python
threading_rlock(timeout)
```






---

<a href="../booktest/requests.py#L410"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `snapshot_requests`

```python
snapshot_requests(
    lose_request_details=True,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None,
    match_request=None,
    url=None
)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list @param json_to_hash allows adding your own json to hash for calculating hash code to request.  can be used to print or prune e.g. http arguments in case they contain e.g. platform specific  details or timestamps @param encode_body allows adding your own body encoding for removing e.g. platform or time details from  request bodies. this needs to always return a string. encode body method receives body, url and method 


---

## <kbd>class</kbd> `RequestKey`




<a href="../booktest/requests.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(json_object, ignore_headers=True, json_to_hash=None)
```








---

<a href="../booktest/requests.py#L96"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_properties`

```python
from_properties(
    url,
    method,
    headers,
    body,
    ignore_headers,
    json_to_hash=None,
    encode_body=None
)
```





---

<a href="../booktest/requests.py#L115"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_request`

```python
from_request(
    request: PreparedRequest,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None
)
```





---

<a href="../booktest/requests.py#L74"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `increase_order`

```python
increase_order()
```





---

<a href="../booktest/requests.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_json_object`

```python
to_json_object(hide_details)
```





---

<a href="../booktest/requests.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `url`

```python
url()
```






---

## <kbd>class</kbd> `RequestSnapshot`




<a href="../booktest/requests.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(request: RequestKey, response: Response)
```








---

<a href="../booktest/requests.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_json_object`

```python
from_json_object(json_object, ignore_headers=True, json_to_hash=None)
```





---

<a href="../booktest/requests.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `hash`

```python
hash()
```





---

<a href="../booktest/requests.py#L156"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `json_object`

```python
json_object(hide_details)
```





---

<a href="../booktest/requests.py#L140"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `match`

```python
match(request: RequestKey)
```






---

## <kbd>class</kbd> `SnapshotAdapter`
A fake adapter than can return predefined responses. 

<a href="../booktest/requests.py#L179"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    snapshots,
    capture_snapshots,
    ignore_headers,
    json_to_hash=None,
    encode_body=None,
    match_request=<function accept_all at 0x7b4e2dbf9440>
)
```








---

<a href="../booktest/requests.py#L201"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `get_snapshot`

```python
get_snapshot(key)
```





---

<a href="../booktest/requests.py#L210"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `lookup_request_snapshot`

```python
lookup_request_snapshot(request)
```





---

<a href="../booktest/requests.py#L194"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `mark_order`

```python
mark_order(key: RequestKey)
```





---

<a href="../booktest/requests.py#L237"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `send`

```python
send(request, **kwargs)
```





---

<a href="../booktest/requests.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `snapshot`

```python
snapshot(request)
```






---

## <kbd>class</kbd> `SnapshotRequests`




<a href="../booktest/requests.py#L295"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    t: TestCaseRun,
    lose_request_details=True,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None,
    match_request=<function accept_all at 0x7b4e2dbf9440>
)
```








---

<a href="../booktest/requests.py#L345"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start()
```

Start mocking requests.  



---

<a href="../booktest/requests.py#L375"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `stop`

```python
stop()
```

Stop mocking requests. 

This should have no impact if mocking has not been started. When nesting mockers, make sure to stop the innermost first. 

---

<a href="../booktest/requests.py#L395"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `t_snapshots`

```python
t_snapshots()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
