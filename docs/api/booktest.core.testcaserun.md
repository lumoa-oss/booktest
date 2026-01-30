<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.core.testcaserun`




**Global Variables**
---------------
- **DIFF_POSITION**


---

## <kbd>class</kbd> `TestCaseRun`
A utility, that manages an invidiual test run, and provides the main API for the test case 

### <kbd>method</kbd> `__init__`

```python
__init__(run, test_path, config, output)
```








---

### <kbd>method</kbd> `anchor`

```python
anchor(anchor)
```

creates a prefix anchor by seeking & printing prefix. e.g. if you have "key=" anchor, the snapshot cursor will be moved to next line starting with "key=" prefix. 

This method is used for controlling the snapshot cursor location and guaranteeing that a section in test is compared against correct section in the snapshot 

---

### <kbd>method</kbd> `anchorln`

```python
anchorln(anchor)
```

creates a line anchor by seeking & printing an anchor line. e.g. if you have "# SECTION 3" anchor, the snapshot cursor will be moved to next "# SECTION 3" line. 

This method is used for controlling the snapshot cursor location and guaranteeing that a section in test is compared against correct section in the snapshot 

---

### <kbd>method</kbd> `close`

```python
close()
```

Closes all resources (e.g. file system handles). 

---

### <kbd>method</kbd> `close_exp_reader`

```python
close_exp_reader()
```

Closes the expectation/snapshot file reader :return: 

---

### <kbd>method</kbd> `commit_line`

```python
commit_line()
```

Internal method. Commits the prepared line into testing. 

This writes both decorated line into reporting AND this writes the line into test output. Also the snapshot file cursor is moved into next line. 

Statistics line number of differing or erroneous lines get updated. 

Uses token-level markers for fine-grained coloring of specific tokens/cells that changed, failed, or have info-level differences. 

---

### <kbd>method</kbd> `diff`

```python
diff()
```

Mark the entire line as different from position 0 to end. 

Adds a marker (0, MAX_SIZE, 'diff') that colors the entire line yellow. Individual token markers with higher priority will override this. 

---

### <kbd>method</kbd> `diff_token`

```python
diff_token()
```

Mark only the current token/position as different. 

Use this for fine-grained diff marking, e.g., to highlight a specific changed cell in a table without marking the entire row as different. 

Note: This should be called AFTER adding the token to out_line to properly capture the token length. Prefer using feed_token with check=True. 

---

### <kbd>method</kbd> `end`

```python
end()
```

Test ending step. This records the test time, closes resources, and sets up preliminary result (FAIL, DIFF, OK). This also reports the case and calls the review step. 

:return: (result, interaction) where result can be legacy TestResult or TwoDimensionalTestResult 

---

### <kbd>method</kbd> `f`

```python
f(text)
```

Writes failed text inline (primitive method for OutputWriter). 

In TestCaseRun, all tokens are marked as failed and colored red. 'f' comes from 'fail'. 

---

### <kbd>method</kbd> `fail`

```python
fail()
```

Mark the entire line as failed from position 0 to end. 

Adds a marker (0, MAX_SIZE, 'fail') that colors the entire line red. Individual token markers with higher priority will override this. 

---

### <kbd>method</kbd> `fail_feed`

```python
fail_feed(text)
```

Feeds text into the stream and marks all tokens as failed (red). Use this to write error messages or failed output. 

---

### <kbd>method</kbd> `fail_feed_token`

```python
fail_feed_token(token)
```

Feeds a token into the stream and marks it as failed. The token will be colored red in the output. 

---

### <kbd>method</kbd> `fail_token`

```python
fail_token()
```

Mark only the current token/position as failed. 

Use this for fine-grained failure marking, e.g., to highlight a specific failed assertion in a table cell without marking the entire row as failed. 

Note: This should be called AFTER adding the token to out_line to properly capture the token length. Prefer using feed_token with check=True. 

---

### <kbd>method</kbd> `feed`

```python
feed(text)
```

Feeds a piece text into the info stream. The text tokenized and feed into text stream as individual tokens. 

NOTE: The token content IS NOT COMPARED to snapshot content, and differences are ignored 

---

### <kbd>method</kbd> `feed_token`

```python
feed_token(token, check=False, info_check=False)
```

Feeds a token into test stream with optional comparison. 



**Args:**
 
 - <b>`token`</b>:  The token to feed 
 - <b>`check`</b>:  If True, compare against snapshot and mark diff() on mismatch 
 - <b>`info_check`</b>:  If True, compare against snapshot and mark info() on mismatch  (shows in diff without failing test) 

NOTE: if token is a line end character, the line will be committed to the test stream. 

---

### <kbd>method</kbd> `file`

```python
file(filename)
```

creates a file with the filename in the test's main directory 

these files can include test output or e.g. images and graphs included in the .md output. NOTE: these files may end up in Git, so keep them small and avoid sensitive information. 

---

### <kbd>method</kbd> `get_snapshot_state`

```python
get_snapshot_state() → <enum 'SnapshotState'>
```

Determine overall snapshot state from tracked usage. 



**Returns:**
 
 - <b>`SnapshotState`</b>:  INTACT if all snapshots valid, UPDATED if any updated,  FAIL if any failed 

---

### <kbd>method</kbd> `get_storage`

```python
get_storage()
```

Get the storage backend for this test. 



**Returns:**
 
 - <b>`SnapshotStorage`</b>:  The storage instance 

---

### <kbd>method</kbd> `h`

```python
h(level: int, title: str)
```

Markdown style header (primitive method for OutputWriter). 

This method is used to mark titles. Use h1(), h2(), h3() convenience methods instead. 

```python
t.h1("This is my title")
t.h2("Subsection")
``` 

---

### <kbd>method</kbd> `head_exp_token`

```python
head_exp_token()
```

Returns the next token in the snapshot file without moving snapshot file cursor 

---

### <kbd>method</kbd> `i`

```python
i(text)
```

Writes info text inline (primitive method for OutputWriter). 

In TestCaseRun, differences in info content are marked with info markers (shown in diff without causing test failure). 'i' comes from 'info'/'ignore'. 

---

### <kbd>method</kbd> `info`

```python
info()
```

Mark the entire line as having info-level differences from position 0 to end. 

Adds a marker (0, MAX_SIZE, 'info') that colors the entire line cyan. Individual token markers with higher priority will override this. 

Info markers show differences in diagnostic output (i() content) that don't cause test failure. 

---

### <kbd>method</kbd> `info_feed`

```python
info_feed(text)
```

Feeds a piece text into the info stream with comparison. The text is tokenized and compared to snapshot content. Differences are marked as 'info' (shown in diff without causing test failure). 

Use this for diagnostic output that should be tracked but not cause failures. 

---

### <kbd>method</kbd> `info_feed_token`

```python
info_feed_token(token)
```

Feeds a token into info stream. The token will be compared to the next awaiting token in the snapshot file, but differences are marked as 'info' (shown in diff without causing test failure). 

---

### <kbd>method</kbd> `info_token`

```python
info_token()
```

Mark only the current token/position as having info-level differences. 

Use this for fine-grained info marking, e.g., to highlight which specific cell in a diagnostic table changed without affecting the test result. 

Note: This should be called AFTER adding the token to out_line to properly capture the token length. Prefer using feed_token with info_check=True. 

---

### <kbd>method</kbd> `jump`

```python
jump(line_number)
```

Moves the snapshot reader cursor to the specified line number. 

If line number is before current reader position, the snapshot file reader is reset. 

---

### <kbd>method</kbd> `next_exp_line`

```python
next_exp_line()
```

Moves snapshot reader cursor to the next snapshot file line 

---

### <kbd>method</kbd> `next_exp_token`

```python
next_exp_token()
```

Reads the next token from the snapshot file. NOTE: this moves snapshot file cursor into the next token. 

---

### <kbd>method</kbd> `open`

```python
open()
```





---

### <kbd>method</kbd> `print`

```python
print(*args, sep=' ', end='\n')
```





---

### <kbd>method</kbd> `rel_path`

```python
rel_path(file)
```

rel_path returns relative path for a file. the returned path that can be referred from the MD file e.g. in images 

---

### <kbd>method</kbd> `rename_file_to_hash`

```python
rename_file_to_hash(file, postfix='')
```

this can be useful with images or similar resources it avoids overwrites (e.g. image.png won't be renamed with image.pnh), guarantees uniqueness and makes the test break whenever image changes. 

---

### <kbd>method</kbd> `report`

```python
report(*args, sep=' ', end='\n')
```

writes a report line in report log and possibly in standard output   

---

### <kbd>method</kbd> `report_snapshot_usage`

```python
report_snapshot_usage(
    snapshot_type: str,
    hash_value: str,
    state: SnapshotState,
    details: dict = None
)
```

Report snapshot usage for this test. 



**Args:**
 
 - <b>`snapshot_type`</b>:  Type of snapshot (http, httpx, env, func) 
 - <b>`hash_value`</b>:  SHA256 hash of snapshot content 
 - <b>`state`</b>:  Current state (INTACT, UPDATED, FAIL) 
 - <b>`details`</b>:  Optional additional information about the snapshot 

---

### <kbd>method</kbd> `reset_exp_reader`

```python
reset_exp_reader()
```

Resets the reader that reads expectation / snapshot file  

---

### <kbd>method</kbd> `review`

```python
review(result)
```

Internal method: runs the review step, which is done at the end of the test. This method is typically called by end method() 

This step may be interactive depending on the configuration. It ends up with the user or automation accepting or rejecting the result. 

Returns test result (TEST, DIFF, OK) and interaction value, which is used to signal e.g. test run termination. 

---

### <kbd>method</kbd> `seek`

```python
seek(is_line_ok, begin=0, end=9223372036854775807)
```

Seeks the next snapshot/expectation file line that matches the is_line_ok() lambda. The seeking is started on 'begin' line and it ends on the 'end' line. 

NOTE: The seeks starts from the cursor position, but it may restart seeking from the beginning of the file, if the sought line is not found. 

NOTE: this is really an O(N) scanning operation.  it may restart at the beginning of file and  it typically reads the the entire file  on seek failures. 

---

### <kbd>method</kbd> `seek_line`

```python
seek_line(anchor, begin=0, end=9223372036854775807)
```

Seeks the next snapshot/expectation file line matching the anchor. 

NOTE: The seeks starts from the cursor position, but it may restart seeking from the beginning of the file, if the sought line is not found. 

NOTE: this is really an O(N) scanning operation.  it may restart at the beginning of file and  it typically reads the the entire file  on seek failures. 

---

### <kbd>method</kbd> `seek_prefix`

```python
seek_prefix(prefix)
```

Seeks the next snapshot/expectation file line matching the prefix. 

NOTE: The seeks starts from the cursor position, but it may restart seeking from the beginning of the file, if the sought line is not found. 

NOTE: this is really an O(N) scanning operation.  it may restart at the beginning of file and  it typically reads the the entire file  on seek failures. 

---

### <kbd>method</kbd> `start`

```python
start(title=None)
```

Internal method: starts the test run with the given title 

---

### <kbd>method</kbd> `start_review`

```python
start_review(llm=None)
```

Start an LLM-assisted review session. 

Returns an LlmReview instance that accumulates output and can use an LLM to answer questions about the test results. 



**Args:**
 
 - <b>`llm`</b>:  Optional Llm instance. If None, uses get_llm() default. 



**Returns:**
 
 - <b>`LlmReview`</b>:  Review instance for writing output and performing LLM-based validation 



**Example:**
 def test_code_generation(t: bt.TestCaseRun):  r = t.start_review() 

 r.h1("Generated Code:")  r.icode(code, "python") 

 r.start_review()  r.reviewln("Is code well formatted?", "Yes", "No") 

For GPT/Azure OpenAI (default LLM), requires: 
    - openai package 
    - Environment variables: OPENAI_API_KEY, OPENAI_API_BASE, etc. 

---

### <kbd>method</kbd> `t`

```python
t(text)
```

Writes tested text inline (primitive method for OutputWriter). 

In TestCaseRun, this text is compared against snapshots. 

---

### <kbd>method</kbd> `test_feed`

```python
test_feed(text)
```

Feeds a piece text into the test stream. The text tokenized and feed into text stream as individual tokens. 

NOTE: The token content IS COMPARED to snapshot content for differences that are reported. 

---

### <kbd>method</kbd> `test_feed_token`

```python
test_feed_token(token)
```

Feeds a token into test stream. The token will be compared to the next awaiting token in the snapshot file, and on difference a 'diff' is reported. 

---

### <kbd>method</kbd> `tmp_dir`

```python
tmp_dir(dir_name)
```





---

### <kbd>method</kbd> `tmp_file`

```python
tmp_file(filename)
```





---

### <kbd>method</kbd> `tmp_path`

```python
tmp_path(name)
```

creates a temporary file with the filename in the test's .tmp directory 

these files get deleted before new runs, and by `booktest --clean` command 

---

### <kbd>method</kbd> `write_line`

```python
write_line()
```

Internal method. Writes a line into test output file and moves the snaphost line forward by one. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
