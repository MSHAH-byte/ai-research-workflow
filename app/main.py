from dotenv import load_dotenv

from app.graph.workflow import MAX_ITERATIONS, build_workflow


def run_research_workflow(workflow, topic: str) -> None:
    """
    Run the research workflow for a single user topic and display
    the resulting answer and evaluation information.
    """

    initial_state = {
        "topic": topic,
        "plan": "",
        "research": "",
        "feedback": "",
        "quality_score": 0,
        "iteration": 0,
        "max_iterations": MAX_ITERATIONS,
        "final_answer": "",
    }

    print("\nRunning research workflow...\n")

    result = workflow.invoke(initial_state)

    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)
    print(result["final_answer"])
    print("=" * 60)

    print(f"\nResearch iterations: {result['iteration']}")
    print(f"Final quality score: {result['quality_score']}/10")
    print()


def main() -> None:
    """Run the interactive AI research workflow."""

    load_dotenv()

    workflow = build_workflow()

    print("AI Research Workflow")
    print("Enter 'quit' or 'exit' to end the program.")

    while True:
        topic = input("\nEnter a research topic: ").strip()

        if topic.lower() in {"quit", "exit"}:
            print("\nGoodbye!")
            break

        if not topic:
            print("Research topic cannot be empty.")
            continue

        run_research_workflow(workflow, topic)


if __name__ == "__main__":
    main()