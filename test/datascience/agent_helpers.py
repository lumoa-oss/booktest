"""
Shared utilities for LLM agent testing.

This module provides common functionality for testing LLM agents with booktest,
including context loading and snapshot configuration.
"""
import booktest as bt
import os


def load_booktest_context():
    """Load booktest documentation as context for LLM agents."""
    docs_dir = os.path.join(os.path.dirname(__file__), '..', '..')

    context = []

    # Load readme
    readme_path = os.path.join(docs_dir, 'readme.md')
    with open(readme_path, 'r') as f:
        context.append(f"# README\n\n{f.read()}")

    # Load getting started guide
    getting_started_path = os.path.join(docs_dir, 'getting-started.md')
    with open(getting_started_path, 'r') as f:
        context.append(f"# GETTING STARTED GUIDE\n\n{f.read()}")

    return "\n\n---\n\n".join(context)


def snapshot_gpt():
    """
    Snapshot decorator for GPT/OpenAI API calls.

    This decorator combines:
    - httpx snapshotting for API request/response capture
    - Environment variable mocking for API keys
    - Environment variable snapshotting for API configuration

    Use this for any test that calls OpenAI/Azure OpenAI APIs.
    """
    return bt.combine_decorators(
        bt.snapshot_httpx(lose_request_details=False),
        bt.mock_missing_env({"OPENAI_API_KEY": "mock-key"}),
        bt.snapshot_env(
            "BOOKTEST_LLM",
            "OPENAI_API_BASE",
            "OPENAI_MODEL",
            "OPENAI_DEPLOYMENT",
            "OPENAI_API_VERSION",
            "OPENAI_COMPLETION_MAX_TOKENS"
        )
    )


def create_assistant_prompt(context: str, question: str) -> str:
    """Create a prompt for an LLM assistant with context and question."""
    return f"""You are a helpful assistant answering questions about booktest, a Python testing framework.

Use the following documentation to answer the question accurately and concisely:

{context}

---

Question: {question}

Answer (be concise, 2-3 sentences max):"""
