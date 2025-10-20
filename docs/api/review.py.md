<!-- markdownlint-disable -->

<a href="../booktest/review.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `review.py`




**Global Variables**
---------------
- **BOOK_TEST_PREFIX**

---

<a href="../booktest/review.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `run_tool`

```python
run_tool(config, tool, args)
```

Run a tool used in reviews  


---

<a href="../booktest/review.py#L28"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `interact`

```python
interact(exp_dir, out_dir, case_name, test_result, config)
```






---

<a href="../booktest/review.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `freeze_case`

```python
freeze_case(exp_dir, out_dir, case_name)
```






---

<a href="../booktest/review.py#L101"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `case_review`

```python
case_review(exp_dir, out_dir, case_name, test_result, config)
```






---

<a href="../booktest/review.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `start_report`

```python
start_report(printer)
```






---

<a href="../booktest/review.py#L134"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `report_case_begin`

```python
report_case_begin(printer, case_name, title, verbose)
```






---

<a href="../booktest/review.py#L147"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `report_case_result`

```python
report_case_result(printer, case_name, result, took_ms, verbose)
```






---

<a href="../booktest/review.py#L168"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `maybe_print_logs`

```python
maybe_print_logs(printer, config, out_dir, case_name)
```






---

<a href="../booktest/review.py#L193"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `report_case`

```python
report_case(printer, exp_dir, out_dir, case_name, result, took_ms, config)
```






---

<a href="../booktest/review.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `end_report`

```python
end_report(printer, failed, tests, took_ms)
```






---

<a href="../booktest/review.py#L244"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `create_index`

```python
create_index(dir, case_names)
```






---

<a href="../booktest/review.py#L275"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `review`

```python
review(exp_dir, out_dir, config, passed, cases=None)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
