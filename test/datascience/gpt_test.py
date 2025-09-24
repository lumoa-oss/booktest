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