# description:

this test verifies that broken snapshots will gracefully fail

# command:

booktest 

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

  book/broken_snapshots_book.py::test_function_snapshot - FAIL <number> ms (snapshots updated)
  book/broken_snapshots_book.py::test_httpx - FAIL <number> ms
  book/broken_snapshots_book.py::test_requests - FAIL <number> ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# test results:

test book/broken_snapshots_book.py::test_function_snapshot

  # snapshot:
  
  
! test raised exception missing snapshot for function call hello_world - 10b1d5dde04cb7165fda604e9c02a88365ede15c. try running booktest with '-s' flag to capture the missing snapshot: | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/functions.py", line 282, in wrapper
      return await maybe_async_call(func, args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 8, in maybe_async_call
      return func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/broken_snapshots/book/broken_snapshots_book.py", line 36, in test_function_snapshot
      t.keyvalueln(" * hello:", hello_world())
                                ^^^^^^^^^^^^^
    File "<workdir>/booktest/functions.py", line 99, in __call__
      return self.t.snapshot(self.func, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/functions.py", line 147, in snapshot
      raise ValueError(f"missing snapshot for function call {call.func()} - {call.hash}. "
  ValueError: missing snapshot for function call hello_world - 10b1d5dde04cb7165fda604e9c02a88365ede15c. try running booktest with '-s' flag to capture the missing snapshot
  

book/broken_snapshots_book.py::test_function_snapshot FAILED in <number> ms

test book/broken_snapshots_book.py::test_httpx

  
! test raised exception missing snapshot for request https://postman-echo.com/get - 0e88eb6e0a8953a80d7d4af2b621e3bd65098073. try running booktest with '-s' flag to capture the missing snapshot: | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/httpx.py", line 421, in wrapper
      return await maybe_async_call(func , args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 8, in maybe_async_call
      return func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/broken_snapshots/book/broken_snapshots_book.py", line 21, in test_httpx
      response = httpx.get("https://postman-echo.com/get")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_api.py", line 210, in get
      return request(
             ^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_api.py", line 118, in request
      return client.request(
             ^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 837, in request
      return self.send(request, auth=auth, follow_redirects=follow_redirects)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 926, in send
      response = self._send_handling_auth(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 954, in _send_handling_auth
      response = self._send_handling_redirects(
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 991, in _send_handling_redirects
      response = self._send_single_request(request)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/httpx/_client.py", line 1027, in _send_single_request
      response = transport.handle_request(request)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/httpx.py", line 299, in mocked_handle_request
      return self.handle_request(transport, request)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/httpx.py", line 273, in handle_request
      return self.snapshot_request(transport, request)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/httpx.py", line 263, in snapshot_request
      key, rv = self.lookup_request_snapshot(request)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/httpx.py", line 257, in lookup_request_snapshot
      raise ValueError(f"missing snapshot for request {request.url} - {key.hash}. "
  ValueError: missing snapshot for request https://postman-echo.com/get - 0e88eb6e0a8953a80d7d4af2b621e3bd65098073. try running booktest with '-s' flag to capture the missing snapshot
  

book/broken_snapshots_book.py::test_httpx FAILED in <number> ms

test book/broken_snapshots_book.py::test_requests

  
! test raised exception missing snapshot for request https://postman-echo.com/get - 085bbb060375440e09281c5b08f704d4a53a6d4a. try running booktest with '-s' flag to capture the missing snapshot: | EOF
  Traceback (most recent call last):
    File "<workdir>/booktest/testrun.py", line 105, in run_case
      rv = await maybe_async_call(case, [t], {})
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 6, in maybe_async_call
      return await func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/requests.py", line 489, in wrapper
      return await maybe_async_call(func , args, kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/coroutines.py", line 8, in maybe_async_call
      return func(*args2, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/examples/broken_snapshots/book/broken_snapshots_book.py", line 13, in test_requests
      response = requests.get("https://postman-echo.com/get")
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/api.py", line 73, in get
      return request("get", url, params=params, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/api.py", line 59, in request
      return session.request(method=method, url=url, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/sessions.py", line 589, in request
      resp = self.send(prep, **send_kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/requests.py", line 374, in _fake_send
      return _original_send(session, request, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/sessions.py", line 703, in send
      r = adapter.send(request, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/requests.py", line 239, in send
      return self.snapshot(request)
             ^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/requests.py", line 229, in snapshot
      key, rv = self.lookup_request_snapshot(request)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "<workdir>/booktest/requests.py", line 223, in lookup_request_snapshot
      raise ValueError(f"missing snapshot for request {request.url} - {key.hash}. "
  ValueError: missing snapshot for request https://postman-echo.com/get - 085bbb060375440e09281c5b08f704d4a53a6d4a. try running booktest with '-s' flag to capture the missing snapshot
  

book/broken_snapshots_book.py::test_requests FAILED in <number> ms


3/3 test 3 failed in <number> ms:

  book/broken_snapshots_book.py::test_function_snapshot - FAIL
  book/broken_snapshots_book.py::test_httpx - FAIL
  book/broken_snapshots_book.py::test_requests - FAIL


💡 To review interactively, run: booktest -w
💡 To rerun and review failed test results, run: booktest -v -i -c


