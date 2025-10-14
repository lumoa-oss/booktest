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
        ],
        "ratings": [
            "How clear and concise is the explanation?",
            "How compelling is the value proposition for using booktest?"
        ]
    },
    {
        "question": "When should I use booktest instead of pytest?",
        "criteria": [
            "Does answer mention expert review needs?",
            "Does answer mention non-deterministic or probabilistic results?",
            "Does answer mention data science workflows or caching?"
        ],
        "ratings": [
            "How clearly are the use cases differentiated?",
            "How helpful would this be for someone choosing a testing framework?"
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
        ],
        "ratings": [
            "How clear and understandable is the code example?",
            "How well does the example demonstrate booktest features?"
        ]
    },
    {
        "question": "How does booktest handle non-deterministic results?",
        "criteria": [
            "Does answer mention snapshots or snapshot testing?",
            "Does answer mention caching intermediate results?",
            "Does answer mention mocking functions or environment variables?"
        ],
        "ratings": [
            "How well does the answer explain the technical approach?",
            "How practical and actionable is the explanation?"
        ]
    },
    {
        "question": "How do I integrate booktest into my existing Python project?",
        "criteria": [
            "Does answer mention 'pip install booktest' or installation?",
            "Does answer mention creating a test directory?",
            "Does answer mention running 'booktest' command or CLI?"
        ],
        "ratings": [
            "How complete is the integration guide?",
            "How easy would it be to follow these instructions?"
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
    context = load_context()
    context_lines = len(context.split('\n'))
    t.iln(f"Loaded {context_lines} lines of documentation")
    t.iln()

    # Scoring schemes
    binary_scoring = {
        "Yes": 1,
        "Partially": 0.5,
        "No": 0
    }

    rating_scoring = {
        "Excellent": 1,
        "Good": 0.75,
        "Poor": 0
    }

    # Test each prompt
    t.h2("Testing Prompts")
    total_criteria_score = 0
    max_criteria_score = 0
    total_rating_score = 0
    max_rating_score = 0

    for i, prompt_data in enumerate(PROMPTS, 1):
        question = prompt_data["question"]
        criteria = prompt_data["criteria"]
        ratings = prompt_data.get("ratings", [])

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
        r.h4("Evaluation:")

        # Binary criteria evaluation
        criteria_score = 0
        for criterion in criteria:
            result = r.ireviewln(criterion, "Yes", "Partially", "No")
            criteria_score += binary_scoring.get(result, 0)

        total_criteria_score += criteria_score
        max_criteria_score += len(criteria)

        # Rating evaluation
        rating_score = 0
        if ratings:
            r.h4("Quality ratings:")
            for rating_question in ratings:
                result = r.ireviewln(rating_question, "Excellent", "Good", "Poor")
                rating_score += rating_scoring.get(result, 0)

        total_rating_score += rating_score
        max_rating_score += len(ratings)

        t.iln()
        t.iln(f" * **Criteria Score:** {criteria_score}/{len(criteria)}")
        if ratings:
            t.iln(f" * **Rating Score:** {rating_score}/{len(ratings)}")
        t.iln()

    # Final evaluation
    t.h2("Final Evaluation")

    criteria_rate = (total_criteria_score / max_criteria_score) * 100 if max_criteria_score > 0 else 0
    rating_rate = (total_rating_score / max_rating_score) * 100 if max_rating_score > 0 else 0

    t.iln(f" * Criteria Score: {total_criteria_score}/{max_criteria_score} ({criteria_rate:.1f}%)")
    t.iln(f" * Rating Score: {total_rating_score}/{max_rating_score} ({rating_rate:.1f}%)")
    t.iln()

    # Require 80% criteria success and 70% rating success
    required_criteria_score = max_criteria_score * 0.8
    required_rating_score = max_rating_score * 0.7

    t.t(f" * Require {required_criteria_score:.1f}+ criteria score (80%).. ").assertln(
        total_criteria_score >= required_criteria_score,
        f"Only {total_criteria_score}/{max_criteria_score} ({criteria_rate:.1f}%)"
    )

    t.t(f" * Require {required_rating_score:.1f}+ rating score (70%).. ").assertln(
        total_rating_score >= required_rating_score,
        f"Only {total_rating_score}/{max_rating_score} ({rating_rate:.1f}%)"
    )
