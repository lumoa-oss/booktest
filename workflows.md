# Common workflows, coverage and CI

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

You may also want to inspect logs with -L flag:

```bash
booktest -w -i -L
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
for loading test data. After this, you can create a separate test suite for 
the runs in a separate directory called 'run'.

After this, the runs can be executed with:

```bash
booktest -v -i run/real-world-case
```

Similar integrations can be done for e.g. performance testing, which 
may be slow enough to be maintained and run non-regularly and outside CI:

```bash
booktest -v -i perf/slow-perfomance-test
```
