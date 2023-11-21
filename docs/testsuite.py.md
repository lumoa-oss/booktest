<!-- markdownlint-disable -->

<a href="../booktest/testsuite.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `testsuite.py`





---

<a href="../booktest/testsuite.py#L17"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `drop_prefix`

```python
drop_prefix(prefix: str, tests: Tests) → Tests
```

removes a prefix like 'test' from all test. this can be used, if the test name inference adds unnecessary decorations to test names. 


---

<a href="../booktest/testsuite.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `merge_tests`

```python
merge_tests(suites: list) → Tests
```

Combines a list of Tests into a single Tests entity 


---

## <kbd>class</kbd> `TestSuite`




<a href="../booktest/testsuite.py#L6"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(suite_name, cases)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
