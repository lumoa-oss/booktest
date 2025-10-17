# description:

this test verifies that the slow test will fail with 1s timeout

# command:

booktest -p --timeout 2

# configuration:

 * context: examples/timeout

# output:


# test results:

  book/timeout_book.py::test_fast - <number> ms
  book/timeout_book.py::test_slow - FAILED in <number> ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# test results:

test book/timeout_book.py::test_slow

  waiting 3s...
  done.

book/timeout_book.py::test_slow FAILED in <number> ms


1/2 test 1 failed in <number> ms:

  book/timeout_book.py::test_slow - FAIL


💡 To review (-w) failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -w -c -v -i
💡 To rerun failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -c -v -i
💡 To update failed tests's (-c) missing snapshots (-s), run: booktest -c -s


