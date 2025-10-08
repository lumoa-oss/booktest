
test raised exception missing snapshot for request https://postman-echo.com/get - 0e88eb6e0a8953a80d7d4af2b621e3bd65098073. try running booktest with '-s' flag to capture the missing snapshot:
Traceback (most recent call last):
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 105, in run_case
    rv = await maybe_async_call(case, [t], {})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/httpx.py", line 421, in wrapper
    return await maybe_async_call(func , args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/examples/async_book.py", line 53, in test_httpx
    response = await client.get("https://postman-echo.com/get")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1814, in get
    return await self.request(
           ^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1585, in request
    return await self.send(request, auth=auth, follow_redirects=follow_redirects)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1674, in send
    response = await self._send_handling_auth(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1702, in _send_handling_auth
    response = await self._send_handling_redirects(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1739, in _send_handling_redirects
    response = await self._send_single_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1776, in _send_single_request
    response = await transport.handle_async_request(request)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/httpx.py", line 309, in mocked_handle_async_request
    return await self.handle_async_request(transport, request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/httpx.py", line 288, in handle_async_request
    return await self.async_snapshot_request(transport, request)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/httpx.py", line 278, in async_snapshot_request
    key, rv = self.lookup_request_snapshot(request)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/httpx.py", line 257, in lookup_request_snapshot
    raise ValueError(f"missing snapshot for request {request.url} - {key.hash}. "
ValueError: missing snapshot for request https://postman-echo.com/get - 0e88eb6e0a8953a80d7d4af2b621e3bd65098073. try running booktest with '-s' flag to capture the missing snapshot

