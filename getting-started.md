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

### Build system and dependencies

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

### Resources

As an addition to managing dependencies, booktest manages exclusive resources 
like ports in order to avoid race conditions or other issues with parallel runs.

When running tests in parallel format, two tests are never scheduled at the same 
time, when an exclusive resources (like a port) is being used. here is an 
example about using a global state parellelization safely using Resources:

Following example demonstrates that how resource pool can be used to avoid 
port conflicts in parallel runs. 

```python
import socket
from time import sleep
import booktest as bt


PORT_POOL = bt.port_range(10000, 10002)


def t_open_server_socket(t: bt.TestCaseRun, port):
    server_socket = \
        t.t(f" * creating server socket..").imsln(
            lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    try:
        # Bind the socket to the specified port
        t.t(f" * binding the socket in port ").i(f"{port}..").imsln(
            lambda: server_socket.bind(('localhost', port)))
        # Start listening for connections
        t.t(f" * start listening to the connection..").imsln(
            lambda: server_socket.listen(1))
        t.t(" * server socket opened at port ").iln(f"{port}")

        # Keep the socket open for 300 milliseconds
        t.t(" * sleeping for 100 milliseconds..").imsln(
            lambda: sleep(0.1))
    finally:
        # Close the socket
        server_socket.close()
        t.t(" * server socket closed at port ").iln(f"{port}.")

@bt.depends_on(PORT_POOL)
def test_port_pool_1(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)

@bt.depends_on(PORT_POOL)
def test_port_pool_2(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)

@bt.depends_on(PORT_POOL)
def test_port_pool_3(t: bt.TestCaseRun, port):
    t_open_server_socket(t, port)
```

You can find the example code [here](test/examples/resource_book.py) and 
the results [here](books/test/examples/resource) .

Check also Pool resources like `port_range(10000, 10100)`. You can find example code [here](test/examples/pool_book.py) 
and results [here](books/test/examples/pool/). Port pool can be used to allocate a port range to be used
in your tests without port collisions. 

Other use cases for resources are preventing two tests of e.g. using GPU, external service, a file or too much RAM at the same time.


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

### Snapshots

In real life testing setting, the system may be dependent on external dependencies like
internal or public HTTP servers and environment variables related to these resources. 

Booktest provides HTTP snapshotting and environment variable snapshot for providing
a simple way for mocking the variables and services. 

Here is an example of using both environment and request snapshotting for creating tests
using live HTTP service with an api key. 

```python
import booktest as bt
import os 
import requests
import json

@bt.snapshot_env("HOST_NAME")
@bt.mock_missing_env({"API_KEY": "mock"})
@bt.snapshot_requests()
def test_requests_and_env(t: bt.TestCaseRun):
    t.h1("request:")

    host_name = os.environ["HOST_NAME"]
    response = (
        t.t(f"making post request to {host_name} in ").imsln(
            lambda:
            requests.post(
                host_name,
                json={
                    "message": "hello"
                },
                headers={
                    "X-Api-Key": os.environ["API_KEY"]
                })))

    t.h1("response:")
    t.tln(json.dumps(response.json()["json"], indent=4))

```

This test produces [following results](books/test/examples/snapshots/requests_and_env.md)

In the example, HOST_NAME is captured using bt.snaphot_env decoration and the 
http request is captured using the snaphot_requests. 

NOTE: X-Api-Key is not captured, but a mock value is provided instead, whenever the test
is not in a snapshot capture mode. 

Also, both HTTP headers are ignored by default to avoid leaking information about secrets
via SHA-1 encoded hashes and to match requests independent of variable header details.
You can check the example for more selective HTTP header selection in case the response 
depends on the header content.

When developing code with snapshots, note, that you need special flags for snapshots
library to be completed with snapshots or to recreate old ones. 

You can capture missing snapshots with '-s' flag as in 

```bash
booktest -v -i -s test/examples/snapshots/requests_and_env
```

Or you completely recapture the snapshots with '-S' flag as in:

```bash
HOST_NAME="https://httpbin.org/anything" API_KEY="secret" booktest -v -i -S test/examples/snapshots/requests_and_env
```

Remember to provide access to hosts and the missing environment variables, when updating snapshots.

#### Other snapshot targets:

It's common in data science to run into algorithms that are non-deterministic. They may be non-deterministic
even with fixed seeds, as the specifics may depend on optimizations, which may depend on hardware. Normal 
function calls can also be snapshotted as in the following example: 

```python
import booktest as bt
import time
import random

def non_deterministic_and_slow_algorithm(input):
    rnd = random.Random(input)
    noise = random.Random(int(time.time()))

    rv = []
    for i in range(rnd.randint(0, 3) + 1 + noise.randint(0, 1)):
        rv.append(rnd.randint(0, 10000) + noise.randint(-1, 1))
        time.sleep(1)

    return rv


def multiargs(a, b, c, *args, **kwargs):
    return { "a": a, "b": b, "c": c, "args": list(args), "kwargs": kwargs }


@bt.snapshot_functions(time.time_ns,
                       random._inst.random,
                       non_deterministic_and_slow_algorithm,
                       multiargs)
def test_auto_function_snapshots(t: bt.TestCaseRun):
    t.h1("snapshots:")

    t.keyvalueln(" * timestamp:", time.time_ns())
    t.keyvalueln(" * random:", random._inst.random())

    t.h1("algorithm snapshot:")

    result = (
        t.t(" * calculating result..").imsln(
            lambda: non_deterministic_and_slow_algorithm(124)))

    t.keyvalueln(" * result:", result)

    t.h1("args:")
    t.keyvalueln(" * args: 123:", multiargs(1, 2, 3))
    t.keyvalueln(" * args: 12345:", multiargs(1, 2, 3, 4, 5))
    t.keyvalueln(" * named args:", multiargs(a=1, b=2, c=3, d=4, e=5))
```

NOTE: currently, the inputs and outputs are stored in json format, which limits what can be snapshotted. 

Also httpx snapshotting is supported, which is useful when making snaphots of e.g. GPT requests. 

```python
import booktest as bt
import httpx 
import json

@bt.snapshot_httpx()
def test_httpx(t: bt.TestCaseRun):
    response = httpx.get("https://api.weather.gov/")

    t.h1("response:")
    t.tln(json.dumps(response.json(), indent=4))
```

### Async support

Booktest has async support, and it can run async tests.

```python
import booktest as bt
import asyncio
import time


async def test_wait(t: bt.TestCaseRun):
    t.h1("async test:")

    t.t(" * waiting on async io..")
    before = time.time()
    await asyncio.sleep(0.1)
    after = time.time()
    t.ifloatln(after-before, "s")

    t.tln(" * done")
```

If you need to call booktest in from asynchronous code, 
you can run_async method. 

### Process setup and teardown 

A test may be dependent on some global values or initializations, which may lead to issues when using parallel processing. 
Booktest has a simplistic mechanism for providing setup and teardown functionality via __booktest__.py file. If the fil
contains a function named process_setup_teardown, this will be called for each test process to setup the 
environment.

Here's an example of the __booktest__.py file:

```python
def process_setup_teardown():
    from test.global_value import set_global_value
    set_global_value("set")
    yield
    set_global_value("unset")
```

Here's example of a test, which verifies that the process is setup correctly. 

```python
import booktest as bt
from test.global_value import get_global_value


def test_setup_teardown(t: bt.TestCaseRun):
    t.h1("description:")
    t.tln("global operations are needed to things like faking system times")
    t.tln("or initializing resources. ")
    t.tln()
    t.tln("booktest allows user to define process_setup_teardown in __booktest__.py")
    t.tln("to set up and teardown global settings")

    t.h1("test:")
    t.tln("the global variable should always be 'set'")
    t.tln()

    value = get_global_value()

    t.t(f"global variable is '{value}'..").assertln(value == 'set')
```

## More documentation

You can find the API documentation for the TestCaseRun class [here](docs/testcaserun.py.md).
This class contains most interesting piece of the API.

You can find more examples in the [test/examples](test/examples) folder. You can 
find the test results [here](books/index.md).
