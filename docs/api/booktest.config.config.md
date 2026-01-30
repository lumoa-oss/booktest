<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.config.config`




**Global Variables**
---------------
- **BOOK_TEST_PREFIX**
- **PROJECT_CONFIG_FILE**
- **DOT_CONFIG_FILE**
- **DEFAULT_CONFIG**
- **DEFAULT_PYTHON_PATH**
- **DEFAULT_TIMEOUT**

---

## <kbd>function</kbd> `parse_config_value`

```python
parse_config_value(value)
```






---

## <kbd>function</kbd> `parse_config_file`

```python
parse_config_file(config_file, config)
```






---

## <kbd>function</kbd> `resolve_default_config`

```python
resolve_default_config()
```






---

## <kbd>function</kbd> `get_default_config`

```python
get_default_config()
```






---

## <kbd>function</kbd> `update_config_value`

```python
update_config_value(config_file: str, key: str, value: str)
```

Update or add a configuration value in a config file. 

This preserves comments and formatting of the config file. 


---

## <kbd>function</kbd> `get_fs_version`

```python
get_fs_version(config_file: str = 'booktest.ini') → str
```

Get the filesystem version from config. 

Returns "v1" (legacy) if not found, "v2" for pytest-style naming. Reads from booktest.ini (project config) as this is project state. 


---

## <kbd>function</kbd> `set_fs_version`

```python
set_fs_version(version: str, config_file: str = 'booktest.ini')
```

Set the filesystem version in config. 

Writes to booktest.ini (project config) as this should be in Git. 


---

## <kbd>function</kbd> `extract_env_vars`

```python
extract_env_vars(config: dict) → dict
```

Extract environment variables from config. 

Supports pytest-style format:  env =  FOO=bar  BAZ=qux 

Also supports legacy env_ prefix format:  env_FOO=bar 

Returns a dictionary of environment variable names to values. 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
