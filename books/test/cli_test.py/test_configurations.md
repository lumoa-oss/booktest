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


💡 To review (-w) failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -w -c -v -i
💡 To rerun failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -c -v -i
💡 To update failed tests's (-c) missing snapshots (-s), run: booktest -c -s


