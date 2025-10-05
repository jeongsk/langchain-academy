---
title: LangGraph quickstart
source: https://langchain-ai.github.io/langgraph/agents/agents/
---

## LangGraph quickstart

This guide shows you how to set up and use LangGraph's **prebuilt**, **reusable** components, which are designed to help you construct agentic systems quickly and reliably.

## Prerequisites

Before you start this tutorial, ensure you have the following:

- An [Anthropic](https://console.anthropic.com/settings/keys) API key

## 1\. Install dependencies

If you haven't already, install LangGraph and LangChain:

```js
pip install -U langgraph "langchain[anthropic]"
```

Info

`langchain[anthropic]` is installed so the agent can call the [model](https://python.langchain.com/docs/integrations/chat/).

## 2\. Create an agent

To create an agent, use [`create_react_agent`](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent):

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

```python
from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",  
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

## 3\. Configure an LLM

To configure an LLM with specific parameters, such as temperature, use [init\_chat\_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html):

<sup><i>API Reference: <a href="https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html">init_chat_model</a> | <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

For more information on how to configure LLMs, see [Models](https://langchain-ai.github.io/langgraph/agents/models/).

## 4\. Add a custom prompt

Prompts instruct the LLM how to behave. Add one of the following types of prompts:

- **Static**: A string is interpreted as a **system message**.
- **Dynamic**: A list of messages generated at **runtime**, based on input or configuration.

Define a fixed prompt string or list of messages:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    # A static prompt that never changes
    prompt="Never answer questions about the weather."
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

Define a function that returns a message list based on the agent's state and configuration:

```python
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent

def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:  
    user_name = config["configurable"].get("user_name")
    system_msg = f"You are a helpful assistant. Address the user as {user_name}."
    return [{"role": "system", "content": system_msg}] + state["messages"]

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt=prompt
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config={"configurable": {"user_name": "John Smith"}}
)
```
1. Dynamic prompts allow including non-message [context](https://langchain-ai.github.io/langgraph/agents/context/) when constructing an input to the LLM, such as:
	- Information passed at runtime, like a `user_id` or API credentials (using `config`).
	- Internal agent state updated during a multi-step reasoning process (using `state`).
	Dynamic prompts can be defined as functions that take `state` and `config` and return a list of messages to send to the LLM.

For more information, see [Context](https://langchain-ai.github.io/langgraph/agents/context/).

## 5\. Add memory

To allow multi-turn conversations with an agent, you need to enable [persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/) by providing a checkpointer when creating an agent. At runtime, you need to provide a config containing `thread_id` — a unique identifier for the conversation (session):

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a> | <a href="https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.InMemorySaver">InMemorySaver</a></i></sup>

```python
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    checkpointer=checkpointer  
)

# Run the agent
config = {"configurable": {"thread_id": "1"}}
sf_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]},
    config  
)
ny_response = agent.invoke(
    {"messages": [{"role": "user", "content": "what about new york?"}]},
    config
)
```

When you enable the checkpointer, it stores agent state at every step in the provided checkpointer database (or in memory, if using `InMemorySaver`).

Note that in the above example, when the agent is invoked the second time with the same `thread_id`, the original message history from the first conversation is automatically included, together with the new user input.

For more information, see [Memory](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/).

## 6\. Configure structured output

To produce structured responses conforming to a schema, use the `response_format` parameter. The schema can be defined with a `Pydantic` model or `TypedDict`. The result will be accessible via the `structured_response` field.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

LLM post-processing

Structured output requires an additional call to the LLM to format the response according to the schema.

- [Deploy your agent locally](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/)
- [Learn more about prebuilt agents](https://langchain-ai.github.io/langgraph/agents/overview/)
- [LangGraph Platform quickstart](https://langchain-ai.github.io/langgraph/cloud/quick_start/)