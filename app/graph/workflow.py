from langgraph.graph import END, START, StateGraph

from app.nodes.evaluator import evaluator
from app.nodes.finalizer import finalizer
from app.nodes.planner import planner
from app.nodes.researcher import researcher
from app.state.research_state import ResearchState


# Research must reach this score before the workflow can finish early.
QUALITY_THRESHOLD = 7

# Prevents the feedback loop from running indefinitely.
MAX_ITERATIONS = 3


def route_after_evaluation(state: ResearchState) -> str:
    """
    Decide whether the research is good enough to finalize or needs
    another improvement cycle.
    """

    if state["quality_score"] >= QUALITY_THRESHOLD:
        return "finalizer"

    if state["iteration"] >= MAX_ITERATIONS:
        return "finalizer"

    return "researcher"


def build_workflow():
    """
    Build and compile the LangGraph research workflow.
    """

    graph = StateGraph(ResearchState)

    # Register the workflow nodes.
    graph.add_node("planner", planner)
    graph.add_node("researcher", researcher)
    graph.add_node("evaluator", evaluator)
    graph.add_node("finalizer", finalizer)

    # Define the normal execution path.
    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "evaluator")

    # The evaluator decides whether to finish or improve the research.
    graph.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "researcher": "researcher",
            "finalizer": "finalizer",
        },
    )

    graph.add_edge("finalizer", END)

    return graph.compile()