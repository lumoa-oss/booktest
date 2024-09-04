<!-- markdownlint-disable -->

<a href="../booktest/httpx.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `httpx.py`





---

<a href="../booktest/httpx.py#L312"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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




<a href="../booktest/httpx.py#L27"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(json_object, ignore_headers=True, json_to_hash=None)
```








---

<a href="../booktest/httpx.py#L75"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/httpx.py#L98"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/httpx.py#L63"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `to_json_object`

```python
to_json_object(hide_details)
```





---

<a href="../booktest/httpx.py#L60"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `url`

```python
url()
```






---

## <kbd>class</kbd> `RequestSnapshot`




<a href="../booktest/httpx.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(request: RequestKey, response: Response)
```








---

<a href="../booktest/httpx.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `from_json_object`

```python
from_json_object(json_object, ignore_headers=True, json_to_hash=None)
```





---

<a href="../booktest/httpx.py#L160"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `hash`

```python
hash()
```





---

<a href="../booktest/httpx.py#L141"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `json_object`

```python
json_object(hide_details)
```





---

<a href="../booktest/httpx.py#L123"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `match`

```python
match(request: RequestKey)
```






---

## <kbd>class</kbd> `SnapshotHttpx`




<a href="../booktest/httpx.py#L169"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

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

<a href="../booktest/httpx.py#L245"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `async_handle_request`

```python
async_handle_request(transport: AsyncHTTPTransport, request: Request)
```





---

<a href="../booktest/httpx.py#L236"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `handle_request`

```python
handle_request(transport: HTTPTransport, request: Request)
```





---

<a href="../booktest/httpx.py#L213"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `lookup_snapshot`

```python
lookup_snapshot(request: Request)
```





---

<a href="../booktest/httpx.py#L231"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `save_snapshot`

```python
save_snapshot(key, response)
```





---

<a href="../booktest/httpx.py#L254"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start()
```





---

<a href="../booktest/httpx.py#L280"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `stop`

```python
stop()
```





---

<a href="../booktest/httpx.py#L299"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `t_snapshots`

```python
t_snapshots()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
