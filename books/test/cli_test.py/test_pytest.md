# testing pytest project with booktest


# command:

booktest -v

# configuration:

 * context: examples/pytest

# output:


# test results:

test book/test_hello.py::test_hello...

  the message is hello world!

book/test_hello.py::test_hello OK <number> ms.

test book/teardown/setup_teardown_test.py::test_setup_teardown...

  # description:
  
  global operations are needed to things like faking system times
  or initializing resources. 
  
  booktest allows user to define process_setup_teardown in __booktest__.py
  to set up and teardown global settings
  
  # test:
  
  the global variable should always be 'set'
  
  global variable is 'set'..ok

book/teardown/setup_teardown_test.py::test_setup_teardown OK <number> ms.


2/2 test succeeded in <number> ms



# testing pytest project with pytest

test/test_books.py::test_fs_detect[book/test_hello.py::test_hello] PASSED [ 16%]
test/test_books.py::test_fs_detect[book/teardown/setup_teardown_test.py::test_setup_teardown] PASSED [ 33%]
test/test_books.py::test_module_detect[book/teardown/setup_teardown_test.py::test_setup_teardown] PASSED [ 50%]
test/test_books.py::test_module_detect[book/test_hello.py::test_hello] PASSED [ 66%]
test/test_books.py::test_books[book/teardown/setup_teardown_test.py::test_setup_teardown] PASSED [ 83%]
test/test_books.py::test_books[book/test_hello.py::test_hello] PASSED    [100%]

return code is 0..ok
