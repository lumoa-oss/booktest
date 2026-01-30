<!-- markdownlint-disable -->

<a href="../../booktest/config/selection.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `config.selection`





---

<a href="../../booktest/config/selection.py#L1"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_selected`

```python
is_selected(test_name, selection)
```

checks whether the test name is selected based on the selection 

Supports both pytest format (test/foo_test.py::test_bar) and legacy format (test/foo/bar). 


---

<a href="../../booktest/config/selection.py#L47"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `match_selection_with_test_suite_name`

```python
match_selection_with_test_suite_name(s, test_suite_name)
```






---

<a href="../../booktest/config/selection.py#L62"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_selected_test_suite`

```python
is_selected_test_suite(test_suite_name, selection)
```

checks whether the test suiite is selected based on the selection 

Supports both pytest format (test/foo_test.py::TestClass) and legacy format (test/foo). 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
