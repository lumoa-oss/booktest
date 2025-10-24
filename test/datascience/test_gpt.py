"""
Tests demonstrating LLM-assisted review functionality with GPT.

To use a custom LLM for specific tests, use the @use_llm decorator:

    @bt.use_llm(my_custom_llm)
    @snapshot_gpt()
    def test_with_custom_llm(t: bt.TestCaseRun):
        r = t.start_review()
        r.reviewln("Is output correct?", "Yes", "No")

Or set globally:
    bt.set_llm(my_custom_llm)

Or use context manager for scoped changes:
    with bt.LlmSentry(my_custom_llm):
        # tests here use custom LLM
"""
import booktest as bt
import os

from openai import AzureOpenAI
from test.datascience.agent_helpers import snapshot_gpt


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


class CatDetector:

    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
            azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            max_retries=5)

    def contains_a_cat(self, text: str) -> bool:
        prompt = f"Does the following text mention or imply a non-robot cat? Answer yes, no or robot\n\n{text}"

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a pedantic assistant providing very precise and concise answers."},
                {"role": "user", "content": prompt}
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", 1024)),
            seed=0)

        result = response.choices[0].message.content.lower()
        return "yes" in result


@snapshot_gpt()
def test_evaluation(t: bt.TestCaseRun):
    detector = CatDetector()

    data = [
        ("I have a cat named Whiskers.", True),
        ("The dog barked loudly.", False),
        ("My pet is very playful.", False),  # ambiguous, but no direct mention of
        ("Cats are great companions.", True),
        ("I love my feline friend.", True),
        ("It walks like a cat, meows like a cat and looks like a cat", True),
        ("It walks like a cat, meows like a cat and looks like a cat, but it's actually a robot", False)
    ]

    t.h1("cat detection results:")

    cats = 0
    accurate = 0
    n = 0
    errors = []

    for text, ground in data:
        result = detector.contains_a_cat(text)
        if result == ground:
            t.iln(f" * {text} -> {result}")
            accurate += 1
        else:
            t.iln(f" * {text} -> {result} (expected {ground})")
            errors.append((text, result, ground))
        if ground:
            cats += 1
        n += 1

    t.h1("errors:")
    for text, result, ground in errors:
        t.iln(f" * {text} -> {result} (expected {ground})")

    precision = accurate/(accurate + len(errors))
    recall = cats / accurate if accurate > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy_pct = 100 * accurate / len(data)

    t.h1("evaluation:")
    t.iln("Tracking metrics with ±5% tolerance")
    t.iln()

    # Track metrics with tolerance - allows minor fluctuations but catches regressions
    t.key(" * accuracy:").i(f"{accurate}/{len(data)} = ").tmetricln(accuracy_pct, tolerance=5, unit="%")
    t.key(" * precision:").tmetricln(100*precision, tolerance=5, unit="%")
    t.key(" * recall:").tmetricln(100*recall, tolerance=5, unit="%")
    t.key(" * F1 score:").tmetricln(f1, tolerance=0.05)
    t.iln()

    t.h1("minimum requirements:")
    t.iln("Hard requirements that must always pass")
    t.iln()

    # Minimum requirements - these are hard failures if not met
    t.key(" * accuracy ≥ 80%..").assertln(accuracy_pct >= 80.0, f"only {accuracy_pct:.1f}%")
    t.key(" * precision ≥ 80%..").assertln(precision >= 0.80, f"only {100*precision:.1f}%")
    t.key(" * errors ≤ 1..").assertln(len(errors) <= 1, f"{len(errors)} errors")


# Review class moved to booktest.gpt_review.GptReview
# Use t.start_review() to create a review instance


class Assistant:

    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
            azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            max_retries=5)

    def prompt(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model=os.getenv("OPENAI_MODEL"),
            max_completion_tokens=int(os.getenv("OPENAI_COMPLETION_MAX_TOKENS", 1024)),
            seed=0)

        return response.choices[0].message.content

hello_world_prompt = """
Write me a hello world code example in python! The code must print "Hello World!" to the console.

This example is made for a school age child, and it should contain
comments in Finnish explain every step on the way. 

The response will be run with python to see the result, 
so it should be syntactically valid python.   
"""


def run_python(code: str):
    # run code in python and capture output
    import sys
    from io import StringIO

    local_vars = {}
    exception = None
    output = ""

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code, {}, local_vars)
        output = sys.stdout.getvalue()
    except Exception as e:
        exception = e
    finally:
        sys.stdout = old_stdout
    return output, exception


@snapshot_gpt()
def test_review(t: bt.TestCaseRun):
    prompt = hello_world_prompt

    code = Assistant().prompt(prompt)

    r = t.start_review()

    r.h1("request:")
    r.iln(prompt)

    r.h1("code:")
    r.icode(code, "python")

    output, exception = run_python(code)

    if exception:
        r.h1("exception:")
        r.fail().iln(str(exception))
    else:
        r.h1("output:")
        r.iln(output)

    r.start_review()
    r.reviewln("Does results follow instructions?", "Yes", "No")
    r.reviewln("Are comments in Finnish?", "Yes", "No")
    r.reviewln("Is code in python?", "Yes", "No")
    r.reviewln("How would you grade this response?", "Excellent", "Ok", "Bad")
    r.assertln("Does the code run without errors?", exception is None)
    r.assertln("Does the code print 'Hello World!'?", output.strip() == "Hello World!")
