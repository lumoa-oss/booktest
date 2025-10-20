# match_selection_with_test_suite_name Tests


## Basic Directory Matching

Testing basic directory matching:
 ✓ 'test' matches 'test/test_foo.py'
    selection='test', test_suite='test/test_foo.py' → True
 ✓ 'test' matches nested paths
    selection='test', test_suite='test/subdir/test_bar.py' → True
 ✓ exact directory prefix
    selection='test/subdir', test_suite='test/subdir/test_bar.py' → True
 ✓ 'other' doesn't match 'test/*'
    selection='other', test_suite='test/test_foo.py' → False
 ✓ '*' matches everything
    selection='*', test_suite='test/test_foo.py' → True
 ✓ '*' matches any path
    selection='*', test_suite='anywhere/test.py' → True


## Pytest-Style Class Matching

Testing pytest-style class matching:
 ✓ exact class match
    selection='test/test_foo.py::FooClass', test_suite='test/test_foo.py::FooClass' → True
 ✓ different class names
    selection='test/test_foo.py::FooClass', test_suite='test/test_foo.py::BarClass' → False
 ✓ file selection DOES match classes in that file
    selection='test/test_foo.py', test_suite='test/test_foo.py::FooClass' → True
 ✓ method selection matches class (forward slash)
    selection='test/test_foo.py::FooClass/test_bar', test_suite='test/test_foo.py::FooClass' → True


## Edge Cases

Testing edge cases:
 ✓ empty selection matches everything
    selection='', test_suite='test/test_foo.py' → True
 ✓ trailing slash doesn't match (exact path mismatch)
    selection='test/', test_suite='test/test_foo.py' → False
 ✓ directory prefix matches file in directory
    selection='test/examples', test_suite='test/examples/foo_test.py' → True
 ✓ partial directory name doesn't match (must have / boundary)
    selection='test/examples', test_suite='test/examples_other/foo_test.py' → False
 ✓ incomplete directory name doesn't match
    selection='test/exa', test_suite='test/examples/foo_test.py' → False
 ✓ case sensitive - 'Test' != 'test'
    selection='Test', test_suite='test/test_foo.py' → False
 ✓ partial class name doesn't match (Bar != BarClass)
    selection='test/foo_test.py::Bar', test_suite='test/foo_test.py::BarClass' → False
 ✓ exact class name matches
    selection='test/foo_test.py::BarClass', test_suite='test/foo_test.py::BarClass' → True


## Real-World Selection Patterns

Testing real-world selection patterns:
 ✓ selecting 'test' includes datascience subdirectory
    selection='test', test_suite='test/datascience/test_gpt.py' → True
 ✓ selecting subdirectory includes files in it
    selection='test/datascience', test_suite='test/datascience/test_gpt.py' → True
 ✓ selecting subdirectory includes nested files
    selection='test/datascience', test_suite='test/datascience/agents/test_agent.py' → True
 ✓ selecting file DOES match classes in that file
    selection='test/datascience/test_gpt.py', test_suite='test/datascience/test_gpt.py::TestGPT' → True
 ✓ selecting class with :: matches exactly
    selection='test/datascience/test_gpt.py::TestGPT', test_suite='test/datascience/test_gpt.py::TestGPT' → True
 ✓ directory selection matches nested suite
    selection='test/examples', test_suite='test/examples/example_suite/simple' → True
 ✓ nested directory selection
    selection='test/examples/example_suite', test_suite='test/examples/example_suite/simple' → True

✓ All match_selection_with_test_suite_name tests passed!
