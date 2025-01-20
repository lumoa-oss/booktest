# description:

this test verifies that the slow test will fail with 1s timeout

# command:

booktest -p --timeout 1

# configuration:

 * context: examples/timeout

# output:


# test results:

  book/timeout/fast..<number> ms
  book/timeout/slow..FAILED in <number> ms

1/2 test failed in <number> ms:

  book/timeout/slow


