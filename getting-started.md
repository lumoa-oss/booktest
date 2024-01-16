# Getting started with book test

If you want to take booktest into use, first install the booktest pypi
package with: 

```bash
pip install booktest
```

Then add `test/` directory containing a file with the following
test case

```python
import booktest as bt

def test_hello(t: bt.TestCaseRun):
    t.h1("This test prints hello world")
    t.tln("hello world")
```

After this, you can run: 

```bash
booktest -v -i
```

...to see [this test's results](books/test/examples/hello/hello.md) 
in the verbose mode and accept the test snapshot. Once you have accepted the
results, there will be `hello.md` file stored in `books/test/example` 
folder and `index.md` in `books` folder containing links to all tests cases. 
Congratulations, you have your first test ready!

After this, you can run the test in a non-verbose and non-interactive mode 
to check that everything works.

```bash
booktest
```

The md files in `book` folder should be added to the version control. 
Remember to add the `books/test/.out` or `.out` into the .gitgnore to avoid
committing temporary test files and caches into the repository

## Configuration

NOTE, that booktest relies on external MD viewer and diff tool. Also, booktest
uses default directory paths for looking up tests, for storing the books and for
storing caches and the output. 

These tools depend on the OS, environment and user preferences. 
To choose tools that work for you, you can run the setup script:

```bash
booktest --setup
```

NOTE: that this operation will create a .booktest file in the local directory. You
can edit the file by hand safely. Rerunning `booktest --setup` will read the configuration
and propose existing as defaults.

NOTE that you can also store a .booktest file in your home directory to provide cross-project 
default settings. These settings will be overriden by project specific .booktest or 
environment variables of form BOOKTEST_VARIABLE_NAME. E.g. BOOKTEST_MD_VIEWER will 
override .booktest file md_viewer configuration.

## Features:

### Headers, anchors and ignored lines

Why? In many test cases there is need to visually organize
the results. There may also be a need to produce pseudorandom
values like time measurements or seeds, that must be compared
against the snapshot.

There may also be a need to produce non-tested content of varying
line length, like logs. Because snasphot testing is done
by comparing test result with snapshot line by line, there
is a need for additional mechanism for resetting the snapshot cursor.
Headers and anchors are used for this purpose

The following test uses demonstrates use of headers 
with `t.h1("title)` call and info/ignored lines 
with `t.iln("ignored")`.

While the testing is normally by comparing the resulting 
file with snapshot file on line by line basis, headers and 
'anchors' make it possible to have variation in the line 
amounts and variation in the content order. 

When testing, the test will simply search for the snapshot
file for the next matching header to continue the test vs
snapshot comparison.

```python
import random as rnd
import time

def headers_test(t):
    rnd.seed(time.time())
    t.h1("This is a test with parts")
    t.tln("Quite nice test")
    
    t.h2("Ignored log")
    for i in range(rnd.randint(1, 5)):
        t.iln(f"log line {i}")
    
    t.h(2, "Tested results")
    t.tln("tested line")
    t.tln("tested line2")
    
    t.h2("Next section has headers and content in random order")
    shuffled = [1, 2, 3]
    rnd.shuffle(shuffled)
    for i in shuffled:
        t.h3(f"header {i}")
        t.tln(f"content {i}")
```
This test produces [following results](books/test/examples/example_suite/headers.md)

There is also separate facility for printing timestamps so 
that you can see the compared snapshot result in the test output: 

```python
import booktest as bt
import time


def test_ms(t: bt.TestCaseRun):
    t.t("sleeping 1 second.. ").imsln(
        lambda: time.sleep(1))
    t.tln()
    t.t("sleeping 1 second.. ").tmsln(
        lambda: time.sleep(1), 3000)
```

This test produces [following results](books/test/examples/example/ms.md)

Note that imsln will never break the test case. tmsln can 
be used to break the test, if the operation takes over specified
millisecond amont

### Build system, dependencies and resources

Why? Big data and long processing times tend to be a common issue plaguing 
data science workflows. The main issue is the slowered down iteration speed. 
This problem can taggled by cacheing intermediate values and splitting 
long operations into smaller intermediate steps that can be tested & iterated
separately. So instead of always running steps A, B and C we create separate
test steps for testing the A, B and C steps separately and caching the results.
By making test C depend on test B, which depend on test A, we can reuse 
results from previous steps in the next step.

Booktest contains a small build system for managing cross test dependencies
and their cacheing. An example of the dependency use can be found 
in `test/examples/simple_book.py` 

In the example, test_cache produces value to cache and test_cache_use uses it.
The test setting makes more sense if you assume test_cache to take lots of time, 
while test_cache_use being a fast operation that you need to iterate & run often.

```python
import booktest as bt


def test_cache(t: bt.TestCaseRun):
    value = "foo"
    t.tln(f"returns '{value}'")
    return value


@bt.depends_on(test_cache)
def test_cache_use(t: bt.TestCaseRun, value: str):
    t.tln(f"got '{value}'")

```

The cached results are stored in `book/.out/test/simple` folder as files
in pickle binary format. 

The test produces 2 different results:

 * [test_cache_file](books/test/examples/simple/cache.md)
 * [test_cache_use](books/test/examples/simple/cache_use.md)

As an addition to managing dependencies, booktest manages exclusive resources 
like ports in order to avoid race conditions or other issues with parallel runs.

When running tests in parallel format, two tests are never scheduled at the same 
time, when an exclusive resources (like a port) is being used. here is an 
example about using a global state parellelization safely using Resources:

```python
from time import sleep

import booktest as bt


class Box:

    def __init__(self, value):
        self.value = value


THE_GLOBAL_BOX = Box(1)


def t_resource_use_with_race_condition(t: bt.TestCaseRun, global_box):
    t.h1("description:")
    t.tln("this test is run several times separately")
    t.tln("there will be race condition, if run parallel")
    t.tln("this test verifies that resource mechanism works")

    t.h1("test sequence:")

    t.tln(f" * the global value is {global_box.value}")
    global_box.value = global_box.value + 1
    t.tln(f" * increased it")
    t.tln(f" * the global value is now {global_box.value}")
    t.tln(f" * sleeping 100 ms")
    sleep(0.1)
    t.tln(f" * the global value is now {global_box.value}")
    t.tln(f" * decreased it")
    global_box.value = global_box.value - 1
    t.tln(f" * the global value is now {global_box.value}")


@bt.depends_on(bt.Resource(THE_GLOBAL_BOX))
def test_resource_use_1(t: bt.TestCaseRun, global_box):
    t_resource_use_with_race_condition(t, global_box)


@bt.depends_on(bt.Resource(THE_GLOBAL_BOX))
def test_resource_use_2(t: bt.TestCaseRun, global_box):
    t_resource_use_with_race_condition(t, global_box)
```

You can find the example code [here](test/examples/resource_book.py) and 
the results [here](books/test/examples/resource) .

### Tables, dataframes and images

Tables can be printed with `t.ttable({"x":[1, 2], "y":[2, 4]})` call, 
while dataframes can be printed with `t.tdf(df)` call as in the following
example:

```python
import booktest as bt
import pandas as pd


def test_df(t: bt.TestCaseRun):
    t.h1("This test demonstrates tables")
    t.tdf(pd.DataFrame({"x": [1, 2, 3], "y": ["foo", "bar", "foobar"]}))
```

This test produces [following results](books/test/examples/example/df.md)

Images can be added to MD file with `t.timage(image_file)`. The image 
needs to be stored into test file directory. You can request test file 
paths with `t.tfile(file_path)` method. Here's example of image use. 

```python
import booktest as bt
import matplotlib.pyplot as plt


def test_image(t: bt.TestCaseRun):

    t.h1("This test demonstrates images")

    file = t.file("figure1.png")
    plt.plot([1, 2, 3], [1, 2, 3])
    plt.savefig(file)
    t.timage(file)
```

This test produces [following results](books/test/examples/example/image.md)

## More documentation

You can find the API documentation for the TestCaseRun class [here](docs/testcaserun.py.md).
This class contains most interesting piece of the API.

You can find more examples in the [test/examples](test/examples) folder. You can 
find the test results [here](books/index.md).
