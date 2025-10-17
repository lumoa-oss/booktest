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

test book/timeout_book.py::test_fast

  done.

book/timeout_book.py::test_fast ok in <number> ms.

test book/timeout_book.py::test_slow

  waiting 3s...
  done.

book/timeout_book.py::test_slow FAILED in <number> ms


1/2 test 1 failed in <number> ms:

  book/timeout_book.py::test_slow - FAIL


💡 To review interactively, run: booktest -w
💡 To rerun and review failed test results, run: booktest -v -i -c
💡 To update missing snapshots, run: 'booktest -c -s' or 'booktest -c -S' to refresh all


