# description:

narrow detection only run detection in related modules/test suites. 
this test merely verifies that nothing breaks, when invoking the code

# command:

booktest --narrow-detection predictor

# configuration:

 * context: examples/predictor

# output:



# error:

usage: booktest [-h] [-i] [-I] [-v] [-L] [-f] [-c] [-r] [-u] [-a] [-p] [-p1]
                [-p2] [-p3] [-p4] [-p6] [-p8] [-p16] [--parallel-count P] [-s]
                [-S] [--cov] [--md-viewer MD_VIEWER] [--diff-tool DIFF_TOOL]
                [--context CONTEXT] [--python-path PYTHON_PATH]
                [--resource-snapshots] [--timeout TIMEOUT]
                [--narrow-detection] [-l] [--setup] [--garbage] [--clean]
                [--config] [--print] [--view] [--path] [--review] [-w]
                [--forget]
                [{*} ...]
booktest: error: argument test_cases: invalid choice: 'predictor' (choose from '*')

