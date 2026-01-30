<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.core.testsuite`





---

## <kbd>function</kbd> `drop_prefix`

```python
drop_prefix(prefix: str, tests: Tests) → Tests
```

removes a prefix like 'test' from all test. this can be used, if the test name inference adds unnecessary decorations to test names. 


---

## <kbd>function</kbd> `cases_of`

```python
cases_of(tests_or_suites) → list
```






---

## <kbd>function</kbd> `merge_tests`

```python
merge_tests(tests_or_suites) → Tests
```

Combines a list of Tests into a single Tests entity 


---

## <kbd>function</kbd> `decorate_tests`

```python
decorate_tests(decorator, tests_or_suites) → Tests
```






---

## <kbd>class</kbd> `TestSuite`




### <kbd>method</kbd> `__init__`

```python
__init__(suite_name, cases)
```











---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
