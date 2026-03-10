# testing snapshot caching

if caching works correctly, the expensive operation
should only be called once (on initial capture)

result: {'call_number': 1, 'query': 'test-query', 'result': 'data'}
call count: 0
elapsed seconds: 0.0

SUCCESS: Function was not called (cached result used)
