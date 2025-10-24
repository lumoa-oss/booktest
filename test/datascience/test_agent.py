"""
Test a 3-step agent using booktest's build system.

This demonstrates how booktest's dependency system allows you to:
1. Break a multi-step agent interaction into separate tests
2. Iterate on individual steps without re-running previous steps
3. Use snapshots to make re-runs instant after first execution

Pattern: Build system + Snapshotting = Fast iterative agent development
"""
import booktest as bt
from test.datascience.agent_helpers import snapshot_gpt, load_booktest_context
from test.datascience.booktest_agent import BooktestAgent, AgentState, create_initial_state


# Step 1: Agent creates a plan
@snapshot_gpt()
def test_agent_step1_plan(t: bt.TestCaseRun) -> AgentState:
    """
    Step 1: Agent analyzes question and creates a plan.

    This test is slow on first run (loads context, calls GPT),
    but instant on subsequent runs due to snapshotting.
    """
    t.h1("Agent Step 1: Planning")
    t.iln("Agent analyzes the question and creates an answering strategy")
    t.iln()

    # Initialize state
    question = "How do I test a multi-step ML pipeline with booktest?"
    state = create_initial_state(question)

    # Load context (expensive on first run)
    t.h2("Loading Context")
    context = load_booktest_context()
    state["context"] = context
    t.iln(f"Loaded {len(context)} characters of documentation")
    t.iln()

    # Create agent and plan
    t.h2("Creating Plan")
    agent = BooktestAgent(context)
    state, message = agent.plan(state)
    t.iln(f"✓ {message}")
    t.iln()

    # Review the plan with LLM
    r = t.start_review()
    r.h3("Question")
    r.iln(question)
    r.iln()

    r.h3("Plan")
    r.iln(state["plan"])
    r.iln()

    r.h3("Plan Review")
    r.treviewln("Does plan address the question?", "Yes", "Partially", "No")
    r.treviewln("Does plan reference relevant features?", "Yes", "Partially", "No")

    # Return state for next step
    return state


# Step 2: Agent generates answer
@bt.depends_on(test_agent_step1_plan)
@snapshot_gpt()
def test_agent_step2_answer(t: bt.TestCaseRun, state: AgentState) -> AgentState:
    """
    Step 2: Agent generates answer following the plan.

    Depends on step 1. If you're iterating on the answer generation,
    step 1 doesn't re-run (instant due to caching + snapshots).
    """
    t.h1("Agent Step 2: Generating Answer")
    t.iln("Agent uses the plan to generate a detailed answer")
    t.iln()

    # Show inherited state
    t.h2("Inherited State from Step 1")
    t.iln(f"Question: {state['question']}")
    t.iln(f"Plan: {state['plan'][:150]}...")
    t.iln()

    # Generate answer
    t.h2("Generating Answer")
    agent = BooktestAgent(state["context"])
    state, message = agent.answer(state)
    t.iln(f"✓ {message}")
    t.iln()

    # Review the answer with LLM
    r = t.start_review()
    r.h3("Generated Answer")
    r.iln(state["answer"])
    r.iln()

    r.h3("Answer Review")
    r.treviewln("Does answer follow the plan?", "Yes", "No")
    r.treviewln("Is answer accurate per documentation?", "Yes", "No")
    r.treviewln("Is answer clear and concise?", "Yes", "No")

    # Return updated state
    return state


# Step 3: Agent validates the answer
@bt.depends_on(test_agent_step2_answer)
@snapshot_gpt()
def test_agent_step3_validate(t: bt.TestCaseRun, state: AgentState):
    """
    Step 3: Agent validates the answer for quality and completeness.

    Depends on step 2. When iterating on validation logic,
    steps 1-2 don't re-run (instant due to caching + snapshots).
    """
    t.h1("Agent Step 3: Validation")
    t.iln("Agent validates the answer for quality and completeness")
    t.iln()

    # Show inherited state
    t.h2("Inherited State from Steps 1-2")
    t.iln(f"Question: {state['question']}")
    t.iln(f"Answer: {state['answer'][:150]}...")
    t.iln()

    # Validate answer
    t.h2("Validation")
    agent = BooktestAgent(state["context"])
    state, message = agent.validate(state)
    t.iln(f"✓ {message}")
    t.iln()

    # Review validation with LLM
    r = t.start_review()
    r.h3("Validation Result")
    r.iln(state["validation"])
    r.iln()

    r.h3("Quality Assessment")
    overall = r.ireviewln("Overall answer quality?", "Excellent", "Good", "Poor")
    complete = r.ireviewln("Completeness?", "Complete", "Mostly Complete", "Incomplete")
    r.iln()

    # Metrics with tolerance
    t.h3("Metrics")
    quality_score = {"Excellent": 100, "Good": 75, "Poor": 50}.get(overall, 0)
    complete_score = {"Complete": 100, "Mostly Complete": 75, "Incomplete": 50}.get(complete, 0)

    t.key(" * Quality Score:").tmetricln(quality_score, tolerance=15, unit="%")
    t.key(" * Completeness Score:").tmetricln(complete_score, tolerance=15, unit="%")
    t.iln()

    # Minimum requirements (relaxed for agent testing)
    t.h3("Minimum Requirements")
    t.key(" * Quality ≥ 50%..").assertln(quality_score >= 50, f"Got {quality_score}%")
    t.key(" * Completeness ≥ 50%..").assertln(complete_score >= 50, f"Got {complete_score}%")

    return state
