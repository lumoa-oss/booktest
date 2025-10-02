# description:

this test verifies that:

 1) snapshots can be recreated
 2) and tool requires user to accept & store recreated snapshot even if their hashes are the same

# command:

booktest -S -v

# configuration:

 * context: examples/broken_snapshots

# output:


# test results:

test book/broken_snapshots/function_snapshot...

  # snapshot:
  
   * hello: hello world

book/broken_snapshots/function_snapshot OK/UPDATED in <number> ms.

test book/broken_snapshots/httpx...

? # response url parameter:                                    | # response:
  
? "https://postman-echo.com/get"                               | {

book/broken_snapshots/httpx DIFF/UPDATED in <number> ms

test book/broken_snapshots/requests...

? # response url parameter:                                    | # response:
  
? "https://postman-echo.com/get"                               | {

book/broken_snapshots/requests DIFF/UPDATED in <number> ms


2/3 test failed in <number> ms:

  book/broken_snapshots/httpx
  book/broken_snapshots/requests


