from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.state.research_state import ResearchState


def finalizer(state: ResearchState) -> dict:
    """
    Convert the evaluated research into the final user-facing answer.

    This node runs after the evaluator determines that the research is
    acceptable or the maximum number of iterations has been reached.
    """

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2,
    )

    prompt = f"""
Create the final answer for the user based on the research below.

Topic:
{state["topic"]}

Research:
{state["research"]}

Quality score:
{state["quality_score"]}/10

Write a clear, accurate, well-structured answer.

Do not mention the internal workflow, planner, evaluator, iterations,
quality score, or feedback. Respond directly to the user's topic.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "final_answer": response.content,
    }