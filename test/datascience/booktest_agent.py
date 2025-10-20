"""
Simple Q&A agent for booktest documentation.

This agent demonstrates a 3-step workflow:
1. Plan: Analyze question and create answering strategy
2. Answer: Generate answer following the plan
3. Validate: Review answer quality and completeness
"""
from typing import TypedDict
from openai import AzureOpenAI
import os

from booktest import get_llm


class AgentState(TypedDict):
    """State that flows through the agent."""
    question: str
    context: str
    plan: str
    answer: str
    validation: str
    step: int


class BooktestAgent:
    """
    A simple agent that answers questions about booktest.

    The agent operates in three steps:
    - plan(): Analyze question and create strategy
    - answer(): Generate answer following the plan
    - validate(): Review and critique the answer
    """

    def __init__(self, context: str):
        """
        Initialize agent with documentation context.

        Args:
            context: Booktest documentation to use for answering questions
        """
        self.llm = get_llm()
        self.context = context
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            azure_endpoint=os.getenv("OPENAI_API_BASE"),
            azure_deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt35turbo"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-08-01-preview")
        )

    def prompt(self, request: str) -> str:
        return self.llm.prompt(request, 2048)

    def plan(self, state: AgentState) -> tuple[AgentState, str]:
        """
        Step 1: Analyze question and create answering plan.

        Returns:
            Updated state with plan, and message describing the plan
        """
        question = state["question"]

        prompt = f"""You are analyzing a question about booktest (a Python testing framework).

Question: "{question}"

Documentation context:
{self.context[:2000]}... (context truncated for prompt)

Task: Create a brief plan (2-3 bullet points) for answering this question.
Focus on:
- Which booktest features are most relevant
- Key concepts that must be explained
- The order in which to present information

Keep your plan concise and actionable."""

        plan = self.prompt(prompt)
        state["plan"] = plan
        state["step"] = 1

        return state, f"Created plan with {len(plan.split())} words"

    def answer(self, state: AgentState) -> tuple[AgentState, str]:
        """
        Step 2: Generate answer following the plan.

        Returns:
            Updated state with answer, and message describing the answer
        """
        question = state["question"]
        plan = state["plan"]

        prompt = f"""You are answering a question about booktest (a Python testing framework).

Question: "{question}"

Your plan:
{plan}

Documentation context:
{self.context[:3000]}... (context truncated for prompt)

Task: Generate a clear, concise answer (4-5 sentences) that:
1. Directly answers the question
2. Follows the plan you created
3. References specific booktest features from the documentation
4. Provides actionable guidance

Be specific and practical."""

        answer = self.prompt(prompt)
        state["answer"] = answer
        state["step"] = 2

        return state, f"Generated answer with {len(answer.split())} words"

    def validate(self, state: AgentState) -> tuple[AgentState, str]:
        """
        Step 3: Validate answer quality and completeness.

        Returns:
            Updated state with validation, and message describing validation
        """
        question = state["question"]
        answer = state["answer"]

        prompt = f"""You are reviewing an answer about booktest (a Python testing framework).

Question: "{question}"

Answer provided:
"{answer}"

Task: Evaluate this answer objectively:
1. Does it accurately answer the question?
2. Does it reference appropriate booktest features?
3. Is it clear and actionable?
4. What could be improved?

Provide a validation (2-3 sentences) with:
- What works well
- Any issues or missing information
- Overall assessment (Excellent/Good/Poor)

Be honest and constructive."""

        validation = self.prompt(prompt)
        state["validation"] = validation
        state["step"] = 3

        return state, f"Completed validation with {len(validation.split())} words"


def create_initial_state(question: str) -> AgentState:
    """Create initial agent state for a question."""
    return {
        "question": question,
        "context": "",
        "plan": "",
        "answer": "",
        "validation": "",
        "step": 0
    }
