from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.state.research_state import ResearchState


def planner(state: ResearchState) -> dict:
    """
    Create a research plan for the user's topic.

    The planner is the first LLM-powered node in the workflow.
    It reads the topic from the shared state and stores the resulting
    research plan back into the state.
    """

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
    )

    prompt = f"""
You are a research planner.

Create a clear and focused research plan for the following topic:

{state["topic"]}

The plan should identify the key areas that need to be covered
to produce an accurate and useful explanation.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        "plan": response.content,
        "iteration": 0,
    }