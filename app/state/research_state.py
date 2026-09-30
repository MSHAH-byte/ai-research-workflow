from typing import TypedDict


class ResearchState(TypedDict):
    """
    Shared state passed between all nodes in the LangGraph workflow.

    Each node reads the information it needs from this state and returns
    updates that are merged back into the workflow state.
    """

    topic: str
    plan: str
    research: str
    feedback: str
    quality_score: int
    iteration: int
    max_iterations: int
    final_answer: str