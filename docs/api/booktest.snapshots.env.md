<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.snapshots.env`





---

## <kbd>function</kbd> `snapshot_env`

```python
snapshot_env(*names)
```






---

## <kbd>function</kbd> `mock_missing_env`

```python
mock_missing_env(env)
```






---

## <kbd>function</kbd> `mock_env`

```python
mock_env(env)
```






---

## <kbd>class</kbd> `SnapshotEnv`




### <kbd>method</kbd> `__init__`

```python
__init__(t: TestCaseRun, names: list)
```








---

### <kbd>method</kbd> `start`

```python
start()
```





---

### <kbd>method</kbd> `stop`

```python
stop()
```





---

### <kbd>method</kbd> `t_snapshots`

```python
t_snapshots()
```

Report snapshot usage to the system instead of printing to test results. 


---

## <kbd>class</kbd> `MockMissingEnv`




### <kbd>method</kbd> `__init__`

```python
__init__(t: TestCaseRun, env: dict)
```








---

### <kbd>method</kbd> `start`

```python
start()
```





---

### <kbd>method</kbd> `stop`

```python
stop()
```






---

## <kbd>class</kbd> `MockEnv`




### <kbd>method</kbd> `__init__`

```python
__init__(env: dict)
```








---

### <kbd>method</kbd> `start`

```python
start()
```





---

### <kbd>method</kbd> `stop`

```python
stop()
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
