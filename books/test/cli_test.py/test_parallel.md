# command:

booktest -p

# configuration:

 * context: examples/predictor

# output:


# test results:

  book/predictor_book.py::PredictorBook/test_predictor - DIFFERED in <number> ms
  book/predictor_book.py::PredictorBook/test_predict_dog - DIFFERED in <number> ms

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILURE REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# test results:

test book/predictor_book.py::PredictorBook/test_predictor

  making predictor..0.<number> ms

book/predictor_book.py::PredictorBook/test_predictor DIFFERED in <number> ms

test book/predictor_book.py::PredictorBook/test_predict_dog

  dog is a mammal with probability 0.5,
  because most mammals have 4 legs

book/predictor_book.py::PredictorBook/test_predict_dog DIFFERED in <number> ms


2/2 test 2 differed in <number> ms:

  book/predictor_book.py::PredictorBook/test_predictor - DIFF
  book/predictor_book.py::PredictorBook/test_predict_dog - DIFF


💡 To review (-w) failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -w -c -v -i
💡 To rerun failed (-c) tests verbosely (-v) and interactively (-i), run: booktest -c -v -i
💡 To update failed tests's (-c) missing snapshots (-s), run: booktest -c -s


