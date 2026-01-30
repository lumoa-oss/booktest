<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.snapshots.requests`





---

## <kbd>function</kbd> `json_to_sha1`

```python
json_to_sha1(json_object)
```






---

## <kbd>function</kbd> `default_encode_body`

```python
default_encode_body(body, _url, _method)
```






---

## <kbd>function</kbd> `threading_rlock`

```python
threading_rlock(timeout)
```






---

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




### <kbd>method</kbd> `__init__`

```python
__init__(json_object, ignore_headers=True, json_to_hash=None)
```








---

### <kbd>method</kbd> `from_properties`

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

### <kbd>method</kbd> `from_request`

```python
from_request(
    request: PreparedRequest,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None
)
```





---

### <kbd>method</kbd> `increase_order`

```python
increase_order()
```





---

### <kbd>method</kbd> `to_json_object`

```python
to_json_object(hide_details)
```





---

### <kbd>method</kbd> `url`

```python
url()
```






---

## <kbd>class</kbd> `RequestSnapshot`




### <kbd>method</kbd> `__init__`

```python
__init__(request: RequestKey, response: Response)
```








---

### <kbd>method</kbd> `from_json_object`

```python
from_json_object(json_object, ignore_headers=True, json_to_hash=None)
```





---

### <kbd>method</kbd> `hash`

```python
hash()
```





---

### <kbd>method</kbd> `json_object`

```python
json_object(hide_details)
```





---

### <kbd>method</kbd> `match`

```python
match(request: RequestKey)
```






---

## <kbd>class</kbd> `SnapshotAdapter`
A fake adapter than can return predefined responses. 

### <kbd>method</kbd> `__init__`

```python
__init__(
    snapshots,
    capture_snapshots,
    ignore_headers,
    json_to_hash=None,
    encode_body=None,
    match_request=<function accept_all at 0x79bd3f5ca480>
)
```








---

### <kbd>method</kbd> `get_snapshot`

```python
get_snapshot(key)
```





---

### <kbd>method</kbd> `lookup_request_snapshot`

```python
lookup_request_snapshot(request)
```





---

### <kbd>method</kbd> `mark_order`

```python
mark_order(key: RequestKey)
```





---

### <kbd>method</kbd> `send`

```python
send(request, **kwargs)
```





---

### <kbd>method</kbd> `snapshot`

```python
snapshot(request)
```






---

## <kbd>class</kbd> `SnapshotRequests`




### <kbd>method</kbd> `__init__`

```python
__init__(
    t: TestCaseRun,
    lose_request_details=True,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None,
    match_request=<function accept_all at 0x79bd3f5ca480>
)
```








---

### <kbd>method</kbd> `start`

```python
start()
```

Start mocking requests.  



---

### <kbd>method</kbd> `stop`

```python
stop()
```

Stop mocking requests. 

This should have no impact if mocking has not been started. When nesting mockers, make sure to stop the innermost first. 

---

### <kbd>method</kbd> `t_snapshots`

```python
t_snapshots()
```

Report snapshot usage to the system instead of printing to test results. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
