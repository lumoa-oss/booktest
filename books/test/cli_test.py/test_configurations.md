# command:

booktest -v

# configuration:

 * context: examples/configurations

# output:


# test results:

test booktests/test_hello.py::test_hello

  the message is hello world!

booktests/test_hello.py::test_hello DIFF <number> ms


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# test results:

test booktests/test_hello.py::test_hello

  the message is hello world!

booktests/test_hello.py::test_hello DIFFERED in <number> ms


1/1 test 1 differed in <number> ms:

  booktests/test_hello.py::test_hello - DIFF


💡 To review interactively, run: booktest -w
💡 To rerun and review failed test results, run: booktest -v -i -c


