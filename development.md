# Developing booktest

This guides through the basic steps of building booktest locally and 
running it's tests.

## dependencies

You will need uv and Python 3.10+ to use this package. To setup the environment
and install dependencies, run:

```bash
uv sync
```


## Testing

booktest uses booktest for testing. To configure booktest, see the instructions above.

To run the test cases, run:

```bash
booktest test
```

The tests are run against expectation files, which 
represent test snapshots and have been generated
from previous runs. 

Click [here](books/index.md) to see the booktest test cases
expectation files.

## Regenerating documentation

Install lazydocs and run:

```bash
lazydocs `find booktest -name '*.py' `
```

## Contributing

If you want to contribute, please contact Antti Rauhala (antti.rauhala at netigate.net)