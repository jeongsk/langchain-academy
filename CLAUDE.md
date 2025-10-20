# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Korean-language LangGraph academy course repository organized into three main tracks:
- **Foundation** (6 modules): Core LangGraph concepts from basics to deployment
- **Ambient Agents** (project series): Hands-on projects for building ambient agents
- **Tutorial**: Independent examples and advanced patterns

It uses Jupyter notebooks for interactive learning and includes LangGraph Studio integration for visual graph development.

## Technology Stack

- **Python**: 3.12+ (3.13 in use)
- **Package Manager**: uv (modern Python package installer)
- **Core Framework**: LangGraph 0.6.8+
- **LLM Provider**: OpenAI (primary), with Cohere support
- **Checkpointing**: SQLite-based persistence
- **Documentation**: MkDocs with Material theme (Korean language)

## Official Documentation References

When implementing code or solving problems, always refer to these official documentation sources:

- **LangGraph Python**: <https://langchain-ai.github.io/langgraph/llms.txt>
- **LangChain Python**: <https://python.langchain.com/llms.txt>

These LLM-optimized documentation files contain the most up-to-date API references, best practices, and implementation patterns.

## Development Environment Setup

### Environment Management

```bash
# Sync dependencies (creates/updates .venv)
uv sync

# Run commands without activating venv
uv run jupyter notebook
uv run python script.py

# Or activate manually
source .venv/bin/activate
```

### Required API Keys (.env file)

```bash
OPENAI_API_KEY=sk-xxx
LANGSMITH_API_KEY=      # Optional but recommended for tracing
TAVILY_API_KEY=         # Required for Module 4 (web search)
COHERE_API_KEY=         # Optional
```

### Running Jupyter Notebooks

```bash
jupyter notebook
# Navigate to module-X/ or langgraph-tutorial/ directories
```

## LangGraph Studio Development

Each module has a `studio/` subdirectory containing deployable graphs:

### Starting Studio Dev Server

```bash
cd module-X/studio/
langgraph dev
```

Server runs at:

- API: <http://127.0.0.1:2024>
- Studio UI: <https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024>
- API Docs: <http://127.0.0.1:2024/docs>

### Studio Configuration (langgraph.json)

- Defines multiple graphs in a single studio project
- Graph format: `"graph_name": "./file.py:graph"`
- Environment variables loaded from `.env` in studio directory
- Each studio folder needs its own `.env` file

Example structure:

```
module-1/studio/
  ├── langgraph.json      # Graph definitions
  ├── .env                # API keys
  ├── simple.py           # Graph: simple_graph
  ├── router.py           # Graph: router
  └── agent.py            # Graph: agent
```

## Code Architecture

### Foundation Structure (langgraph-foundation/)

Foundation course contains 6 modules teaching LangGraph fundamentals:

```
langgraph-foundation/
  ├── README.md          # Foundation series overview
  └── module-X/          # Individual modules (1-6)
      ├── README.md      # Module overview (Korean)
      ├── X-topic.ipynb  # Numbered learning notebooks
      └── studio/        # LangGraph Studio graphs
          ├── langgraph.json
          ├── .env.example
          ├── requirements.txt
          └── *.py       # Graph implementations
```

### Ambient Agents Structure (projects/ambient-agents/)

Project-based learning series for building ambient agents:

```
projects/
  └── ambient-agents/
      ├── README.md          # Series overview and Ambient Agents concepts
      └── project-X/         # Individual projects (1-6)
          ├── README.md      # Project overview and goals
          ├── X-topic.ipynb  # Learning notebooks
          └── studio/        # LangGraph Studio graphs
              ├── langgraph.json
              ├── .env.example
              ├── requirements.txt
              └── *.py       # Graph implementations
```

### Common LangGraph Patterns

**State Management**:

- Use `MessagesState` for conversation agents
- Use `StateGraph` for custom state schemas
- Reducers control state update behavior (append, replace, custom)

**Graph Construction**:

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(StateType)
builder.add_node("node_name", node_function)
builder.add_edge(START, "node_name")
builder.add_conditional_edges("node_name", routing_function, {"path": "target"})
graph = builder.compile()
```

**Checkpointing**:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string("checkpoints.db")
graph = builder.compile(checkpointer=memory)
```

### tutorial Structure

Tutorial are production-like implementations combining multiple concepts:

**QA-RAG-Agent Pattern** (`langgraph-tutorial/11-QA-RAG-Agent/studio/`):

- `states.py`: State schema definitions
- `nodes.py`: Business logic nodes
- `tools.py`: LLM tool definitions
- `retrievers.py`: Vector retrieval setup
- `graph.py`: Main graph assembly

This separation enables clean testing and modular development.

## Testing and Validation

### Running Individual Notebooks

Open specific notebooks in Jupyter and execute cells sequentially. Notebooks are self-contained learning units.

### Testing Studio Graphs

Use LangGraph Studio UI to:

- Visualize graph structure
- Test with sample inputs
- Debug state transitions
- View execution traces

### LangSmith Integration

Set `LANGSMITH_TRACING_V2=true` to automatically trace all LangGraph executions. Project names in code often specify the module (e.g., "10-langgraph-qa-rag-agent").

## Documentation

### Building Documentation Site

```bash
mkdocs serve              # Development server at http://127.0.0.1:8000
mkdocs build              # Build static site to site/
```

Documentation is configured for Korean language with Material theme and automatic page discovery via awesome-pages plugin.

### Deployment

GitHub Actions workflow (`.github/workflows/deploy_docs.yml`) handles documentation deployment.

## Module-Specific Notes

### Foundation Modules

**Module 1** (langgraph-foundation/module-1): Basics - simple graphs, chains, routers, agents with tool calling
**Module 2** (langgraph-foundation/module-2): State schemas, reducers, message trimming, external memory with SQLite
**Module 3** (langgraph-foundation/module-3): Human-in-the-loop patterns - breakpoints, state editing, time travel
**Module 4** (langgraph-foundation/module-4): Parallelization, sub-graphs, map-reduce patterns, research assistant
**Module 5** (langgraph-foundation/module-5): Advanced memory - BaseStore interface, StateSchema, Redis integration
**Module 6** (langgraph-foundation/module-6): Deployment and client connections to LangGraph servers

### Ambient Agents Projects

**Project 1** (projects/ambient-agents/project-1): [Project description - to be filled during learning]
**Project 2** (projects/ambient-agents/project-2): [Project description - to be filled during learning]
**Project 3+** (projects/ambient-agents/project-3+): [Additional projects - to be added]

## Common Development Tasks

### Adding a New Studio Graph

1. Create Python file in `langgraph-foundation/module-X/studio/` or `projects/ambient-agents/project-X/studio/`
2. Implement graph with `graph = builder.compile()`
3. Add entry to `langgraph.json`: `"graph_name": "./file.py:graph"`
4. Restart `langgraph dev` to load new graph

### Creating a New Project

Follow the pattern in `langgraph-tutorial/11-QA-RAG-Agent/`:

- Separate concerns into states, nodes, tools, retrievers
- Include `langgraph.json` for Studio integration
- Document in `langgraph-tutorial/README.md`

### Working with Vector Stores

Projects use FAISS (CPU) for vector similarity search. Retriever initialization typically happens in a separate module (e.g., `retrievers.py`) to keep graph definitions clean.

## Important Notes

- All documentation and module READMEs are in Korean
- Python 3.12+ required for optimal LangGraph compatibility
- Use `uv` instead of pip for dependency management
- Each studio directory must have its own `.env` file with API keys
- LangGraph Studio requires local dev server running via `langgraph dev`
