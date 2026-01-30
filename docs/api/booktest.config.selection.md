<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.config.selection`





---

## <kbd>function</kbd> `is_selected`

```python
is_selected(test_name, selection)
```

checks whether the test name is selected based on the selection 

Supports both pytest format (test/foo_test.py::test_bar) and legacy format (test/foo/bar). 


---

## <kbd>function</kbd> `match_selection_with_test_suite_name`

```python
match_selection_with_test_suite_name(s, test_suite_name)
```






---

## <kbd>function</kbd> `is_selected_test_suite`

```python
is_selected_test_suite(test_suite_name, selection)
```

checks whether the test suiite is selected based on the selection 

Supports both pytest format (test/foo_test.py::TestClass) and legacy format (test/foo). 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
