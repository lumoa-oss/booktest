<!-- markdownlint-disable -->

# <kbd>module</kbd> `booktest.llm.llm`
LLM abstraction for booktest. 

This module provides an abstract LLM interface and implementations for different LLM providers. The default LLM can be configured globally. 


---

## <kbd>function</kbd> `get_llm`

```python
get_llm() → Llm
```

Get the default LLM instance. 

The instance is cached for efficiency. To reset the cache (e.g., after environment variables change), call set_llm(None). 

Auto-detects the LLM provider based on environment variables: 1. ANTHROPIC_API_KEY -> ClaudeLlm 2. OLLAMA_HOST or OLLAMA_MODEL -> OllamaLlm 3. Otherwise -> GptLlm (Azure OpenAI) 

You can override with set_llm_factory() to use a specific LLM class. 



**Returns:**
  The cached LLM instance 


---

## <kbd>function</kbd> `set_llm`

```python
set_llm(llm: Optional[Llm])
```

Set a specific LLM instance to use globally. 



**Args:**
 
 - <b>`llm`</b>:  The LLM instance to use, or None to reset cache 


---

## <kbd>function</kbd> `set_llm_factory`

```python
set_llm_factory(factory: Optional[Callable[[], Llm]])
```

Set which LLM class to use without creating an instance immediately. 

The factory is called once when get_llm() is first invoked (after any cache reset). The created instance is then cached. 



**Args:**
 
 - <b>`factory`</b>:  A callable that returns an Llm (e.g., bt.GptLlm, bt.ClaudeLlm),  or None to reset to auto-detection 



**Example:**
 # Use GPT regardless of environment bt.set_llm_factory(bt.GptLlm) 

# Use Claude bt.set_llm_factory(bt.ClaudeLlm) 

# Custom configuration bt.set_llm_factory(lambda: bt.OllamaLlm(model="codellama")) 


---

## <kbd>function</kbd> `use_llm`

```python
use_llm(llm: Llm)
```

Decorator to set the LLM for a specific test function. 

This decorator temporarily sets the default LLM for the duration of the test, then restores the previous default when the test completes. Works with both sync and async test functions. 



**Args:**
 
 - <b>`llm`</b>:  The LLM instance to use for this test 



**Example:**
 @bt.use_llm(my_custom_llm) def test_agent(t: bt.TestCaseRun):  r = t.start_review()  r.reviewln("Is output correct?", "Yes", "No") 

@bt.use_llm(my_custom_llm) async def test_async_agent(t: bt.TestCaseRun):  r = t.start_review()  r.reviewln("Is output correct?", "Yes", "No") 


---

## <kbd>class</kbd> `Llm`
Abstract base class for LLM providers. 

Subclasses must implement the prompt() method to interact with their specific LLM backend. 




---

### <kbd>method</kbd> `prompt`

```python
prompt(request: str, max_completion_tokens: int = 2048) → str
```

Send a prompt to the LLM and get a response. 



**Args:**
 
 - <b>`request`</b>:  The prompt text to send to the LLM 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for the LLM's response 



**Returns:**
 The LLM's response as a string 

---

### <kbd>method</kbd> `prompt_json`

```python
prompt_json(
    request: str,
    required_fields: List[str] = None,
    validator: Callable[[dict], bool] = None,
    max_retries: int = 3,
    max_completion_tokens: int = 4096
) → dict
```

Send a prompt and parse the response as JSON with validation and retry. 

Note: Retries use the same request to preserve HTTP snapshot compatibility. The request is not modified between retries. 



**Args:**
 
 - <b>`request`</b>:  The prompt text (should instruct LLM to respond with JSON) 
 - <b>`required_fields`</b>:  List of field names that must be present in response 
 - <b>`validator`</b>:  Optional function to validate parsed JSON, returns True if valid 
 - <b>`max_retries`</b>:  Number of retry attempts on parse/validation failure 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for the LLM's response 



**Returns:**
 Parsed JSON as a dictionary 



**Raises:**
 
 - <b>`ValueError`</b>:  If JSON parsing or validation fails after all retries 


---

## <kbd>class</kbd> `GptLlm`
GPT/Azure OpenAI implementation of the LLM interface. 

Requires environment variables: 
- OPENAI_API_KEY: API key for OpenAI/Azure 
- OPENAI_API_BASE: API endpoint (for Azure) 
- OPENAI_MODEL: Model name 
- OPENAI_DEPLOYMENT: Deployment name (for Azure) 
- OPENAI_API_VERSION: API version (for Azure) 
- OPENAI_COMPLETION_MAX_TOKENS: Max tokens (default: 2048) 

### <kbd>method</kbd> `__init__`

```python
__init__(client=None)
```

Initialize GPT LLM. 



**Args:**
 
 - <b>`client`</b>:  Optional OpenAI client. If None, creates AzureOpenAI client  from environment variables. 




---

### <kbd>method</kbd> `prompt`

```python
prompt(request: str, max_completion_tokens: int = 2048) → str
```

Send a prompt to GPT and get a response. 



**Args:**
 
 - <b>`request`</b>:  The prompt text to send to GPT 



**Returns:**
 GPT's response as a string 

---

### <kbd>method</kbd> `prompt_json`

```python
prompt_json(
    request: str,
    required_fields: List[str] = None,
    validator: Callable[[dict], bool] = None,
    max_retries: int = 3,
    max_completion_tokens: int = 4096
) → dict
```

Send a prompt and parse the response as JSON with validation and retry. 

Note: Retries use the same request to preserve HTTP snapshot compatibility. The request is not modified between retries. 



**Args:**
 
 - <b>`request`</b>:  The prompt text (should instruct LLM to respond with JSON) 
 - <b>`required_fields`</b>:  List of field names that must be present in response 
 - <b>`validator`</b>:  Optional function to validate parsed JSON, returns True if valid 
 - <b>`max_retries`</b>:  Number of retry attempts on parse/validation failure 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for the LLM's response 



**Returns:**
 Parsed JSON as a dictionary 



**Raises:**
 
 - <b>`ValueError`</b>:  If JSON parsing or validation fails after all retries 


---

## <kbd>class</kbd> `ClaudeLlm`
Anthropic Claude implementation of the LLM interface. 

Requires: 
- anthropic package: pip install anthropic 
- ANTHROPIC_API_KEY environment variable 

Optional environment variables: 
- ANTHROPIC_MODEL: Model name (default: claude-sonnet-4-20250514) 

### <kbd>method</kbd> `__init__`

```python
__init__(client=None)
```

Initialize Claude LLM. 



**Args:**
 
 - <b>`client`</b>:  Optional Anthropic client. If None, creates client  from ANTHROPIC_API_KEY environment variable. 




---

### <kbd>method</kbd> `prompt`

```python
prompt(request: str, max_completion_tokens: int = 2048) → str
```

Send a prompt to Claude and get a response. 



**Args:**
 
 - <b>`request`</b>:  The prompt text to send to Claude 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for Claude's response 



**Returns:**
 Claude's response as a string 

---

### <kbd>method</kbd> `prompt_json`

```python
prompt_json(
    request: str,
    required_fields: List[str] = None,
    validator: Callable[[dict], bool] = None,
    max_retries: int = 3,
    max_completion_tokens: int = 4096
) → dict
```

Send a prompt and parse the response as JSON with validation and retry. 

Note: Retries use the same request to preserve HTTP snapshot compatibility. The request is not modified between retries. 



**Args:**
 
 - <b>`request`</b>:  The prompt text (should instruct LLM to respond with JSON) 
 - <b>`required_fields`</b>:  List of field names that must be present in response 
 - <b>`validator`</b>:  Optional function to validate parsed JSON, returns True if valid 
 - <b>`max_retries`</b>:  Number of retry attempts on parse/validation failure 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for the LLM's response 



**Returns:**
 Parsed JSON as a dictionary 



**Raises:**
 
 - <b>`ValueError`</b>:  If JSON parsing or validation fails after all retries 


---

## <kbd>class</kbd> `OllamaLlm`
Ollama implementation of the LLM interface for local LLMs. 

Requires: 
- Ollama running locally (default: http://localhost:11434) 

Optional environment variables: 
- OLLAMA_HOST: Ollama server URL (default: http://localhost:11434) 
- OLLAMA_MODEL: Model name (default: llama3.2) 

### <kbd>method</kbd> `__init__`

```python
__init__(host: str = None, model: str = None)
```

Initialize Ollama LLM. 



**Args:**
 
 - <b>`host`</b>:  Ollama server URL. If None, uses OLLAMA_HOST env var 
 - <b>`or defaults to http`</b>: //localhost:11434. 
 - <b>`model`</b>:  Model name. If None, uses OLLAMA_MODEL env var  or defaults to llama3.2. 




---

### <kbd>method</kbd> `prompt`

```python
prompt(request: str, max_completion_tokens: int = 2048) → str
```

Send a prompt to Ollama and get a response. 



**Args:**
 
 - <b>`request`</b>:  The prompt text to send to Ollama 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for Ollama's response 



**Returns:**
 Ollama's response as a string 

---

### <kbd>method</kbd> `prompt_json`

```python
prompt_json(
    request: str,
    required_fields: List[str] = None,
    validator: Callable[[dict], bool] = None,
    max_retries: int = 3,
    max_completion_tokens: int = 4096
) → dict
```

Send a prompt and parse the response as JSON with validation and retry. 

Note: Retries use the same request to preserve HTTP snapshot compatibility. The request is not modified between retries. 



**Args:**
 
 - <b>`request`</b>:  The prompt text (should instruct LLM to respond with JSON) 
 - <b>`required_fields`</b>:  List of field names that must be present in response 
 - <b>`validator`</b>:  Optional function to validate parsed JSON, returns True if valid 
 - <b>`max_retries`</b>:  Number of retry attempts on parse/validation failure 
 - <b>`max_completion_tokens`</b>:  Maximum tokens for the LLM's response 



**Returns:**
 Parsed JSON as a dictionary 



**Raises:**
 
 - <b>`ValueError`</b>:  If JSON parsing or validation fails after all retries 


---

## <kbd>class</kbd> `LlmSentry`
Context manager for temporarily switching the default LLM. 



**Example:**
  with LlmSentry(my_custom_llm):  # Code here uses my_custom_llm as default  r = t.start_review()  r.reviewln("Is output correct?", "Yes", "No")  # Original LLM is restored 

### <kbd>method</kbd> `__init__`

```python
__init__(llm: Llm)
```

Initialize the sentry with a temporary LLM. 



**Args:**
 
 - <b>`llm`</b>:  The LLM to use temporarily 







---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
