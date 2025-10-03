# description:

this test verifies that broken snapshots will gracefully fail

# command:

booktest 

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

  book/broken_snapshots/function_snapshot..FAIL <number> ms
  book/broken_snapshots/httpx..FAIL <number> ms
  book/broken_snapshots/requests..FAIL <number> ms

3/3 test failed in <number> ms:

  book/broken_snapshots/function_snapshot
  book/broken_snapshots/httpx
  book/broken_snapshots/requests


