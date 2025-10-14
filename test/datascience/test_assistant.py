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


# Define test prompts and success criteria
PROMPTS = [
    {
        "question": "What is booktest?",
        "keywords": ["snapshot", "review", "data science", "git", "test"],
        "description": "Should mention snapshot/review-driven testing and data science focus"
    },
    {
        "question": "When should I use booktest instead of pytest?",
        "keywords": ["expert review", "non-deterministic", "data science", "cache", "snapshot"],
        "description": "Should mention expert review needs and data science workflows"
    },
    {
        "question": "Write a simple booktest example for fizzbuzz",
        "keywords": ["def test_", "bt.TestCaseRun", "t.h1", "t.tln", "import booktest"],
        "description": "Should provide working code with correct syntax"
    },
    {
        "question": "How does booktest handle non-deterministic results?",
        "keywords": ["snapshot", "cache", "mock", "review", "expert"],
        "description": "Should mention snapshots, caching, or function mocking"
    },
    {
        "question": "How do I integrate booktest into my existing Python project?",
        "keywords": ["pip install", "test/", "booktest -v -i", ".booktest", "books/"],
        "description": "Should mention installation and basic setup steps"
    }
]


def evaluate_answer(answer: str, criteria: dict) -> tuple[bool, str]:
    """
    Evaluate if an answer meets the success criteria.

    Returns:
        (passes, reason) tuple
    """
    answer_lower = answer.lower()

    # Count how many keywords are present
    keywords_found = []
    keywords_missing = []

    for keyword in criteria["keywords"]:
        if keyword.lower() in answer_lower:
            keywords_found.append(keyword)
        else:
            keywords_missing.append(keyword)

    # Pass if at least 40% of keywords are present
    threshold = len(criteria["keywords"]) * 0.4
    passes = len(keywords_found) >= threshold

    reason = f"{len(keywords_found)}/{len(criteria['keywords'])} keywords found"
    if not passes:
        reason += f" (need {int(threshold)}+)"

    return passes, reason


@bt.snapshot_httpx(lose_request_details=False)
@bt.mock_missing_env({"OPENAI_API_KEY": "mock-key"})
@bt.snapshot_env(
    "OPENAI_API_BASE",
    "OPENAI_MODEL",
    "OPENAI_DEPLOYMENT",
    "OPENAI_API_VERSION",
    "OPENAI_COMPLETION_MAX_TOKENS"
)
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

    # Test each prompt
    t.h2("Testing Prompts")
    results = []

    for i, prompt_data in enumerate(PROMPTS, 1):
        question = prompt_data["question"]

        t.h3(f"Prompt {i}: {question}")
        t.iln(f"Expected: {prompt_data['description']}")
        t.iln()

        # Get LLM answer
        full_prompt = create_assistant_prompt(context, question)

        r = t.start_review()
        r.iln(f"**Question:** {question}")
        r.iln()

        # Use LLM to answer
        answer = r.llm.prompt(full_prompt)

        r.iln(f"**Answer:** {answer}")
        r.iln()

        # Evaluate answer
        passes, reason = evaluate_answer(answer, prompt_data)
        results.append((question, passes, reason, answer))

        status = "✓ PASS" if passes else "✗ FAIL"
        t.iln(f"**Evaluation:** {status} - {reason}")
        t.iln()

    # Final evaluation
    t.h2("Final Evaluation")

    passed_count = sum(1 for _, passes, _, _ in results if passes)
    total_count = len(results)
    success_rate = (passed_count / total_count) * 100

    t.ttable({
        "Prompt": [f"Prompt {i+1}" for i in range(total_count)],
        "Status": ["✓ PASS" if p else "✗ FAIL" for _, p, _, _ in results],
        "Reason": [r for _, _, r, _ in results]
    })

    t.iln()
    t.iln(f"Success Rate: {passed_count}/{total_count} ({success_rate:.0f}%)")
    t.iln()

    # Require 80% success rate
    required_passes = int(total_count * 0.8)
    t.t(f"Require {required_passes}+ passes for 80% success rate.. ").assertln(
        passed_count >= required_passes,
        f"Only {passed_count}/{total_count} passed (need {required_passes}+)"
    )
