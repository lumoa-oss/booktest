# testing pytest project with booktest


# command:

booktest -v

# configuration:

 * context: examples/pytest

# output:


# test results:

test book/test_hello/hello...

  the message is hello world!

book/test_hello/hello ok in <number> ms.

test book/teardown/setup_teardown/setup_teardown...

  # description:
  
  global operations are needed to things like faking system times
  or initializing resources. 
  
  booktest allows user to define process_setup_teardown in __booktest__.py
  to set up and teardown global settings
  
  # test:
  
  the global variable should always be 'set'
  
  global variable is 'set'..ok

book/teardown/setup_teardown/setup_teardown ok in <number> ms.


2/2 test succeeded in <number> ms



# testing pytest project with pytest

============================= test session starts ==============================
platform linux -- Python 3.11.9, pytest-8.3.4, pluggy-1.5.0 -- /home/arau/.cache/pypoetry/virtualenvs/booktest-OySOPCsb-py3.11/bin/python
cachedir: .pytest_cache
rootdir: /home/arau/lumoa/src/booktest/examples/pytest
configfile: pytest.ini
testpaths: test
plugins: anyio-4.7.0
collecting ... collected 4 items

test/test_books.py::test_fs_detect[book/test_hello/hello] PASSED         [ 25%]
test/test_books.py::test_fs_detect[book/teardown/setup_teardown/setup_teardown] PASSED [ 50%]
test/test_books.py::test_module_detect[book/teardown/setup_teardown/setup_teardown] PASSED [ 75%]
test/test_books.py::test_module_detect[book/test_hello/hello] PASSED     [100%]

============================== 4 passed in <number>s ===============================


return code is 0..ok
