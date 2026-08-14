# Automated Research & Quality-Gated Report Generator Agent

A LangGraph-based research agent that automatically researches a user query, generates a structured report, evaluates the report against quality criteria, and iterates until the result meets the required quality threshold or reaches a maximum iteration limit.

The project is designed as a practical exploration of **LangGraph's core concepts**: stateful workflows, nodes, conditional edges, iterative execution, persistence, and thread-based state management.

## Overview

Traditional LLM applications often follow a simple pipeline:

```text
User Query → Search → LLM → Answer
```

This project uses a more structured agentic workflow:

```text
                    ┌──────────────┐
                    │    START     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Research   │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Writer    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Critic    │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Quality Gate │
                    └───┬──────┬───┘
                        │      │
              Insufficient   Approved
                        │      │
                        ▼      ▼
                   Research   END
```

If the generated report does not satisfy the quality criteria, the graph can continue through another research/writing cycle. The workflow maintains its state throughout the process.

## Project Goals

This project focuses on understanding and implementing the fundamental building blocks of **LangGraph**:

* Defining and managing graph state
* Building workflows from independent nodes
* Connecting nodes with directed edges
* Implementing conditional routing
* Creating iterative agentic workflows
* Controlling loops using state
* Evaluating LLM-generated outputs
* Persisting graph state with a checkpointer
* Using `thread_id` to manage independent executions
* Inspecting and resuming previous graph executions

The goal is not simply to produce a report, but to build a clean and reusable **stateful agent workflow**.

## Architecture

### State

The graph maintains a shared state throughout the execution.

A conceptual state contains:

```text
query
research_results
draft
critique
iteration_count
final_report
```

Each node reads the information it needs from the state and returns updates that are merged back into the graph state.

### Nodes

#### 1. Research Node

Responsible for gathering information relevant to the user's query.

```text
State
  │
  ▼
Research Node
  │
  └──► Search / Retrieval Tools
          │
          ▼
    Research Results
```

The collected information is stored in the graph state for downstream nodes.

#### 2. Writer Node

Uses the query and available research to produce a structured report.

```text
Query + Research + Previous Critique
                │
                ▼
           Writer Node
                │
                ▼
              Draft
```

The writer can use previous critique feedback to improve subsequent versions of the report.

#### 3. Critic Node

Evaluates the generated draft against predefined quality requirements.

The critic determines whether the report is sufficiently:

* Relevant to the original query
* Supported by the available research
* Complete
* Clear and well structured
* Consistent with the required report format

The resulting feedback is stored in the graph state.

## Conditional Routing

After the critic evaluates the draft, the graph uses a conditional edge to determine what happens next.

Conceptually:

```text
                 ┌──────────────┐
                 │    Critic    │
                 └──────┬───────┘
                        │
                        ▼
                should_continue()
                   /          \
                  /            \
          Not sufficient      Approved
               │                  │
               ▼                  ▼
           Research              END
               │
               ▼
            Writer
               │
               ▼
             Critic
```

The graph can therefore improve its own output through multiple iterations rather than accepting the first generated draft.

A maximum iteration limit is maintained in the state to prevent an uncontrolled loop.

## Persistence & Threading

The project uses a **LangGraph checkpointer** to persist graph state.

This enables executions to be associated with a `thread_id`, allowing the application to:

* Keep independent conversations/executions separate
* Inspect the state of a previous execution
* Resume an execution
* Maintain state across graph invocations
* Experiment with LangGraph's persistence capabilities

Conceptually:

```text
thread_id = "research-session-001"

        │
        ▼
┌─────────────────────────┐
│   Persistent Graph      │
│                         │
│ Query                   │
│ Research Results        │
│ Draft                   │
│ Critique                │
│ Iteration Count         │
│ Final Report            │
└─────────────────────────┘
```

## Quality-Gated Generation

The defining feature of the project is the quality gate between generation and completion.

Instead of:

```text
Generate → Return
```

the system follows:

```text
Generate
   │
   ▼
Evaluate
   │
   ├──► Good enough → Return
   │
   └──► Needs improvement
              │
              ▼
           Research
              │
              ▼
            Write
              │
              ▼
           Evaluate
```

This provides a practical example of how evaluation can be incorporated directly into an LLM workflow.

## Example Execution

Given a query such as:

```text
What are the main applications of retrieval-augmented generation?
```

the workflow might proceed as follows:

```text
Iteration 1
───────────
Research
   ↓
Collect relevant sources
   ↓
Generate report
   ↓
Critique
   ↓
Insufficient coverage

Iteration 2
───────────
Research
   ↓
Expand / refine research
   ↓
Generate improved report
   ↓
Critique
   ↓
Approved

Final Report
```

The exact number of iterations depends on the quality-gate result and the configured iteration limit.

## Technologies

* **Python**
* **LangGraph**
* **LangChain**
* **LLM provider**
* **Web search / retrieval tools**
* **LangGraph Checkpointing**
* **FastAPI** *(if an API layer is included)*

## Project Structure

A possible project structure is:

```text
automated-research-agent/
│
├── app/
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   ├── edges.py
│   │   └── graph.py
│   │
│   ├── tools/
│   │   └── search.py
│   │
│   ├── config.py
│   └── main.py
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

The exact structure may evolve as the project develops.

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd automated-research-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Or on Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example` and add the required API credentials.

### 5. Run the application

Use the project's configured entry point to start the graph/application.

## Core LangGraph Concepts Demonstrated

| Concept                | Implementation                              |
| ---------------------- | ------------------------------------------- |
| State                  | Shared research workflow state              |
| Nodes                  | Research, Writer, and Critic                |
| Edges                  | Sequential node transitions                 |
| Conditional Edges      | Quality-gate routing                        |
| Loops                  | Iterative research and generation           |
| State-based Control    | Maximum iteration limit                     |
| Checkpointing          | Persistent graph state                      |
| Threading              | Independent execution state via `thread_id` |
| Human/Agent Evaluation | Critic-based quality assessment             |

## Future Improvements

Potential extensions include:

* Source citation and attribution
* More specialized research tools
* Parallel research agents
* Source-quality scoring
* Human approval checkpoints
* Structured report schemas
* More sophisticated quality metrics
* Streaming graph execution
* LangGraph Studio integration
* Persistent database-backed checkpointing
* REST API and frontend interface
* Observability and tracing

## Learning Outcomes

By completing this project, the main concepts reinforced are:

1. Designing stateful LLM workflows
2. Modeling workflows as graphs
3. Separating agent responsibilities into nodes
4. Implementing conditional execution
5. Building controlled agentic loops
6. Using evaluation to improve generated content
7. Persisting graph state
8. Managing executions with threads
9. Designing modular LangGraph applications

## License

This project is intended primarily as a learning and experimentation project.
