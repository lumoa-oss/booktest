# description:

narrow detection only run detection in related modules/test suites. 
this test merely verifies that nothing breaks, when invoking the code

# command:

booktest --narrow-detection book/predictor_book.py

# configuration:

 * context: examples/predictor

# output:


# test results:

  book/predictor_book.py::PredictorBook/test_predictor - <number> ms
  book/predictor_book.py::PredictorBook/test_predict_dog - <number> ms

2/2 test succeeded in <number> ms


