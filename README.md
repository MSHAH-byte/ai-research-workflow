# AI Research Workflow

A workflow-based AI research assistant built with **Python, LangGraph, LangChain, and Groq**.

The project demonstrates how an LLM application can be structured as a stateful workflow where multiple specialized nodes collaborate to plan, generate, evaluate, improve, and finalize a research response.

## Overview

Instead of sending a user query directly to an LLM, the application processes it through a structured LangGraph workflow:

```text
User Topic
    ↓
Planner
    ↓
Researcher
    ↓
Evaluator
    ↓
Quality Check
    ├── Good enough ──────→ Finalizer → END
    │
    └── Needs improvement
              ↓
          Researcher
              ↓
          Evaluator
              ↓
             ...
```

The workflow can repeat the research and evaluation cycle when the generated research does not meet the required quality threshold.

A maximum iteration limit prevents the workflow from running indefinitely.

## Features

* Interactive command-line interface
* LLM-powered research planning
* LLM-powered research generation
* Automated research evaluation
* Quality scoring from 1–10
* Feedback-driven research improvement
* Conditional workflow routing
* Cyclic LangGraph workflow
* Maximum iteration safeguard
* Final answer generation
* Environment-based API key configuration

## Tech Stack

* **Python 3.12**
* **LangGraph** — workflow orchestration and state management
* **LangChain** — LLM application framework
* **ChatGroq** — Groq LLM integration
* **python-dotenv** — environment variable management

## Architecture

### Shared State

The workflow uses a shared `ResearchState` object:

```text
topic
plan
research
feedback
quality_score
iteration
max_iterations
final_answer
```

Each node reads the information it needs from the state and returns updates that are passed to subsequent nodes.

### Workflow Nodes

#### Planner

Creates a focused research plan based on the user's topic.

```text
Topic → Research Plan
```

#### Researcher

Generates the initial research using the topic and plan.

During later iterations, it uses evaluator feedback to improve the previous research.

```text
Topic + Plan
     ↓
Research
```

or:

```text
Previous Research + Feedback
            ↓
     Improved Research
```

#### Evaluator

Reviews the research according to:

* Accuracy
* Completeness
* Relevance
* Clarity
* Structure

It produces a quality score from 1–10 and feedback for the researcher.

#### Finalizer

Converts the evaluated research into the final user-facing answer.

The final response does not expose the internal workflow details.

## Conditional Routing

After evaluation, the workflow checks the quality score.

The current configuration uses:

```text
Quality threshold: 7/10
Maximum research iterations: 3
```

Routing logic:

```text
Score >= 7
    ↓
Finalizer

Score < 7 AND iterations < 3
    ↓
Researcher → Evaluator

Iterations >= 3
    ↓
Finalizer
```

This provides both a **quality-based exit condition** and a **maximum-iteration safeguard**.

## Project Structure

```text
ai-research-workflow/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── state/
│   │   ├── __init__.py
│   │   └── research_state.py
│   │
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── evaluator.py
│   │   └── finalizer.py
│   │
│   └── graph/
│       ├── __init__.py
│       └── workflow.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/MSHAH-byte/ai-research-workflow.git
cd ai-research-workflow
```

### 2. Create a Python 3.12 virtual environment

```bash
py -3.12 -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_actual_groq_api_key
```

You can use `.env.example` as a template.

**Never commit your actual `.env` file or API key.**

## Running the Application

Start the application with:

```bash
python -m app.main
```

You will see:

```text
AI Research Workflow
Enter 'quit' or 'exit' to end the program.

Enter a research topic:
```

Enter a topic such as:

```text
What is Retrieval-Augmented Generation?
```

The workflow processes the topic and displays the final answer.

To stop the application:

```text
quit
```

or:

```text
exit
```

## Example Workflow

Example input:

```text
What is Retrieval-Augmented Generation?
```

Example execution:

```text
Planner
   ↓
Researcher
   ↓
Evaluator → 9/10
   ↓
Finalizer
   ↓
Final Answer
```

When improvement is required:

```text
Planner
   ↓
Researcher → Iteration 1
   ↓
Evaluator
   ↓
Researcher → Iteration 2
   ↓
Evaluator
   ↓
Researcher → Iteration 3
   ↓
Evaluator
   ↓
Finalizer
```

## What This Project Demonstrates

This project was built to practice core **LangGraph** concepts in a practical application:

* State-driven AI workflows
* Node-based architecture
* Sequential execution
* Conditional edges
* Cyclic workflows
* State updates between nodes
* LLM orchestration
* Automated evaluation
* Feedback loops
* Workflow termination and safeguards

## Limitations

This project is a workflow demonstration rather than a production research engine.

Currently:

* The researcher does not perform live web search.
* The system does not use RAG or a vector database.
* There is no persistent conversation memory.
* Research quality depends on the underlying LLM.
* The evaluator is itself LLM-based.
* The application currently uses a command-line interface.
* API authentication and production deployment are not included.

These limitations are intentional to keep the project focused on **LangGraph workflow orchestration**.

## Future Improvements

Possible extensions include:

* Web search tools
* RAG integration
* Source citation and verification
* Persistent conversation state
* Human-in-the-loop approval
* Tool-calling research agents
* FastAPI backend
* Observability and evaluation pipelines
* Production deployment

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Muhammad Shah**

GitHub: [MSHAH-byte](https://github.com/MSHAH-byte)
