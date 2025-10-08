# description:

sometimes apis are stateful and we want to keep track of response sequence
following requests should provide different answer

# first response:


test raised exception missing snapshot for request https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam - 61a85a10ba34bfb5cdee47cba501dee356846bbb. try running booktest with '-s' flag to capture the missing snapshot:
Traceback (most recent call last):
  File "/home/arau/lumoa/src/booktest/booktest/testrun.py", line 105, in run_case
    rv = await maybe_async_call(case, [t], {})
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 6, in maybe_async_call
    return await func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/requests.py", line 489, in wrapper
    return await maybe_async_call(func , args, kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/coroutines.py", line 8, in maybe_async_call
    return func(*args2, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/test/examples/snapshots_book.py", line 54, in test_requests_sequence
    response = requests.get("https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/api.py", line 73, in get
    return request("get", url, params=params, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/api.py", line 59, in request
    return session.request(method=method, url=url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/requests.py", line 374, in _fake_send
    return _original_send(session, request, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/lib/python3.11/site-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/requests.py", line 239, in send
    return self.snapshot(request)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/requests.py", line 229, in snapshot
    key, rv = self.lookup_request_snapshot(request)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/arau/lumoa/src/booktest/booktest/requests.py", line 223, in lookup_request_snapshot
    raise ValueError(f"missing snapshot for request {request.url} - {key.hash}. "
ValueError: missing snapshot for request https://timeapi.io/api/time/current/zone?timeZone=Europe%2FAmsterdam - 61a85a10ba34bfb5cdee47cba501dee356846bbb. try running booktest with '-s' flag to capture the missing snapshot

