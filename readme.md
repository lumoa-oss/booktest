# Booktest

booktest is review-driven testing tool that combines Jupyterbook style data science
development with traditional regression testing. Booktest is developed by 
[Lumoa.me](https://lumoa.me), the actionable feedback analytics platform.

book_test is designed to tackle a common problem with the data science work 
RnD work flows and regression testing: 

 * Data science produces results such as probability estimates, which can be 
   good or bad, but not really right or wrong as in traditional software engineering. 
     * Because the DS results are not right/wrong, it's very difficult to use assertions 
       to support the data science RnD workflow or regression testing.
     * For example, can you cannot really assert that accuracy 0.84 is correct, 
       but the accuracy 0.83 is incorrec. Neither you cannot really assert that this
       topic model is correct, but this different is not. Such assertions require
       an expert opinion and in extreme cases: the assertions can be somewhat subjective.
     * At the same time, while Jupyter notebooks support the data science workflow by
       providing the necessary visibility to results to do the expert review, it 
       cannot be used for regression testing purposes.
 * There is also the problem of the data science data being big, and the intermediate 
   results being computationally expensive. 
     * Jupyter notebook supports this by keeping the state in memory between runs, while 
       traditional unittests tend to lose the program state between runs.
 * So the problem is that what kind of tool would support BOTH data science workflow and
   the regression testing needs.

book_test solves this problem by delivering on 3 main points:

 * Focus on the results and analytic as in Jupyter notebook by allowing user to print
   the results as MD files. 
 * Keep the intermediate results cached either in memory or in filesystem by
   having two level cache.
 * Instead of doing strict assertions, do testing by comparing old results with 
   new results.

As such, book_test does snapshot testing, and it stores the snapshots in filesystem and in Git. 
Additional benefit of this approach is that you can trace the result development in Git.

You can find the test behavior and results [here](books/index.md)

# Setup

## dependencies

You will need Poetry and Python 3.8 to use this package. To set-up the environment
and run the commands described in this package, run:

```bash
poetry shell
```


## Configurations

Book test uses two tools for reviewing the test results, that are: 

 1. diff tool for reviewing changes in results
 2. md tool for viewing MD files 

These tools depend on the OS, environment and user preferences. 
To choose tools that work for you:

 1. copy the .booktest.example as .booktest
 2. change the defaults (meld, retext) to a difftool and
    an md tool, that work for you in your working environment.

# Testing

To run the test cases, run:

```bash
booktest test
```

The tests are run against expectation files, which 
represent test snapshots and have been generated
from previous runs. 

Click [here](books/index.md) to see the booktest test cases
expectation files.

# Guide

## Getting started with book test

If you want to take booktest into use, first install the booktest pypi
package with: 

```bash
pip install booktest
```

Then add `test/` directory containing e.g. the following
test case

```python
import booktest as bt

class ExampleTest(bt.TestBook):

    def test_hello(self, t: bt.TestCaseRun):
        t.h1("This test prints hello world")
        t.tln("hello world")
```

After this, you can run: 

```bash
booktest test -v -i
```

To see the test results in the verbose mode and freeze the test snapshot. 
Once the snapshot has been frozen, there will be `hello.md` file stored
in `books/example` folder and `index.md` in `books` folder containing
links to all tests cases. 

After this, you can run the test in a non-verbose and non-interactive mode 
to check that everything works.

```bash
booktest test
```

The md files in `book` folder should be added to the version control. 
Remember to add the `books/test/.out` or `.out` into the .gitgnore to avoid
committing temporary test files and caches into the repository

## Configuration

NOTE, that booktest relies on external MD viewer and diff tool. Also, booktest
uses default directory paths for looking up tests, for storing the books and for
storing caches and the output. 

You can configure these variables by creating .booktest file in the root directory with 
content like:

```
#
# diff_tool is used to see changes in the results
#
diff_tool=meld

#
# md_viewer is used to view the md content, like tables, lists, links and images
#
md_viewer=retext --preview

#
# default paths for looking up test cases
#
test_paths=test,book,run

#
# default location for storing the results and books
#
books_path=books
```

## Common workflows

To see available test cases run:

```bash
booktest -l
```

After creating a new test case you may want to run the test case in 
a verbose (`-v`) and interactive (`-i`) mode to see how the test case works:

```bash
booktest -v -i suite/path
```

If the test case is using caches built in previous test cases, and you
want to refresh those caches, use the `-r` refresh flag:

```bash
booktest -v -i -r suite/test-with-dependencies
```

If you have done wider modifications in the code, you may want to run tests in 
interactive mode to see how things work:

```bash
booktest -v -i
```

You can use 'q' option in interactive mode to abort the testing, if you need to 
e.g. fix a broken test case. To continue from the last failed test, you 
can use `-c` continue flag. Using `-c` will skip all already succeeded tests.

```bash
booktest -v -i -c
```

Before doing a commit or a PR, it makes sense to run the tests in non-interactive
and fragile mode 

```bash
booktest -f
```

This will automatically stop the test on first failure. The `./do test -v -i -c`
can be used to inspect the failure and fix it.

If you have tons of test cases, you may want to run them parallel and get a cup of coffee:

```bash
booktest -p
```

If tests failed, you likely want review (-w) them in interactive (-i) mode:

```bash
booktest -w -i
```

If you want to see the test results containing you can use 

```bash
booktest --print measurements/speed
```

If you want to view the test results containing e.g. books or tables an in MD viewer, 
you can use 

```bash
booktest --view analysis/graphs-and-tables
```

If you have been deleting or renaming tests cases, and want to remove the old
expectation files and temporary files, you can first check the garbage

```bash
booktest --garbage
```

Then it can be deleted with `--clean`:

```bash
booktest --clean
```

## Coverage measurement

To measure and print coverage, run: 

```bash
coverage run -m booktest
coverage combine
coverage report
```

There is also a separate command for measuring coverage, but this setups
coverage *after* modules have been loaded, which meaans that lines run
module load time are not included in measurements.

```bash
booktest --cov
```

## CI integration

In bitbucket pipelines, you can add the following step:

```
- pip install -r requirements.txt
- booktest || booktest -w -v -c
```

`booktest` will run all test cases and `booktest -w -v -c` 
print verbose review of all failed test cases, if the 
run failed.

## Tips and tricks

### Enable autocomplete

To enable the autocomplete, run the following in bash:

```bash
eval "$(register-python-argcomplete booktest)"
```

### Integrating booktest to CLI interface using argparse

It often helps both the developer workflow and introducing other people 
into the project, if you provide a simple developer CLI interface for
running common tasks in the project. 

This CLI interface may include commands for e.g. linting the code, 
deploying pypi packages or running tests.

As long your CLI interface uses the Python argparse, integrating the 
booktest should be easy. You can follow the example in the `do.py` and 
`do` scripts in this project:

```python
import argparse
import argcomplete
import sys
import test.tests as tests

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='sub-command help')

# TODO: add your own parsers
tests_parser = subparsers.add_parser("test")
tests.setup_parser(tests_parser)
tests_parser.set_defaults(
    exec=lambda parsed:
    tests.exec_parsed("books/test",
                      parsed))

argcomplete.autocomplete(parser)
parsed = parser.parse_args(sys.args)

exit(parsed.exec(parsed))
```

After the integration, you can run the test cases with:

```
./do test examples/hello
```

### Tests and runs

In data science, there are often 2 different needs related to booktest:

 - Regression testing, which is run in CI and run locally to assert
   quality. Regression testing should always use public data, and 
   this public data and the test results can be kept in Git to make
   testing easier.
   
 - Runs with real data and integrations, which may take long time,
   use sensitive data or use live integrations. These runs are impractical
   to keep updated and run in CI. Because they may contain real sensitive
   data, the data or test results cannot maintained in Git.
   
Booktest can help maintaining and rerunning the real world tests, which 
may still be necessary for asserting the system real word performance and 
quality and for doing exploratory analysis. 

You may want to save the run data separately and supply separate method
for loading test data.

```
./do load-run-data
```

After this, you can create a separate test suite for the runs with 
separate integration

```
runs_parser = subparsers.add_parser("run")
runs.setup_parser(tests_parser)
runs_parser.set_defaults(
    exec=lambda parsed:
        runs.exec_parsed("books/runs",
                         parsed))
```

After this, the runs can be executed with:

```bash
./do run -v -i real-world-case
```

Similar integrations can be done for e.g. performance testing, which 
may be slow enough to be maintained and run non-regularly and outside CI:

```bash
./do perf -v -i slow-perfomance-test
```
