# description:

this test verifies that:

 1) snapshots can be recreated
 2) and tool requires user to accept & store recreated snapshot even if their hashes are the same

# breaking snapshots

 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/function_snapshot.snapshots.json
 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/function_snapshot/_snapshots/functions.json
 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/httpx/_snapshots/httpx.json
 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/requests/_snapshots/requests.json

# command:

booktest -S -v

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

test book/broken_snapshots_book.py::test_function_snapshot

  # snapshot:
  
   * hello: hello world

book/broken_snapshots_book.py::test_function_snapshot DIFF <number> ms

test book/broken_snapshots_book.py::test_httpx

  # response url parameter:
  
  "https://postman-echo.com/get"

book/broken_snapshots_book.py::test_httpx DIFF <number> ms (snapshots updated)

test book/broken_snapshots_book.py::test_requests

  # response url parameter:
  
  "https://postman-echo.com/get"

book/broken_snapshots_book.py::test_requests DIFF <number> ms (snapshots updated)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# test results:

test book/broken_snapshots_book.py::test_function_snapshot

  # snapshot:
  
   * hello: hello world

book/broken_snapshots_book.py::test_function_snapshot DIFFERED in <number> ms

test book/broken_snapshots_book.py::test_httpx

  # response url parameter:
  
  "https://postman-echo.com/get"

book/broken_snapshots_book.py::test_httpx DIFFERED in <number> ms

test book/broken_snapshots_book.py::test_requests

  # response url parameter:
  
  "https://postman-echo.com/get"

book/broken_snapshots_book.py::test_requests DIFFERED in <number> ms


3/3 test 3 differed in <number> ms:

  book/broken_snapshots_book.py::test_function_snapshot - DIFF
  book/broken_snapshots_book.py::test_httpx - DIFF
  book/broken_snapshots_book.py::test_requests - DIFF


💡 To review (-w) failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -w -c -v -i
💡 To rerun failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -c -v -i
💡 To update failed tests's (-c) missing snapshots (-s), run: booktest -c -s



# rebreak snapshots to keep git status clean:

 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/function_snapshot.snapshots.json
 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/function_snapshot/_snapshots/functions.json
 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/httpx/_snapshots/httpx.json
 * broke snapshot file: examples/broken_snapshots/books/book/broken_snapshots/requests/_snapshots/requests.json
