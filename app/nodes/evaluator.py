from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from app.state.research_state import ResearchState


def evaluator(state: ResearchState) -> dict:
    """
    Evaluate the current research and provide actionable feedback.

    The evaluator returns a numerical quality score and feedback that
    the researcher can use during another iteration.
    """

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
    )

    prompt = f"""
You are a strict research evaluator.

Evaluate the following research about:

Topic:
{state["topic"]}

Research plan:
{state["plan"]}

Research:
{state["research"]}

Evaluate it based on:
1. Accuracy
2. Completeness
3. Relevance to the topic
4. Clarity
5. Structure

Give a score from 1 to 10.

Return your response using exactly this format:

SCORE: <number>
FEEDBACK: <specific feedback>

The feedback should explain what is good and what needs improvement.
If the research is already strong, say so clearly.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    content = response.content.strip()

    score = 1
    feedback = content

    # Extract the score from the structured evaluator response.
    for line in content.splitlines():
        if line.upper().startswith("SCORE:"):
            try:
                score = int(line.split(":", 1)[1].strip())
                score = max(1, min(score, 10))
            except ValueError:
                score = 1

        elif line.upper().startswith("FEEDBACK:"):
            feedback = line.split(":", 1)[1].strip()

    return {
        "quality_score": score,
        "feedback": feedback,
    }