# command:

booktest -h

# configuration:

 * context: examples/predictor

# output:

usage: booktest [-h] [-i] [-I] [-v] [-L] [-f] [-c] [-r] [-u] [-a] [-p] [-p1]
                [-p2] [-p3] [-p4] [-p6] [-p8] [-p16] [--parallel-count P] [-s]
                [-S] [--cov] [--md-viewer MD_VIEWER] [--diff-tool DIFF_TOOL]
                [--context CONTEXT] [--python-path PYTHON_PATH] [-l] [--setup]
                [--garbage] [--clean] [--config] [--print] [--view] [--path]
                [--review] [-w] [--forget]
                [{*,book,skip:book,book/predictor,skip:book/predictor,book/predictor/predictor,skip:book/predictor/predictor,book/predictor/predict_dog,skip:book/predictor/predict_dog} ...]

booktest - review driven test tool

positional arguments:
  {*,book,skip:book,book/predictor,skip:book/predictor,book/predictor/predictor,skip:book/predictor/predictor,book/predictor/predict_dog,skip:book/predictor/predict_dog}

options:
  -h, --help            show this help message and exit
  -i                    interactive mode
  -I                    always interactive, even on success
  -v                    verbose
  -L                    prints logs
  -f                    fails fast
  -c                    continue, skip succesful test
  -r                    refresh test dependencies
  -u                    update test on success
  -a                    automatically accept differing tests
  -p                    run test on N parallel processes, where is N relative
                        to CPU count
  -p1                   run test on 1 parallel processes
  -p2                   run test on 2 parallel processes
  -p3                   run test on 3 parallel processes
  -p4                   run test on 4 parallel processes
  -p6                   run test on 6 parallel processes
  -p8                   run test on 8 parallel processes
  -p16                  run test on 16 parallel processes
  --parallel-count P    run test on N parallel processes
  -s                    complete snapshots. this captures snapshots that are
                        missing
  -S                    refresh snapshots and discard old snapshots
  --cov                 store coverage information
  --md-viewer MD_VIEWER
                        set the used mark down viewer
  --diff-tool DIFF_TOOL
                        set the used diff tool
  --context CONTEXT     context, where the tests are detected and run. default
                        is local directory.
  --python-path PYTHON_PATH
                        python path for detecting source files. values should
                        separated by ':'. default is 'src:.'
  -l                    lists the selected test cases
  --setup               setups booktest
  --garbage             prints the garbage files
  --clean               cleans the garbage files
  --config              Prints the configuration
  --print               Prints the selected test cases expected output
  --view                Opens the selected test cases in markdown viewere
  --path                Prints the selected test cases expected output paths
  --review              Prints interactive report of previous run for review.
  -w                    Short hand for --review.
  --forget              Removes reviews from test cases. This stages them for
                        rerun even with -c flag.

