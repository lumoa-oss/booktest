<!-- markdownlint-disable -->

<a href="../booktest/httpx.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `httpx.py`





---

<a href="../booktest/httpx.py#L324"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `snapshot_httpx`

```python
snapshot_httpx(
    lose_request_details=True,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None
)
```

@param lose_request_details Saves no request details to avoid leaking keys @param ignore_headers Ignores all headers (True) or specific header list @param json_to_hash allows adding your own json to hash for calculating hash code to request.  can be used to print or prune e.g. http arguments in case they contain e.g. platform specific  details or timestamps @param encode_body allows adding your own body encoding for removing e.g. platform or time details from  request bodies. this needs to always return a string. encode body method receives body, url and method 


---

## <kbd>class</kbd> `RequestKey`




<a href="../booktest/httpx.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(json_object, ignore_headers=True, json_to_hash=None)
```








---

<a href="../booktest/httpx.py#L83"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/httpx.py#L106"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_request`

```python
from_request(
    request: Request,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None
)
```





---

<a href="../booktest/httpx.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `increase_order`

```python
increase_order()
```





---

<a href="../booktest/httpx.py#L71"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_json_object`

```python
to_json_object(hide_details)
```





---

<a href="../booktest/httpx.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `url`

```python
url()
```






---

## <kbd>class</kbd> `RequestSnapshot`




<a href="../booktest/httpx.py#L125"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(request: RequestKey, response: Response)
```








---

<a href="../booktest/httpx.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_json_object`

```python
from_json_object(json_object, ignore_headers=True, json_to_hash=None)
```





---

<a href="../booktest/httpx.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `hash`

```python
hash()
```





---

<a href="../booktest/httpx.py#L149"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `json_object`

```python
json_object(hide_details)
```





---

<a href="../booktest/httpx.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `match`

```python
match(request: RequestKey)
```






---

## <kbd>class</kbd> `SnapshotHttpx`




<a href="../booktest/httpx.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(
    t: TestCaseRun,
    lose_request_details=True,
    ignore_headers=True,
    json_to_hash=None,
    encode_body=None
)
```








---

<a href="../booktest/httpx.py#L257"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `handle_async_request`

```python
handle_async_request(transport: AsyncHTTPTransport, request: Request)
```





---

<a href="../booktest/httpx.py#L248"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `handle_request`

```python
handle_request(transport: HTTPTransport, request: Request)
```





---

<a href="../booktest/httpx.py#L228"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `lookup_snapshot`

```python
lookup_snapshot(request: Request)
```





---

<a href="../booktest/httpx.py#L221"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `mark_order`

```python
mark_order(key: RequestKey)
```





---

<a href="../booktest/httpx.py#L266"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start()
```





---

<a href="../booktest/httpx.py#L292"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `stop`

```python
stop()
```





---

<a href="../booktest/httpx.py#L311"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `t_snapshots`

```python
t_snapshots()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
