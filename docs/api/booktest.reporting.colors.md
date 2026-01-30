<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.reporting.colors`
ANSI color code utilities for terminal output. 


---

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

## <kbd>function</kbd> `red`

```python
red(text: str) → str
```

Colorize text in red (for errors). 


---

## <kbd>function</kbd> `yellow`

```python
yellow(text: str) → str
```

Colorize text in yellow (for diffs). 


---

## <kbd>function</kbd> `green`

```python
green(text: str) → str
```

Colorize text in green. 


---

## <kbd>function</kbd> `blue`

```python
blue(text: str) → str
```

Colorize text in blue. 


---

## <kbd>function</kbd> `gray`

```python
gray(text: str) → str
```

Colorize text in gray. 


---

## <kbd>function</kbd> `cyan`

```python
cyan(text: str) → str
```

Colorize text in cyan. 


---

## <kbd>function</kbd> `white`

```python
white(text: str) → str
```

Colorize text in bright white. 


---

## <kbd>function</kbd> `dim_gray`

```python
dim_gray(text: str) → str
```

Colorize text in dim gray (more subtle than regular gray). 


---

## <kbd>function</kbd> `default_color`

```python
default_color(text: str) → str
```

Return text in terminal's default color (adapts to light/dark themes). 


---

## <kbd>function</kbd> `is_color_enabled`

```python
is_color_enabled() → bool
```

Check if color output is enabled. 


---

## <kbd>function</kbd> `set_color_enabled`

```python
set_color_enabled(enabled: bool)
```

Override color support detection. 



**Args:**
 
 - <b>`enabled`</b>:  True to enable colors, False to disable 


---

## <kbd>class</kbd> `Colors`
ANSI color codes for terminal output. 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
