"""
Test LLM assistant's ability to answer questions about booktest.

This test evaluates an LLM's capability to provide accurate responses
about booktest by testing it with 5 key questions that a Hacker News
audience might ask.
"""
import booktest as bt
import os


def load_context():
    """Load booktest documentation as context for the LLM."""
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


def create_assistant_prompt(context: str, question: str) -> str:
    """Create a prompt for the LLM with context and question."""
    return f"""You are a helpful assistant answering questions about booktest, a Python testing framework.

Use the following documentation to answer the question accurately and concisely:

{context}

---

Question: {question}

Answer (be concise, 2-3 sentences max):"""


# Define test prompts with LLM-based evaluation criteria
PROMPTS = [
    {
        "question": "What is booktest?",
        "criteria": [
            "Does answer mention snapshot or review-driven testing?",
            "Does answer mention data science focus?",
            "Does answer mention Git-tracked results?"
        ]
    },
    {
        "question": "When should I use booktest instead of pytest?",
        "criteria": [
            "Does answer mention expert review needs?",
            "Does answer mention non-deterministic or probabilistic results?",
            "Does answer mention data science workflows or caching?"
        ]
    },
    {
        "question": "Write a simple booktest example for fizzbuzz",
        "criteria": [
            "Does code include 'import booktest' or 'import booktest as bt'?",
            "Does code define a test function starting with 'test_'?",
            "Does code use TestCaseRun parameter (like 't: bt.TestCaseRun')?",
            "Does code use output methods like t.h1() or t.tln()?",
            "Is the code syntactically valid Python?"
        ]
    },
    {
        "question": "How does booktest handle non-deterministic results?",
        "criteria": [
            "Does answer mention snapshots or snapshot testing?",
            "Does answer mention caching intermediate results?",
            "Does answer mention mocking functions or environment variables?"
        ]
    },
    {
        "question": "How do I integrate booktest into my existing Python project?",
        "criteria": [
            "Does answer mention 'pip install booktest' or installation?",
            "Does answer mention creating a test directory?",
            "Does answer mention running 'booktest' command or CLI?"
        ]
    }
]


def snapshot_gpt():
    """Snapshot decorator for GPT/OpenAI API calls."""
    return bt.combine_decorators(
        bt.snapshot_httpx(lose_request_details=False),
        bt.mock_missing_env({"OPENAI_API_KEY": "mock-key"}),
        bt.snapshot_env(
            "OPENAI_API_BASE",
            "OPENAI_MODEL",
            "OPENAI_DEPLOYMENT",
            "OPENAI_API_VERSION",
            "OPENAI_COMPLETION_MAX_TOKENS"
        )
    )


@snapshot_gpt()
def test_assistant(t: bt.TestCaseRun):
    """Test LLM assistant with booktest documentation context."""

    t.h1("Test: LLM Assistant for Booktest Questions")
    t.iln("This test evaluates an LLM's ability to answer questions about booktest")
    t.iln("using documentation as context.")
    t.iln()

    # Load context
    t.h2("Loading Context")
    context = t.cache(load_context)
    context_lines = len(context.split('\n'))
    t.iln(f"Loaded {context_lines} lines of documentation")
    t.iln()

    # Scoring scheme
    scoring = {
        "Yes": 1,
        "Partially": 0.5,
        "No": 0
    }

    # Test each prompt
    t.h2("Testing Prompts")
    total_score = 0
    max_score = 0

    for i, prompt_data in enumerate(PROMPTS, 1):
        question = prompt_data["question"]
        criteria = prompt_data["criteria"]

        t.h3(f"Prompt {i}: {question}")

        # Get LLM answer
        full_prompt = create_assistant_prompt(context, question)

        r = t.start_review()
        r.iln(f"**Question:** {question}")
        r.iln()

        # Use LLM to answer
        answer = r.llm.prompt(full_prompt)

        r.iln(f"**Answer:**")
        r.iln(answer)
        r.iln()

        # Evaluate using LLM review
        r.h1("Evaluation:")
        prompt_score = 0
        prompt_max = len(criteria)

        for criterion in criteria:
            result = r.ireviewln(criterion, "Yes", "Partially", "No")
            prompt_score += scoring.get(result, 0)

        total_score += prompt_score
        max_score += prompt_max

        t.iln()
        t.iln(f"**Score:** {prompt_score}/{prompt_max}")
        t.iln()

    # Final evaluation
    t.h2("Final Evaluation")

    success_rate = (total_score / max_score) * 100 if max_score > 0 else 0

    t.iln(f"Total Score: {total_score}/{max_score} ({success_rate:.1f}%)")
    t.iln()

    # Require 80% success rate
    required_score = max_score * 0.8
    t.t(f"Require {required_score:.1f}+ score for 80% success rate.. ").assertln(
        total_score >= required_score,
        f"Only {total_score}/{max_score} ({success_rate:.1f}%) - need {required_score:.1f}+"
    )
