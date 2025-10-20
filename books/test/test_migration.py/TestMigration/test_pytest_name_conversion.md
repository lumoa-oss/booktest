# Testing pytest_name_to_legacy_path()

Testing conversions:
 ✓ test/foo_test.py::test_bar
   Expected: test/foo/bar
   Actual:   test/foo/bar
 ✓ test/foo_test.py::FooBook/test_bar
   Expected: test/foo/bar
   Actual:   test/foo/bar
 ✓ test/examples/simple_book.py::test_hello
   Expected: test/examples/simple/hello
   Actual:   test/examples/simple/hello
 ✓ test/migration_test.py::test_hello
   Expected: test/migration/hello
   Actual:   test/migration/hello
 ✓ test/migration_test.py::test_snapshot
   Expected: test/migration/snapshot
   Actual:   test/migration/snapshot

✓ All conversion tests passed!
