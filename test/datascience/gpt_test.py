import booktest as bt
import requests
import json

import os

from openai import AzureOpenAI


def snapshot_gpt():
    """Snapshot decorator for GPT/OpenAI API calls."""
    return bt.combine_decorators(
        bt.snapshot_httpx(
            lose_request_details=False),
        bt.mock_missing_env({
            "OPENAI_API_KEY": "mock-key"
        }),
        bt.snapshot_env(
            "OPENAI_API_BASE",
            "OPENAI_MODEL",
            "OPENAI_DEPLOYMENT",
            "OPENAI_API_VERSION",
            "OPENAI_COMPLETION_MAX_TOKENS"
        )
    )


@snapshot_gpt()
def test_request(t: bt.TestCaseRun):
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        azure_endpoint=os.getenv("OPENAI_API_BASE"),
        azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        max_retries=5)

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing very concise answers."},
            {"role": "user", "content": "What is the capital of Finland? "}
        ],
        model=os.getenv("OPENAI_MODEL"),
        max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", 1024)),
        seed=0)

    result = response.choices[0].message.content

    t.h1("response:")
    t.iln(result)

    t.h1("assertions:")
    t.key(" * contains Helsinki..").assertln("helsinki" in result.lower())


class Review:
    
    def __init__(self, t: bt.TestCaseRun):
        self.t = t
        self.buffer = ""
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
            azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            max_retries=5)

    def i(self, text):
        self.buffer += text
        self.t.i(text)
        
    def h(self, level, title):
        label = "#" * level + " " + title
        self.buffer += f"\n{label}\n"
        self.t.h(level, title)

    def h1(self, title):
        self.h(1, title)
        
    def iln(self, text):
        self.i(text + "\n")

    def icodeln(self, code):
        self.i(f"```\n{code}\n```\n")

    def start_review(self):
        self.t.h1("review:")
        
    def reviewln(self, prompt, expected, *fail):

        system_prompt = \
"""You are an expert reviewer for test results. You are given question in format:

Question? (optionA|optionB|optionC|...)
  
reviewed material

Respond only with the exact option that best answers the question! Do produce any 
other text or explanation! Only respond with one of the options given in the parentheses."""

        options = [expected] + list(fail)

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{prompt} ({'|'.join(options)})\n\n{self.buffer}"}
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", 1024)),
            seed=0)
        
        result = response.choices[0].message.content
        
        self.t.anchor(f" * {prompt} ").i(result).i(" - ").assertln(result == expected)

    def assertln(self, title, condition):
        self.t.anchor(f" * {title}..").assertln(condition)


@snapshot_gpt()
def test_review(t: bt.TestCaseRun):
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        azure_endpoint=os.getenv("OPENAI_API_BASE"),
        azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        max_retries=5)
    
    prompt = """
Write me a hello world code example in python!

This example is made for a school age child, and it should contain
comments in Finnish explain every step on the way. 

The response will be run with python to see the result, so it should be syntactically
valid python. 
"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        model=os.getenv("OPENAI_MODEL"),
        max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", 1024)),
        seed=0)

    code = response.choices[0].message.content
    
    r = Review(t)
    
    r.h1("prompt:")
    r.iln(prompt)

    r.h1("result:")
    r.icodeln(code)

    r.start_review()
    r.reviewln("Does results follow instructions?", "Yes", "No")
    r.reviewln("Are comments in Finnish?", "Yes", "No")
    r.reviewln("Is code in python?", "Yes", "No")
    r.reviewln("How would you grade this response?", "***", "**", "*")

    # run code in python
    local_vars = {}
    exception = None
    try:
        exec(code, {}, local_vars)
    except Exception as e:
        exception = e
    r.assertln("Does code runs without errors", exception is None)

    if exception:
        t.h1("exception:")
        t.iln(str(exception))
