---
title: "개요"
source: "https://langchain-ai.github.io/langgraph/concepts/low_level/"
---

## Graph API 개념

## 그래프

LangGraph는 에이전트 워크플로우를 그래프로 모델링합니다. 에이전트의 동작은 세 가지 핵심 구성 요소로 정의됩니다:

1. **State**: 현재 애플리케이션의 스냅샷을 나타내는 공유 데이터 구조입니다. 어떤 데이터 타입이든 될 수 있지만, 일반적으로 공유 상태 스키마를 사용해 정의합니다.
2. **Nodes**: 에이전트의 로직을 인코딩하는 함수입니다. 현재 상태를 입력으로 받아 연산이나 부수 효과를 수행하고, 업데이트된 상태를 반환합니다.
3. **Edges**: 현재 상태에 따라 다음에 실행할 Node를 결정하는 함수입니다. 조건부 분기이거나 고정 전환일 수 있습니다.

Nodes와 Edges를 조합하면 시간이 흐름에 따라 상태가 변화하는 복잡하고 반복적인 워크플로우를 만들 수 있습니다. 실제 힘은 LangGraph가 상태를 관리하는 방식에 있습니다. 강조하자면, Nodes와 Edges는 단순히 함수일 뿐이며, LLM을 포함할 수도 있고 순수 코드만 포함할 수도 있습니다.

요약: *노드는 작업을 수행하고, 엣지는 다음에 무엇을 할지 알려줍니다*.

LangGraph의 기본 그래프 알고리즘은 메시지 전달을 사용해 일반 프로그램을 정의합니다. Node가 작업을 마치면 하나 이상의 엣지를 따라 다른 노드에 메시지를 보냅니다. 수신 노드는 자신의 함수를 실행하고, 결과 메시지를 다음 노드에 전달하며 이 과정이 계속됩니다. 이는 Google의 Pregel 시스템에서 영감을 받아, 프로그램이 이산적인 “슈퍼스텝”으로 진행됩니다.

슈퍼스텝은 그래프 노드 전체를 한 번 순회하는 단일 반복으로 볼 수 있습니다. 병렬로 실행되는 노드들은 같은 슈퍼스텝에 속하고, 순차적으로 실행되는 노드들은 별도의 슈퍼스텝에 속합니다. 그래프 실행이 시작될 때 모든 노드는 `inactive` 상태에서 시작합니다. 노드는 들어오는 엣지(또는 “채널”) 중 하나에서 새로운 메시지(상태)를 받으면 `active`가 되고, 함수를 실행해 업데이트를 반환합니다. 각 슈퍼스텝이 끝날 때, 들어오는 메시지가 없는 노드들은 `halt`를 선택해 자신을 `inactive`로 표시합니다. 모든 노드가 `inactive`이고 전송 중인 메시지가 없을 때 그래프 실행이 종료됩니다.

### StateGraph

`StateGraph` 클래스는 사용해야 할 주요 그래프 클래스입니다. 이는 사용자가 정의한 State 객체를 매개변수로 받습니다.

### 그래프 컴파일

그래프를 만들려면 먼저 State를 정의하고, Nodes와 Edges를 추가한 뒤 컴파일합니다. 컴파일이 정확히 무엇이며 왜 필요한가요?

컴파일은 매우 간단한 단계입니다. 그래프 구조에 대한 기본 검사를 수행합니다(고아 노드가 없는지 등). 또한 여기서 체크포인터와 브레이크포인트 같은 런타임 인자를 지정할 수 있습니다. 그래프를 컴파일하려면 `.compile` 메서드를 호출하면 됩니다:

```python
graph = graph_builder.compile(...)
```

**그래프를 사용하기 전에 반드시 컴파일해야 합니다.**

## State

그래프를 정의할 때 가장 먼저 하는 일은 그래프의 State를 정의하는 것입니다. State는 그래프의 스키마와 업데이트를 적용하는 방법을 지정하는 reducer 함수들로 구성됩니다. State 스키마는 모든 Node와 Edge에 대한 입력 스키마가 되며, TypedDict 혹은 Pydantic 모델 중 하나로 구현할 수 있습니다. 모든 Node는 State에 업데이트를 내보내며, 지정된 reducer 함수가 이를 적용합니다.

### 스키마

그래프 스키마를 지정하는 가장 일반적인 방법은 TypedDict를 사용하는 것입니다. 기본값을 제공하려면 dataclass를 사용할 수 있습니다. 재귀적인 데이터 검증이 필요하면 Pydantic의 BaseModel을 사용할 수도 있지만, 성능은 TypedDict나 dataclass보다 낮습니다.

기본적으로 그래프는 동일한 입력·출력 스키마를 가집니다. 필요에 따라 명시적인 입력·출력 스키마를 별도로 지정할 수도 있습니다. 이는 키가 많고, 일부는 입력 전용, 일부는 출력 전용일 때 유용합니다. 자세한 내용은 가이드를 참고하세요.

#### 다중 스키마

대부분의 그래프 노드는 단일 스키마를 공유합니다. 즉, 동일한 상태 채널을 읽고 씁니다. 하지만 다음과 같은 경우에는 더 세밀한 제어가 필요합니다:

- 내부 노드는 그래프 입력·출력에 필요하지 않은 정보를 전달할 수 있습니다.
- 그래프에 별도의 입력·출력 스키마를 사용하고 싶을 때, 출력은 예를 들어 단일 관련 키만 포함하도록 할 수 있습니다.

노드가 내부적으로만 사용하는 PrivateState와 같은 개인 스키마를 정의해 비공개 채널에 쓰는 것도 가능합니다. 이러한 경우, 전체 스키마는 InternalState이며, input·output 스키마는 InternalState의 부분집합으로 제한됩니다. 자세한 내용은 가이드를 확인하세요.

예시:

```python
class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str

class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

class PrivateState(TypedDict):
    bar: str

def node_1(state: InputState) -> OverallState:
    # OverallState에 쓰기
    return {"foo": state["user_input"] + " name"}

def node_2(state: OverallState) -> PrivateState:
    # OverallState를 읽고 PrivateState에 쓰기
    return {"bar": state["foo"] + " is"}

def node_3(state: PrivateState) -> OutputState:
    # PrivateState를 읽고 OutputState에 쓰기
    return {"graph_output": state["bar"] + " Lance"}

builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()
graph.invoke({"user_input":"My"})
# {'graph_output': 'My name is Lance'}
```

두 가지 중요한 포인트:

1. `node_1`은 `state: InputState`를 입력 스키마로 받지만, OverallState에 있는 `foo` 채널에 씁니다. 이는 노드가 그래프 전체에 정의된 어떤 상태 채널에도 쓸 수 있기 때문입니다. 그래프 상태는 초기화 시 정의된 모든 채널(OverallState, InputState, OutputState)의 합집합입니다.
2. `node_2`에서 `PrivateState`를 사용하고 있습니다. `StateGraph` 초기화 시 `PrivateState`를 명시하지 않았지만, 해당 스키마가 존재하기 때문에 노드가 추가 채널을 선언하고 사용할 수 있습니다.

### Reducers

Reducer는 노드에서 반환된 업데이트가 State에 어떻게 적용되는지를 이해하는 핵심 요소입니다. State의 각 키는 독립적인 reducer 함수를 가집니다. 명시적인 reducer가 없으면 기본적으로 해당 키의 값을 **덮어쓰기**합니다. 기본 reducer 외에도 여러 종류가 있습니다.

#### 기본 Reducer

다음 예시는 기본 reducer 사용법을 보여줍니다.

**예시 A:**

```python
from typing_extensions import TypedDict

class State(TypedDict):
    foo: int
    bar: list[str]
```

입력이 `{"foo": 1, "bar": ["hi"]}`이고, 첫 번째 Node가 `{"foo": 2}`를 반환하면 상태는 `{"foo": 2, "bar": ["hi"]}`가 됩니다. 두 번째 노드가 `{"bar": ["bye"]}`를 반환하면 최종 상태는 `{"foo": 2, "bar": ["bye"]}`가 됩니다.

**예시 B:**

```python
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]
```

여기서는 `bar` 키에 `operator.add` reducer를 지정했습니다. 입력이 `{"foo": 1, "bar": ["hi"]}`이고, 첫 번째 노드가 `{"foo": 2}`를 반환하면 상태는 `{"foo": 2, "bar": ["hi"]}`가 됩니다. 두 번째 노드가 `{"bar": ["bye"]}`를 반환하면 `bar` 리스트가 합쳐져 `{"foo": 2, "bar": ["hi", "bye"]}`가 됩니다.

### Graph State에서 메시지 다루기

#### 왜 메시지를 사용하나요?

대부분의 최신 LLM 제공자는 리스트 형태의 메시지를 입력으로 받는 챗 모델 인터페이스를 제공합니다. LangChain의 `ChatModel`은 특히 `Message` 객체 리스트를 입력으로 받습니다. 이러한 메시지는 `HumanMessage`(사용자 입력)나 `AIMessage`(LLM 응답) 등 다양한 형태가 있습니다. 자세한 내용은 해당 가이드를 참고하세요.

#### 그래프에 메시지 저장하기

대화 기록을 그래프 상태에 리스트 형태로 저장하고 싶다면, 해당 키에 reducer를 지정해야 합니다. reducer가 없으면 최신 메시지 리스트가 전체를 덮어씁니다. 리스트에 메시지를 **추가**하고 싶다면 `operator.add`를 reducer로 사용할 수 있습니다.

수동으로 메시지를 업데이트할 때는 `operator.add`가 기존 리스트에 새 메시지를 **추가**하지만, 기존 메시지를 **덮어쓰기**하려면 메시지 ID를 추적하는 reducer가 필요합니다. 이를 위해 미리 제공되는 `add_messages` 함수를 사용할 수 있습니다. 새 메시지는 리스트에 추가하고, 기존 메시지는 올바르게 업데이트합니다.

#### 직렬화

`add_messages`는 상태 업데이트가 들어올 때마다 메시지를 LangChain `Message` 객체로 역직렬화합니다. 따라서 다음과 같은 형태의 입력이 가능합니다:

```python
# 지원되는 형태
{"messages": [HumanMessage(content="message")]}

# 또한 지원되는 형태
{"messages": [{"type": "human", "content": "message"}]}
```

역직렬화된 메시지는 `state["messages"][-1].content`와 같이 점 표기법으로 접근할 수 있습니다. 아래 예시는 `add_messages`를 reducer로 사용하는 그래프를 보여줍니다.

```python
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict

class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

#### MessagesState

메시지 리스트를 상태에 포함하는 경우가 흔하기 때문에, `MessagesState`라는 사전 정의된 상태가 있습니다. 이는 `messages` 키 하나만 가지고 있으며, `add_messages` reducer를 사용합니다. 보통 여기서 추가 필드를 정의해 사용합니다:

```python
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]
```

## Nodes

LangGraph에서 노드는 Python 함수(동기 또는 비동기)이며, 다음 인자를 받습니다:

1. `state`: 그래프의 **state**
2. `config`: `RunnableConfig` 객체(예: `thread_id`, `tags` 등)
3. `runtime`: `Runtime` 객체(예: `store`, `stream_writer` 등)

노드를 그래프에 추가하려면 `add_node` 메서드를 사용합니다:

```python
from dataclasses import dataclass
from typing_extensions import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

class State(TypedDict):
    input: str
    results: str

@dataclass
class Context:
    user_id: str

builder = StateGraph(State)

def plain_node(state: State):
    return state

def node_with_runtime(state: State, runtime: Runtime[Context]):
    print("In node: ", runtime.context.user_id)
    return {"results": f"Hello, {state['input']}!"}

def node_with_config(state: State, config: RunnableConfig):
    print("In node with thread_id: ", config["configurable"]["thread_id"])
    return {"results": f"Hello, {state['input']}!"}

builder.add_node("plain_node", plain_node)
builder.add_node("node_with_runtime", node_with_runtime)
builder.add_node("node_with_config", node_with_config)
```

함수는 내부적으로 `RunnableLambda`로 변환되어 배치 및 비동기 지원, 트레이싱, 디버깅 기능을 얻게 됩니다. 이름을 지정하지 않으면 함수 이름이 기본 노드 이름이 됩니다.

### START Node

`START` 노드는 사용자 입력을 그래프에 전달하는 특수 노드이며, 그래프 진입점을 지정하는 데 사용됩니다.

```python
from langgraph.graph import START

graph.add_edge(START, "node_a")
```

### END Node

`END` 노드는 종료 노드이며, 작업이 끝난 후 더 이상 실행할 엣지가 없음을 나타냅니다.

```python
from langgraph.graph import END

graph.add_edge("node_a", END)
```

### Node Caching

노드 결과를 캐시하려면 그래프 컴파일 시 캐시를 지정하고, 각 노드에 캐시 정책을 설정합니다.

```python
import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

class State(TypedDict):
    x: int
    result: int

builder = StateGraph(State)

def expensive_node(state: State) -> dict[str, int]:
    # 비용이 많이 드는 연산
    time.sleep(2)
    return {"result": state["x"] * 2}

builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=3))
builder.set_entry_point("expensive_node")
builder.set_finish_point("expensive_node")

graph = builder.compile(cache=InMemoryCache())

print(graph.invoke({"x": 5}, stream_mode='updates'))
# [{'expensive_node': {'result': 10}}]
print(graph.invoke({"x": 5}, stream_mode='updates'))
# [{'expensive_node': {'result': 10}, '__metadata__': {'cached': True}}]
```

## Edges

Edges는 로직 흐름을 정의하고 그래프가 언제 멈출지를 결정합니다. 주요 유형은 다음과 같습니다:

- **Normal Edges**: 한 노드에서 다음 노드로 직접 연결합니다.
- **Conditional Edges**: 함수를 호출해 다음 노드(들)를 결정합니다.
- **Entry Point**: 사용자 입력이 들어올 때 처음 호출되는 노드.
- **Conditional Entry Point**: 사용자 입력에 따라 시작 노드를 선택합니다.

노드는 **여러 개의** outgoing edge를 가질 수 있습니다. 여러 개의 outgoing edge가 있으면 해당 목적지 노드들이 **병렬**로 다음 슈퍼스텝에서 실행됩니다.

### Normal Edges

항상 A 노드에서 B 노드로 이동하고 싶다면 `add_edge`를 사용합니다:

```python
graph.add_edge("node_a", "node_b")
```

### Conditional Edges

옵션으로 1개 이상의 엣지(또는 종료)를 라우팅하고 싶다면 `add_conditional_edges`를 사용합니다:

```python
graph.add_conditional_edges("node_a", routing_function)
```

`routing_function`은 현재 `state`를 받아 다음에 보낼 노드 이름(또는 리스트)을 반환합니다. 반환값이 바로 다음 노드 이름이 되며, 여러 노드가 동시에 실행됩니다.

딕셔너리를 제공해 반환값을 노드 이름에 매핑할 수도 있습니다:

```python
graph.add_conditional_edges(
    "node_a",
    routing_function,
    {True: "node_b", False: "node_c"}
)
```

#### 팁

조건부 흐름과 상태 업데이트를 동시에 하고 싶다면 `Command`를 사용하세요. 자세한 내용은 아래 **Command** 섹션을 참고하십시오.

### Entry Point

첫 번째 실행 노드를 지정하려면 `START` 노드에서 실제 노드로 엣지를 연결합니다:

```python
from langgraph.graph import START

graph.add_edge(START, "node_a")
```

### Conditional Entry Point

시작 시점에 다른 노드로 진입하고 싶다면 `add_conditional_edges`를 `START`와 함께 사용합니다:

```python
from langgraph.graph import START

graph.add_conditional_edges(START, routing_function)
```

필요에 따라 반환값을 노드 이름에 매핑할 수 있습니다:

```python
graph.add_conditional_edges(START, routing_function, {True: "node_b", False: "node_c"})
```

## Send

대부분의 노드와 엣지는 사전에 정의된 상태와 동일한 상태를 사용합니다. 그러나 경우에 따라 **동적으로** 엣지를 생성하거나, 각 객체마다 별도의 State가 필요할 때가 있습니다. 예를 들어, **map‑reduce** 패턴에서는 첫 번째 노드가 객체 리스트를 생성하고, 그 리스트의 각 항목에 대해 별도의 노드를 적용해야 합니다. 이때 `Send` 객체를 사용해 동적으로 엣지를 만들 수 있습니다.

```python
def continue_to_jokes(state: OverallState):
    return [Send("generate_joke", {"subject": s}) for s in state['subjects']]

graph.add_conditional_edges("node_a", continue_to_jokes)
```

## Command

`Command`는 **상태 업데이트**와 **제어 흐름**을 하나의 노드에서 동시에 수행하고 싶을 때 사용합니다.

```python
def my_node(state: State) -> Command[Literal["my_other_node"]]:
    return Command(
        # 상태 업데이트
        update={"foo": "bar"},
        # 제어 흐름
        goto="my_other_node"
    )
```

조건부 로직을 포함할 수도 있습니다:

```python
def my_node(state: State) -> Command[Literal["my_other_node"]]:
    if state["foo"] == "bar":
        return Command(update={"foo": "baz"}, goto="my_other_node")
```

**주의**: `Command`를 반환하는 함수는 반환 타입에 라우팅될 노드 이름 리스트를 명시해야 합니다(`Command[Literal["my_other_node"]]`). 이는 그래프 렌더링과 타입 검증에 필요합니다.

### 언제 Command를 사용하고 Conditional Edges를 사용하지 않을까?

- **Command**: 상태를 업데이트하면서 동시에 다른 노드로 이동해야 할 때(예: 멀티‑에이전트 핸드오프).
- **Conditional Edges**: 상태 업데이트 없이 순수하게 흐름만 제어하고 싶을 때.

## 부모 그래프에서 노드 이동하기

서브그래프를 사용할 때, 서브그래프 내부 노드에서 **부모 그래프**의 다른 노드로 이동하고 싶다면 `Command`에 `graph=Command.PARENT`를 지정합니다:

```python
def my_node(state: State) -> Command[Literal["other_subgraph"]]:
    return Command(
        update={"foo": "bar"},
        goto="other_subgraph",   # 부모 그래프에 있는 노드
        graph=Command.PARENT
    )
```

부모 그래프에 있는 키를 업데이트하려면 해당 키에 대한 **reducer**를 부모 그래프의 State에 정의해야 합니다.

## 도구 내부에서 사용하기

툴 내부에서 그래프 상태를 업데이트하는 경우가 많습니다. 예를 들어, 고객 지원 애플리케이션에서 초기 단계에 고객 정보를 조회하고 싶을 때 툴을 호출해 상태를 업데이트할 수 있습니다. 자세한 내용은 해당 가이드를 참고하세요.

## Human‑in‑the‑loop

`Command`는 인간‑인‑루프 워크플로우에서도 중요한 역할을 합니다. `interrupt()`로 사용자 입력을 받고, 그 입력을 `Command(resume="User input")`으로 전달해 실행을 재개합니다. 자세한 내용은 개념 가이드를 확인하세요.

## Graph Migrations

LangGraph는 체크포인터를 사용해 그래프 정의(노드, 엣지, 상태)를 **마이그레이션**할 수 있습니다.

- **완료된 스레드**: 전체 토폴로지를 자유롭게 변경 가능(노드 추가·삭제·이름 변경 등).
- **중단된 스레드**: 노드 삭제·이름 변경은 불가능(현재 진행 중인 노드가 사라질 위험).
- **상태**: 키 추가·삭제는 양방향 호환성을 가짐. 키 이름을 바꾸면 기존 스레드의 저장된 상태는 손실됨. 타입이 호환되지 않게 바뀌면 기존 스레드에 문제가 발생할 수 있음.

## Runtime Context

그래프를 만들 때 `context_schema`를 지정해 런타임 컨텍스트를 노드에 전달할 수 있습니다. 이는 모델 이름이나 데이터베이스 연결 같은, 그래프 상태와는 별개인 정보를 전달할 때 유용합니다.

```python
from dataclasses import dataclass

@dataclass
class ContextSchema:
    llm_provider: str = "openai"

graph = StateGraph(State, context_schema=ContextSchema)
```

런타임 시 `invoke`에 `context` 파라미터를 전달하면 노드 내부에서 접근할 수 있습니다:

```python
graph.invoke(inputs, context={"llm_provider": "anthropic"})
```

노드에서 컨텍스트를 사용하는 예시:

```python
from langgraph.runtime import Runtime

def node_a(state: State, runtime: Runtime[ContextSchema]):
    llm = get_llm(runtime.context.llm_provider)
    ...
```

자세한 내용은 [구성 가이드](docs/Graph%20API/Use%20the%20Graph%20API.md#런타임%20구성%20추가)를 참고하세요.

## Recursion Limit

재귀 제한은 그래프가 단일 실행 동안 수행할 수 있는 **최대 슈퍼스텝** 수를 정의합니다. 기본값은 25이며, `invoke`·`stream` 호출 시 `config` 딕셔너리의 `recursion_limit` 키로 조정할 수 있습니다. 이 값은 `configurable` 키 안이 아니라 최상위 `config`에 직접 넣어야 합니다.

```python
graph.invoke(inputs, config={"recursion_limit": 5}, context={"llm": "anthropic"})
```

자세한 내용은 [재귀 제한 가이드](docs/Graph%20API/Use%20the%20Graph%20API.md#루프%20생성%20및%20제어)를 확인하세요.
## Visualization

복잡한 그래프는 시각화가 도움이 됩니다. LangGraph는 여러 내장 시각화 방법을 제공하니, [시각화 가이드](docs/Graph%20API/Use%20the%20Graph%20API.md#그래프%20시각화)를 참고해 보세요.