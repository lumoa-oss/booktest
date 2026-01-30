<!-- markdownlint-disable -->

<a href="../../booktest/reporting/colors.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reporting.colors`
ANSI color code utilities for terminal output. 


---

<a href="../../booktest/reporting/colors.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `colorize`

```python
colorize(text: str, color: str) → str
```

Wrap text with ANSI color codes if color is enabled. 



**Args:**
 
 - <b>`text`</b>:  Text to colorize 
 - <b>`color`</b>:  ANSI color code from Colors class 



**Returns:**
 Colorized text if colors are enabled, otherwise plain text 


---

<a href="../../booktest/reporting/colors.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `red`

```python
red(text: str) → str
```

Colorize text in red (for errors). 


---

<a href="../../booktest/reporting/colors.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `yellow`

```python
yellow(text: str) → str
```

Colorize text in yellow (for diffs). 


---

<a href="../../booktest/reporting/colors.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `green`

```python
green(text: str) → str
```

Colorize text in green. 


---

<a href="../../booktest/reporting/colors.py#L92"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `blue`

```python
blue(text: str) → str
```

Colorize text in blue. 


---

<a href="../../booktest/reporting/colors.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `gray`

```python
gray(text: str) → str
```

Colorize text in gray. 


---

<a href="../../booktest/reporting/colors.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `cyan`

```python
cyan(text: str) → str
```

Colorize text in cyan. 


---

<a href="../../booktest/reporting/colors.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `white`

```python
white(text: str) → str
```

Colorize text in bright white. 


---

<a href="../../booktest/reporting/colors.py#L112"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `dim_gray`

```python
dim_gray(text: str) → str
```

Colorize text in dim gray (more subtle than regular gray). 


---

<a href="../../booktest/reporting/colors.py#L119"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `default_color`

```python
default_color(text: str) → str
```

Return text in terminal's default color (adapts to light/dark themes). 


---

<a href="../../booktest/reporting/colors.py#L126"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `is_color_enabled`

```python
is_color_enabled() → bool
```

Check if color output is enabled. 


---

<a href="../../booktest/reporting/colors.py#L131"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `set_color_enabled`

```python
set_color_enabled(enabled: bool)
```

Override color support detection. 



**Args:**
 
 - <b>`enabled`</b>:  True to enable colors, False to disable 


---

<a href="../../booktest/reporting/colors.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Colors`
ANSI color codes for terminal output. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
