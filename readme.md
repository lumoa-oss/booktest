# Booktest

booktest is review-driven testing tool that combines Jupyterbook style data science
development with traditional regression testing. Booktest is developed by 
[Lumoa.me](https://lumoa.me), the actionable feedback analytics platform.

booktest is designed to tackle a common problem with the data science
RnD work flows and regression testing: 

 * Data science produces results such as probability estimates, which can be 
   good or bad, but not really right or wrong as in the traditional software engineering. 
     * Because the DS results are not strictly right or wrong, it's very difficult to use assertions 
       for quality assurance and preventing regression.
     * For example, you cannot really say that accuracy 0.84 is correct, while the 
       accuracy 0.83 is incorrect, especially if you have other measurements (log likelihood)
       giving conflicting results. Neither evaluating a topic model as correct or incorrect
       is non-sensical. In practice, most data science applications require an expert 
       review.
     * This less ambigious quality also creates need for a better visibility of how
       the system behaves. One typically wants to print out edge cases and their diagnostics
       to see the behavior, see intermediate steps and see the results for different data sets . 
 * There is also the problem of the data science data being big and the intermediate 
   results being computationally expensive. 
     * Jupyter notebook deals with this problem by keeping the state in memory between runs, while 
       traditional unittests tend to lose the program state between runs. This leads to very slow 
       test runs, slow iteration speed and low productivity.
 * While the Jupyter Notebook provides good visibility to results required by the expert review and
   powerful caching functionality: it fails short on a) often requiring copy-pasting production code to 
   make results visible, b) it doesn't support automated regression testing and c) expert review requires
   expensive full review even if nothing changed.

booktest solves this problem setting by delivering on 3 main points:

 * Focus on the results and analytic as in Jupyter notebook by allowing user to print
   the results as MD files. 
 * Keep the intermediate results cached either in memory or in filesystem by
   having two level cache.
 * Instead of doing strict assertions, do testing by comparing old results with 
   new results.

As such, booktest does snapshot testing, and it stores the snapshots in filesystem and in Git. 
Additional benefit of this approach is that you can trace the result development in Git.

# Getting started guide

You can find getting started guide [here](getting-started.md)

# Workflows, coverage and CI

You can find guide on common workflows, coverage measurements and 
continuous integration [here](workflows.md)

# Examples

Examples are found in the [test example directory](test/examples). 

Example results are visible in the [book index](books/index.md).

There are example projects found in example directory: 

 * [examples/predictor](examples/predictor/README.md) demonstrates a simple predictor using booktest
 * [examples/configurations](examples/configurations/readme.md) demonstrates how booktest can be configured
 * [examples/configurations](examples/configurations/readme.md) demonstrates how booktest can be integrated to pytest.

# API reference

API reference is generated under [docs](docs) directory. Main classes are:

 * [TestCaseRun](docs/testcaserun.py.md), which provides API for tests
 * [TestBook](docs/testbook.py.md), which provide a base class for test suite object
 * [TestSuite](docs/testsuite.py.md), which provide a base class for test suite object
 * [Tests](docs/tests.py.md), which manages CLI interface

# Developing booktest

Development guide is available [here](development.md)
