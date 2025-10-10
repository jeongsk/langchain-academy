---
source: https://langchain-ai.github.io/langgraph/agents/agents/
title: "사전 구축된 에이전트로 빠르게 시작하기: create_react_agent"
created: 2025-10-10T21:55:00
---

## LangGraph 빠른 시작

이 가이드는 에이전트 시스템을 빠르고 안정적으로 구축할 수 있도록 설계된 LangGraph의 **사전 구축된**, **재사용 가능한** 컴포넌트를 설정하고 사용하는 방법을 보여줍니다.

## 사전 요구 사항

이 튜토리얼을 시작하기 전에 다음이 필요합니다:

- [Anthropic](https://console.anthropic.com/settings/keys) API 키

## 1\. 종속성 설치

아직 설치하지 않았다면 LangGraph와 LangChain을 설치하세요:

```js
pip install -U langgraph "langchain[anthropic]"
```

정보

`langchain[anthropic]`는 에이전트가 [모델](https://python.langchain.com/docs/integrations/chat/)을 호출할 수 있도록 설치됩니다.

## 2\. 에이전트 생성

에이전트를 생성하려면 [`create_react_agent`](https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent)를 사용하세요:

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

# 에이전트 실행
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

## 3\. LLM 구성

temperature와 같은 특정 매개변수로 LLM을 구성하려면 [init\_chat\_model](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)을 사용하세요:

<sup><i>API Reference: <a href="https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html">init_chat_model</a> | <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

LLM 구성 방법에 대한 자세한 내용은 [Models](https://langchain-ai.github.io/langgraph/agents/models/)를 참조하세요.

## 4\. 사용자 정의 프롬프트 추가

프롬프트는 LLM의 동작 방식을 지시합니다. 다음 유형의 프롬프트 중 하나를 추가하세요:

- **정적**: 문자열은 **시스템 메시지**로 해석됩니다.
- **동적**: 입력 또는 구성을 기반으로 **런타임**에 생성되는 메시지 목록입니다.

고정된 프롬프트 문자열 또는 메시지 목록을 정의하세요:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    # 변경되지 않는 정적 프롬프트
    prompt="Never answer questions about the weather."
)

agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

에이전트의 상태 및 구성을 기반으로 메시지 목록을 반환하는 함수를 정의하세요:

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

1. 동적 프롬프트를 사용하면 LLM에 대한 입력을 구성할 때 메시지가 아닌 [컨텍스트](https://langchain-ai.github.io/langgraph/agents/context/)를 포함할 수 있습니다:
 - `user_id`나 API 자격 증명과 같이 런타임에 전달되는 정보(`config` 사용).
 - 다단계 추론 프로세스 중에 업데이트되는 내부 에이전트 상태(`state` 사용).
 동적 프롬프트는 `state`와 `config`를 받아 LLM에 보낼 메시지 목록을 반환하는 함수로 정의할 수 있습니다.

자세한 내용은 [Context](https://langchain-ai.github.io/langgraph/agents/context/)를 참조하세요.

## 5\. 메모리 추가

에이전트와의 다회전 대화를 허용하려면 에이전트 생성 시 체크포인터를 제공하여 [지속성](https://langchain-ai.github.io/langgraph/concepts/persistence/)을 활성화해야 합니다. 런타임에는 대화(세션)의 고유 식별자인 `thread_id`가 포함된 config를 제공해야 합니다:

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

# 에이전트 실행
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

체크포인터를 활성화하면 제공된 체크포인터 데이터베이스(또는 `InMemorySaver`를 사용하는 경우 메모리)에 모든 단계에서 에이전트 상태가 저장됩니다.

위 예제에서 동일한 `thread_id`로 에이전트가 두 번째로 호출되면 첫 번째 대화의 원본 메시지 기록이 새 사용자 입력과 함께 자동으로 포함됩니다.

자세한 내용은 [Memory](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/)를 참조하세요.

## 6\. 구조화된 출력 구성

스키마를 준수하는 구조화된 응답을 생성하려면 `response_format` 매개변수를 사용하세요. 스키마는 `Pydantic` 모델 또는 `TypedDict`로 정의할 수 있습니다. 결과는 `structured_response` 필드를 통해 액세스할 수 있습니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

LLM 후처리

구조화된 출력은 스키마에 따라 응답을 포맷하기 위해 LLM에 대한 추가 호출이 필요합니다.

- [에이전트를 로컬에 배포하기](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/)
- [사전 구축된 에이전트에 대해 자세히 알아보기](https://langchain-ai.github.io/langgraph/agents/overview/)
- [LangGraph Platform 빠른 시작](https://langchain-ai.github.io/langgraph/cloud/quick_start/)
