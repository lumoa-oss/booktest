<!-- markdownlint-disable -->

<a href="../booktest/testcaserun.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `testcaserun.py`





---

<a href="../booktest/testcaserun.py#L951"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `value_format`

```python
value_format(value)
```






---

## <kbd>class</kbd> `TestCaseRun`
A utility, that manages an invidiual test run, and provides the main API for the test case 

<a href="../booktest/testcaserun.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(run, test_path, config, output)
```








---

<a href="../booktest/testcaserun.py#L563"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `anchor`

```python
anchor(anchor)
```

creates a prefix anchor by seeking & printing prefix. e.g. if you have "key=" anchor, the snapshot cursor will be moved to next line starting with "key=" prefix. 

This method is used for controlling the snapshot cursor location and guaranteeing that a section in test is compared against correct section in the snapshot 

---

<a href="../booktest/testcaserun.py#L575"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `anchorln`

```python
anchorln(anchor)
```

creates a line anchor by seeking & printing an anchor line. e.g. if you have "# SECTION 3" anchor, the snapshot cursor will be moved to next "# SECTION 3" line. 

This method is used for controlling the snapshot cursor location and guaranteeing that a section in test is compared against correct section in the snapshot 

---

<a href="../booktest/testcaserun.py#L816"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `assertln`

```python
assertln(cond, error_message=None)
```

Fails the line if the assertion is false. 

This is typically used in unit testing style assertions like: 

```python
t.t("is HTTP response code 200? ").assertln(response.code() == 200)
``` 

---

<a href="../booktest/testcaserun.py#L293"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `close`

```python
close()
```

Closes all resources (e.g. file system handles). 

---

<a href="../booktest/testcaserun.py#L260"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `close_exp_reader`

```python
close_exp_reader()
```

Closes the expectation/snapshot file reader :return: 

---

<a href="../booktest/testcaserun.py#L430"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `commit_line`

```python
commit_line()
```

Internal method. Commits the prepared line into testing. 

This writes both decorated line into reporting AND this writes the line into test output. Also the snapshot file cursor is moved into next line. 

Statistics line number of differing or erroneous lines get updated. 

---

<a href="../booktest/testcaserun.py#L551"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `diff`

```python
diff()
```

an unexpected difference encountered. this method marks a difference on the line manually  

---

<a href="../booktest/testcaserun.py#L222"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `end`

```python
end()
```

 Test ending step. This records the test time, closes resources,  and sets up preliminary result (FAIL, DIFF, OK). This also  reports the case and calls the review step. s  :return:  



---

<a href="../booktest/testcaserun.py#L557"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `fail`

```python
fail()
```

a proper failure encountered. this method marks an error on the line manually  

---

<a href="../booktest/testcaserun.py#L538"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `feed`

```python
feed(text)
```

Feeds a piece text into the test stream. The text tokenized and feed into text stream as individual tokens. 

NOTE: The token content IS NOT COMPARED to snapshot content, and differences are ignored 

---

<a href="../booktest/testcaserun.py#L492"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `feed_token`

```python
feed_token(token, check=False)
```

Feeds a token into test stream. If `check` is True, the token will be compared to the next awaiting token in the snapshot file, and on difference a 'diff' is reported. 

If `check`is True, snapshot file cursor is also moved, but no comparison is made. 

NOTE: if token is a line end character, the line will be committed to the test stream. 

---

<a href="../booktest/testcaserun.py#L146"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `file`

```python
file(filename)
```

creates a file with the filename in the test's main directory 

these files can include test output or e.g. images and graphs included in the .md output. NOTE: these files may end up in Git, so keep them small and avoid sensitive information. 

---

<a href="../booktest/testcaserun.py#L669"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `h`

```python
h(level, title)
```

Markdown style header at level specified by `level` parameter  

---

<a href="../booktest/testcaserun.py#L674"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `h1`

```python
h1(title)
```

Markdown style header 1st level header 

This method is used to mark titles as in 

```python
t.h1("This is my title")
t.tln("This is my title")
``` 

---

<a href="../booktest/testcaserun.py#L688"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `h2`

```python
h2(title)
```

Markdown style header 2nd level header  

---

<a href="../booktest/testcaserun.py#L693"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `h3`

```python
h3(title)
```

Markdown style header 3rd level header  

---

<a href="../booktest/testcaserun.py#L467"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `head_exp_token`

```python
head_exp_token()
```

Returns the next token in the snapshot file without moving snapshot file cursor 

---

<a href="../booktest/testcaserun.py#L587"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `header`

```python
header(header)
```

creates a header line that also operates as an anchor. 

the only difference between this method and anchorln() method is that the header is preceded and followed by an empty line. 

---

<a href="../booktest/testcaserun.py#L931"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `i`

```python
i(text)
```

Writes the text into test stream without testing the text against snapshot. 

'i' comes from 'info'/'ignore'. 

---

<a href="../booktest/testcaserun.py#L601"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `ifloatln`

```python
ifloatln(value, unit=None)
```





---

<a href="../booktest/testcaserun.py#L940"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `iln`

```python
iln(text='')
```

Writes the text and new line into test stream without testing the text against the snapshot. 

'i' comes from 'info'/'ignore'. 

---

<a href="../booktest/testcaserun.py#L657"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `imsln`

```python
imsln(f)
```

runs the function f and measures the time milliseconds it took. the measurement is printed in the test stream and compared into previous result in the snaphost file. 

This method also prints a new line after the measurements. 

NOTE: unline tmsln(), this method never fails or marks a difference. 

---

<a href="../booktest/testcaserun.py#L876"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `it`

```python
it(name, it)
```

Creates TestIt class around the `it` object named with `name` 

This can be used for assertions as in: 

```python
result = [1, 2]
t.it("result", result).must_be_a(list).must_contain(1).must_contain(2)
``` 

---

<a href="../booktest/testcaserun.py#L620"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `ivalueln`

```python
ivalueln(value, unit=None)
```





---

<a href="../booktest/testcaserun.py#L340"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `jump`

```python
jump(line_number)
```

Moves the snapshot reader cursor to the specified line number. 

If line number is before current reader position, the snapshot file reader is reset. 

---

<a href="../booktest/testcaserun.py#L914"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `keyvalueln`

```python
keyvalueln(key, value)
```

Prints a value of format "{key} {value}", and uses key as prefix anchor for adjusting the snapshot file cursor. 

---

<a href="../booktest/testcaserun.py#L836"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_apply`

```python
must_apply(it, title, cond, error_message=None)
```

Assertions with decoration for testing, whether `it` fulfills a condition. 

Maily used by TestIt class 

---

<a href="../booktest/testcaserun.py#L864"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_be_a`

```python
must_be_a(it, typ)
```

Assertions with decoration for testing, whether `it` is of specific type. 

Maily used by TestIt class 

---

<a href="../booktest/testcaserun.py#L846"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_contain`

```python
must_contain(it, member)
```

Assertions with decoration for testing, whether `it` contains a member. 

Maily used by TestIt class 

---

<a href="../booktest/testcaserun.py#L855"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_equal`

```python
must_equal(it, value)
```

Assertions with decoration for testing, whether `it` equals something. 

Maily used by TestIt class 

---

<a href="../booktest/testcaserun.py#L319"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `next_exp_line`

```python
next_exp_line()
```

Moves snapshot reader cursor to the next snapshot file line 

---

<a href="../booktest/testcaserun.py#L479"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `next_exp_token`

```python
next_exp_token()
```

Reads the next token from the snapshot file. NOTE: this moves snapshot file cursor into the next token. 

---

<a href="../booktest/testcaserun.py#L270"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `open`

```python
open()
```





---

<a href="../booktest/testcaserun.py#L107"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `print`

```python
print(*args, sep=' ', end='\n')
```





---

<a href="../booktest/testcaserun.py#L178"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `rel_path`

```python
rel_path(file)
```

rel_path returns relative path for a file. the returned path that can be referred from the MD file e.g. in images 

---

<a href="../booktest/testcaserun.py#L159"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `rename_file_to_hash`

```python
rename_file_to_hash(file, postfix='')
```

this can be useful with images or similar resources it avoids overwrites (e.g. image.png won't be renamed with image.pnh), guarantees uniqueness and makes the test break whenever image changes. 

---

<a href="../booktest/testcaserun.py#L110"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `report`

```python
report(*args, sep=' ', end='\n')
```

writes a report line in report log and possibly in standard output   

---

<a href="../booktest/testcaserun.py#L116"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `reset_exp_reader`

```python
reset_exp_reader()
```

Resets the reader that reads expectation / snapshot file  

---

<a href="../booktest/testcaserun.py#L204"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `review`

```python
review(result)
```

Internal method: runs the review step, which is done at the end of the test. This method is typically called by end method() 

This step may be interactive depending on the configuration. It ends up with the user or automation accepting or rejecting the result. 

Returns test result (TEST, DIFF, OK) and interaction value, which is used to signal e.g. test run termination. 

---

<a href="../booktest/testcaserun.py#L356"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `seek`

```python
seek(is_line_ok, begin=0, end=9223372036854775807)
```

Seeks the next snapshot/expectation file line that matches the is_line_ok() lambda. The seeking is started on 'begin' line and it ends on the 'end' line. 

NOTE: The seeks starts from the cursor position, but it may restart seeking from the beginning of the file, if the sought line is not found. 

NOTE: this is really an O(N) scanning operation.  it may restart at the beginning of file and  it typically reads the the entire file  on seek failures. 

---

<a href="../booktest/testcaserun.py#L388"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `seek_line`

```python
seek_line(anchor, begin=0, end=9223372036854775807)
```

Seeks the next snapshot/expectation file line matching the anchor. 

NOTE: The seeks starts from the cursor position, but it may restart seeking from the beginning of the file, if the sought line is not found. 

NOTE: this is really an O(N) scanning operation.  it may restart at the beginning of file and  it typically reads the the entire file  on seek failures. 

---

<a href="../booktest/testcaserun.py#L403"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `seek_prefix`

```python
seek_prefix(prefix)
```

Seeks the next snapshot/expectation file line matching the prefix. 

NOTE: The seeks starts from the cursor position, but it may restart seeking from the beginning of the file, if the sought line is not found. 

NOTE: this is really an O(N) scanning operation.  it may restart at the beginning of file and  it typically reads the the entire file  on seek failures. 

---

<a href="../booktest/testcaserun.py#L190"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `start`

```python
start(title=None)
```

Internal method: starts the test run with the given title 

---

<a href="../booktest/testcaserun.py#L889"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `t`

```python
t(text)
```

Writes the text into test stream. NOTE: this will not print a newline. 

---

<a href="../booktest/testcaserun.py#L721"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tdf`

```python
tdf(df)
```

Writes the `df` dataframe as a markdown table. 

NOTE: df should be of pd.DataFrame or compatible type 

---

<a href="../booktest/testcaserun.py#L525"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `test_feed`

```python
test_feed(text)
```

Feeds a piece text into the test stream. The text tokenized and feed into text stream as individual tokens. 

NOTE: The token content IS COMPARED to snapshot content for differences that are reported. 

---

<a href="../booktest/testcaserun.py#L517"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `test_feed_token`

```python
test_feed_token(token)
```

Feeds a token into test stream. The token will be compared to the next awaiting token in the snapshot file, and on difference a 'diff' is reported. 

---

<a href="../booktest/testcaserun.py#L896"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tformat`

```python
tformat(value)
```

Converts the value into json like structure containing only the value types. 

Prints a json containing the value types. 

Mainly used for getting snapshot of a e.g. Json response format. 

---

<a href="../booktest/testcaserun.py#L698"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `timage`

```python
timage(file, alt_text=None)
```

Adds a markdown image in the test stream with specified alt text  

---

<a href="../booktest/testcaserun.py#L760"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tlist`

```python
tlist(list, prefix=' * ')
```

Writes the list into test stream. By default, the list is prefixed by markdown ' * ' list expression. 

For example following call: 

```python
t.tlist(["a", "b", "c"])
``` 

will produce: 

* a * b * c 

---

<a href="../booktest/testcaserun.py#L923"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tln`

```python
tln(text='')
```

Writes the text and new line into test stream. This will commit the test line. 

---

<a href="../booktest/testcaserun.py#L138"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tmp_dir`

```python
tmp_dir(dir_name)
```





---

<a href="../booktest/testcaserun.py#L143"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tmp_file`

```python
tmp_file(filename)
```





---

<a href="../booktest/testcaserun.py#L128"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tmp_path`

```python
tmp_path(name)
```

creates a temporary file with the filename in the test's .tmp directory 

these files get deleted before new runs, and by `booktest --clean` command 

---

<a href="../booktest/testcaserun.py#L634"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tmsln`

```python
tmsln(f, max_ms)
```

runs the function f and measures the time milliseconds it took. the measurement is printed in the test stream and compared into previous result in the snaphost file. 

This method also prints a new line after the measurements. 

NOTE: if max_ms is defined, this line will fail, if the test took more than max_ms milliseconds. 

---

<a href="../booktest/testcaserun.py#L780"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `tset`

```python
tset(items, prefix=' * ')
```

This method used to print and compare a set of items to expected set in out of order fashion. It will first scan the next elements based on prefix. After this step, it will check whether the items were in the list. 

NOTE: this method may be slow, if the set order is unstable. 

---

<a href="../booktest/testcaserun.py#L705"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `ttable`

```python
ttable(table: dict)
```

Writes a markdown table based on the `table` parameter columns. It uses column keys as column names 

```python
t.ttable({
   "x": [1, 2, 3],
   "y": [2, 3, 4]
})
``` 

---

<a href="../booktest/testcaserun.py#L418"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `write_line`

```python
write_line()
```

Internal method. Writes a line into test output file and moves the snaphost line forward by one. 


---

## <kbd>class</kbd> `TestIt`
utility for making assertions related to a specific object  

<a href="../booktest/testcaserun.py#L969"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `__init__`

```python
__init__(run: TestCaseRun, title: str, it)
```








---

<a href="../booktest/testcaserun.py#L991"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `member`

```python
member(title, select)
```

Creates a TestIt class for the member of 'it'  

---

<a href="../booktest/testcaserun.py#L987"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_apply`

```python
must_apply(title, cond)
```





---

<a href="../booktest/testcaserun.py#L983"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_be_a`

```python
must_be_a(typ)
```





---

<a href="../booktest/testcaserun.py#L975"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_contain`

```python
must_contain(member)
```





---

<a href="../booktest/testcaserun.py#L979"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>function</kbd> `must_equal`

```python
must_equal(member)
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
