from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.state.research_state import ResearchState


def researcher(state: ResearchState) -> dict:
    """
    Generate or improve the research based on the current plan and
    evaluator feedback.

    On the first pass there is no feedback, so the node generates the
    initial research. On later passes it uses the evaluator's feedback
    to improve the previous research.
    """

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
    )

    feedback = state["feedback"]

    if feedback:
        instruction = f"""
Improve the previous research using the evaluator's feedback.

Previous research:
{state["research"]}

Evaluator feedback:
{feedback}

Keep the useful information from the previous research, fix the
identified problems, and produce a more accurate and complete version.
"""
    else:
        instruction = f"""
Conduct research on the following topic using the provided research plan.

Topic:
{state["topic"]}

Research plan:
{state["plan"]}

Produce a clear, accurate, and well-structured research response.
Cover the important points from the plan without adding unnecessary
information.
"""

    response = llm.invoke([HumanMessage(content=instruction)])

    return {
        "research": response.content,
        "iteration": state["iteration"] + 1,
    }