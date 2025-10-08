# testing pytest project with booktest


# command:

booktest -v

# configuration:

 * context: examples/pytest

# output:


# test results:

test book/test_hello.py::test_hello...

  the message is hello world!

book/test_hello.py::test_hello DIFF <number> ms

test book/teardown/setup_teardown_test.py::test_setup_teardown...

  # description:
  
  global operations are needed to things like faking system times
  or initializing resources. 
  
  booktest allows user to define process_setup_teardown in __booktest__.py
  to set up and teardown global settings
  
  # test:
  
  the global variable should always be 'set'
  
  global variable is 'set'..ok

book/teardown/setup_teardown_test.py::test_setup_teardown DIFF <number> ms


2/2 test failed in <number> ms:

  book/test_hello.py::test_hello
  book/teardown/setup_teardown_test.py::test_setup_teardown



# testing pytest project with pytest

test/test_books.py::test_fs_detect[book/test_hello.py::test_hello] FAILED [ 16%]
test/test_books.py::test_fs_detect[book/teardown/setup_teardown_test.py::test_setup_teardown] FAILED [ 33%]
test/test_books.py::test_module_detect[book/teardown/setup_teardown_test.py::test_setup_teardown] FAILED [ 50%]
test/test_books.py::test_module_detect[book/test_hello.py::test_hello] FAILED [ 66%]
test/test_books.py::test_books[book/teardown/setup_teardown_test.py::test_setup_teardown] FAILED [ 83%]
test/test_books.py::test_books[book/test_hello.py::test_hello] FAILED    [100%]
test/test_books.py:66: AssertionError
test/test_books.py:66: AssertionError
test/test_books.py:74: AssertionError
test/test_books.py:74: AssertionError
test/test_books.py:79: 
test/test_books.py:79: 

return code is 1..FAILED
