---
created: 2025-10-14 23:42:52
updated: 2025-10-14 23:45:40
source: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/
---
## 사람 개입 활성화하기

에이전트나 워크플로우에서 도구 호출을 검토하고 편집하며 승인하려면, 인터럽트를 사용하여 그래프를 일시 중지하고 사람의 입력을 기다리도록 합니다. 인터럽트는 LangGraph의 [지속성](https://langchain-ai.github.io/langgraph/concepts/persistence/) 레이어를 사용하여 그래프 상태를 저장하고, 재개할 때까지 그래프 실행을 무기한 일시 중지합니다.

> [!Info]
> 휴먼-인-더-루프 워크플로우에 대한 자세한 내용은 [휴먼-인-더-루프](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) 개념 가이드를 참조하세요.

## interrupt를 사용한 일시 중지

[동적 인터럽트](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/#key-capabilities)(동적 중단점이라고도 함)는 그래프의 현재 상태에 따라 트리거됩니다. 적절한 위치에서 [`interrupt` 함수](https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Interrupt)를 호출하여 동적 인터럽트를 설정할 수 있습니다. 그래프가 일시 중지되어 사람의 개입을 허용하고, 입력을 받은 후 그래프를 재개합니다. 이는 승인, 편집 또는 추가 컨텍스트 수집과 같은 작업에 유용합니다.

> [!Note]
> v1.0부터 `interrupt`가 그래프를 일시 중지하는 권장 방법입니다. `NodeInterrupt`는 더 이상 사용되지 않으며 v2.0에서 제거될 예정입니다.

그래프에서 `interrupt`를 사용하려면 다음이 필요합니다:

1. [**체크포인터 지정**](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpoints) - 각 단계 후 그래프 상태를 저장합니다.
2. **`interrupt()` 호출** - 적절한 위치에서 호출합니다. 예제는 [일반적인 패턴](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#common-patterns) 섹션을 참조하세요.
3. **그래프 실행** - [**스레드 ID**](https://langchain-ai.github.io/langgraph/concepts/persistence/#threads)와 함께 `interrupt`에 도달할 때까지 실행합니다.
4. **실행 재개** - `invoke` / `stream`을 사용합니다([**`Command` 프리미티브**](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#resume-using-the-command-primitive) 참조).

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt">interrupt</a> | <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command">Command</a></i></sup>

```python
from langgraph.types import interrupt, Command

def human_node(state: State):
    value = interrupt(
        {
            "text_to_revise": state["some_text"]  # 검토할 텍스트를 사람에게 표시
        }
    )
    return {
        "some_text": value  # 편집된 텍스트로 상태 업데이트
    }

graph = graph_builder.compile(checkpointer=checkpointer)  # 체크포인터로 그래프 컴파일

# 인터럽트에 도달할 때까지 그래프 실행
config = {"configurable": {"thread_id": "some_id"}}
result = graph.invoke({"some_text": "original text"}, config=config)
print(result['__interrupt__'])
# > [
# >    Interrupt(
# >       value={'text_to_revise': 'original text'},
# >       resumable=True,
# >       ns=['human_node:6ce9e64f-edef-fe5d-f7dc-511fa9526960']
# >    )
# > ]

print(graph.invoke(Command(resume="Edited text"), config=config))  # 편집된 텍스트로 재개
# > {'some_text': 'Edited text'}
```
확장 예제: `interrupt` 사용하기
```python
from typing import TypedDict
import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph

from langgraph.types import interrupt, Command

class State(TypedDict):
    some_text: str

def human_node(state: State):
    value = interrupt(
        {
            "text_to_revise": state["some_text"]  # 검토할 텍스트를 사람에게 표시
        }
    )
    return {
        "some_text": value  # 편집된 텍스트로 상태 업데이트
    }

# 그래프 구축
graph_builder = StateGraph(State)
graph_builder.add_node("human_node", human_node)
graph_builder.add_edge(START, "human_node")
checkpointer = InMemorySaver()  # 메모리 내 체크포인터 생성
graph = graph_builder.compile(checkpointer=checkpointer)
# 그래프를 실행하기 위해 스레드 ID 전달
config = {"configurable": {"thread_id": uuid.uuid4()}}
# 인터럽트에 도달할 때까지 그래프 실행
result = graph.invoke({"some_text": "original text"}, config=config)

print(result['__interrupt__'])
# > [
# >    Interrupt(
# >       value={'text_to_revise': 'original text'},
# >       resumable=True,
# >       ns=['human_node:6ce9e64f-edef-fe5d-f7dc-511fa9526960']
# >    )
# > ]
print(result["__interrupt__"])  # 인터럽트 정보 출력
# > [Interrupt(value={'text_to_revise': 'original text'}, id='6d7c4048049254c83195429a3659661d')]

print(graph.invoke(Command(resume="Edited text"), config=config))  # 편집된 텍스트로 재개
# > {'some_text': 'Edited text'}
```

> [!info] 0.4.0의 새로운 기능
> `__interrupt__`는 그래프가 중단되었을 때 반환되는 특수 키입니다. `invoke` 및 `ainvoke`에서 `__interrupt__` 지원이 버전 0.4.0에 추가되었습니다. 이전 버전을 사용하는 경우 `stream` 또는 `astream`을 사용할 때만 결과에서 `__interrupt__`를 볼 수 있습니다. `graph.get_state(thread_id)`를 사용하여 인터럽트 값을 가져올 수도 있습니다.

> [!Warning]
> 인터럽트는 개발자 경험 측면에서 Python의 input() 함수와 유사하지만, 중단 지점에서 자동으로 실행을 재개하지 않습니다. 대신 인터럽트가 사용된 노드 전체를 다시 실행합니다. 이러한 이유로 인터럽트는 일반적으로 노드의 시작 부분이나 전용 노드에 배치하는 것이 가장 좋습니다.

## Command 프리미티브를 사용한 재개

> [!Warning]
> `interrupt`에서 재개하는 것은 Python의 `input()` 함수와 다릅니다. `input()` 함수는 호출된 정확한 지점에서 실행을 재개하지만, `interrupt`는 그렇지 않습니다.

그래프 내에서 `interrupt` 함수를 사용하면 해당 지점에서 실행이 일시 중지되고 사용자 입력을 기다립니다.

실행을 재개하려면 `invoke` 또는 `stream` 메서드를 통해 제공할 수 있는 [`Command`](https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command) 프리미티브를 사용합니다. 그래프는 `interrupt(...)`가 처음 호출된 노드의 시작 부분부터 실행을 재개합니다. 이번에는 `interrupt` 함수가 다시 일시 중지하지 않고 `Command(resume=value)`에 제공된 값을 반환합니다. 노드 시작 부분부터 `interrupt`까지의 모든 코드가 다시 실행됩니다.

```python
# 사용자 입력을 제공하여 그래프 실행 재개
graph.invoke(Command(resume={"age": "25"}), thread_config)
```

### 한 번의 호출로 여러 인터럽트 재개하기

인터럽트 조건이 있는 노드들이 병렬로 실행될 때 작업 큐에 여러 인터럽트가 발생할 수 있습니다. 예를 들어, 다음 그래프에는 사람의 입력이 필요한 두 개의 노드가 병렬로 실행됩니다:

![image](https://langchain-ai.github.io/langgraph/how-tos/assets/human_in_loop_parallel.png)

그래프가 중단되어 정지된 후에는 `Command.resume`을 사용하여 인터럽트 ID와 재개 값의 딕셔너리 매핑을 전달함으로써 모든 인터럽트를 한 번에 재개할 수 있습니다.

<sup><i>API Reference: <a href="https://python.langchain.com/api_reference/core/runnables/langchain_core.runnables.config.RunnableConfig.html">RunnableConfig</a> | <a href="https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.InMemorySaver">InMemorySaver</a> | <a href="https://langchain-ai.github.io/langgraph/reference/constants/#langgraph.constants.START">START</a> | <a href="https://langchain-ai.github.io/langgraph/reference/graphs/#langgraph.graph.state.StateGraph">StateGraph</a> | <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt">interrupt</a> | <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command">Command</a></i></sup>

```python
from typing import TypedDict
import uuid
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command

class State(TypedDict):
    text_1: str
    text_2: str

def human_node_1(state: State):
    value = interrupt({"text_to_revise": state["text_1"]})
    return {"text_1": value}

def human_node_2(state: State):
    value = interrupt({"text_to_revise": state["text_2"]})
    return {"text_2": value}

graph_builder = StateGraph(State)
graph_builder.add_node("human_node_1", human_node_1)
graph_builder.add_node("human_node_2", human_node_2)

# START에서 두 노드를 병렬로 추가
graph_builder.add_edge(START, "human_node_1")
graph_builder.add_edge(START, "human_node_2")

checkpointer = InMemorySaver()
graph = graph_builder.compile(checkpointer=checkpointer)

thread_id = str(uuid.uuid4())
config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
result = graph.invoke(
    {"text_1": "original text 1", "text_2": "original text 2"}, config=config
)

# 인터럽트 ID와 값의 매핑으로 재개
resume_map = {
    i.id: f"edited text for {i.value['text_to_revise']}"
    for i in graph.get_state(config).interrupts
}
print(graph.invoke(Command(resume=resume_map), config=config))
# > {'text_1': 'edited text for original text 1', 'text_2': 'edited text for original text 2'}
```

## 일반적인 패턴

다음은 `interrupt`와 `Command`를 사용하여 구현할 수 있는 다양한 디자인 패턴입니다.

### 승인 또는 거부

![image](https://langchain-ai.github.io/langgraph/concepts/img/human_in_the_loop/approve-or-reject.png)

사람의 승인 또는 거부에 따라 그래프는 작업을 진행하거나 대체 경로를 취할 수 있습니다.

API 호출과 같은 중요한 단계 전에 그래프를 일시 중지하여 작업을 검토하고 승인합니다. 작업이 거부되면 그래프가 해당 단계를 실행하지 못하도록 방지하고 잠재적으로 대체 작업을 수행할 수 있습니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt">interrupt</a> | <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command">Command</a></i></sup>

```python
from typing import Literal
from langgraph.types import interrupt, Command

def human_approval(state: State) -> Command[Literal["some_node", "another_node"]]:
    is_approved = interrupt(
        {
            "question": "Is this correct?",
            # 사람이 검토하고 승인해야 하는
            # 출력을 표시합니다.
            "llm_output": state["llm_output"]
        }
    )

    if is_approved:
        return Command(goto="some_node")
    else:
        return Command(goto="another_node")

# 적절한 위치에 노드를 그래프에 추가하고
# 관련 노드에 연결합니다.
graph_builder.add_node("human_approval", human_approval)
graph = graph_builder.compile(checkpointer=checkpointer)

# 그래프를 실행하여 인터럽트에 도달하면 그래프가 일시 중지됩니다.
# 승인 또는 거부로 재개합니다.
thread_config = {"configurable": {"thread_id": "some_id"}}
graph.invoke(Command(resume=True), config=thread_config)
```
확장 예제: interrupt를 사용한 승인 또는 거부
```python
from typing import Literal, TypedDict
import uuid

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

# 공유 그래프 상태 정의
class State(TypedDict):
    llm_output: str
    decision: str

# LLM 출력 노드 시뮬레이션
def generate_llm_output(state: State) -> State:
    return {"llm_output": "This is the generated output."}

# 사람 승인 노드
def human_approval(state: State) -> Command[Literal["approved_path", "rejected_path"]]:
    decision = interrupt({
        "question": "Do you approve the following output?",
        "llm_output": state["llm_output"]
    })

    if decision == "approve":
        return Command(goto="approved_path", update={"decision": "approved"})
    else:
        return Command(goto="rejected_path", update={"decision": "rejected"})

# 승인 후 다음 단계
def approved_node(state: State) -> State:
    print("✅ Approved path taken.")
    return state

# 거부 후 대체 경로
def rejected_node(state: State) -> State:
    print("❌ Rejected path taken.")
    return state

# 그래프 구축
builder = StateGraph(State)
builder.add_node("generate_llm_output", generate_llm_output)
builder.add_node("human_approval", human_approval)
builder.add_node("approved_path", approved_node)
builder.add_node("rejected_path", rejected_node)

builder.set_entry_point("generate_llm_output")
builder.add_edge("generate_llm_output", "human_approval")
builder.add_edge("approved_path", END)
builder.add_edge("rejected_path", END)

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 인터럽트까지 실행
config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({}, config=config)
print(result["__interrupt__"])
# 출력:
# Interrupt(value={'question': 'Do you approve the following output?', 'llm_output': 'This is the generated output.'}, ...)

# 사람 입력으로 재개 시뮬레이션
# 거부를 테스트하려면 resume="approve"를 resume="reject"로 변경
final_result = graph.invoke(Command(resume="approve"), config=config)
print(final_result)
```

### 상태 검토 및 편집

![image](https://langchain-ai.github.io/langgraph/concepts/img/human_in_the_loop/edit-graph-state-simple.png)

사람이 그래프의 상태를 검토하고 편집할 수 있습니다. 이는 실수를 수정하거나 추가 정보로 상태를 업데이트하는 데 유용합니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt">interrupt</a></i></sup>

```python
from langgraph.types import interrupt

def human_editing(state: State):
    ...
    result = interrupt(
        # 클라이언트에 표시할 인터럽트 정보.
        # JSON 직렬화 가능한 모든 값이 될 수 있습니다.
        {
            "task": "Review the output from the LLM and make any necessary edits.",
            "llm_generated_summary": state["llm_generated_summary"]
        }
    )

    # 편집된 텍스트로 상태 업데이트
    return {
        "llm_generated_summary": result["edited_text"]
    }

# 적절한 위치에 노드를 그래프에 추가하고
# 관련 노드에 연결합니다.
graph_builder.add_node("human_editing", human_editing)
graph = graph_builder.compile(checkpointer=checkpointer)

...

# 그래프를 실행하여 인터럽트에 도달하면 그래프가 일시 중지됩니다.
# 편집된 텍스트로 재개합니다.
thread_config = {"configurable": {"thread_id": "some_id"}}
graph.invoke(
    Command(resume={"edited_text": "The edited text"}),
    config=thread_config
)
```
확장 예제: interrupt를 사용한 상태 편집
```python
from typing import TypedDict
import uuid

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

# 그래프 상태 정의
class State(TypedDict):
    summary: str

# LLM 요약 생성 시뮬레이션
def generate_summary(state: State) -> State:
    return {
        "summary": "The cat sat on the mat and looked at the stars."
    }

# 사람 편집 노드
def human_review_edit(state: State) -> State:
    result = interrupt({
        "task": "Please review and edit the generated summary if necessary.",
        "generated_summary": state["summary"]
    })
    return {
        "summary": result["edited_summary"]
    }

# 편집된 요약의 다운스트림 사용 시뮬레이션
def downstream_use(state: State) -> State:
    print(f"✅ Using edited summary: {state['summary']}")
    return state

# 그래프 구축
builder = StateGraph(State)
builder.add_node("generate_summary", generate_summary)
builder.add_node("human_review_edit", human_review_edit)
builder.add_node("downstream_use", downstream_use)

builder.set_entry_point("generate_summary")
builder.add_edge("generate_summary", "human_review_edit")
builder.add_edge("human_review_edit", "downstream_use")
builder.add_edge("downstream_use", END)

# 인터럽트 지원을 위한 인메모리 체크포인팅 설정
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 인터럽트에 도달할 때까지 그래프 호출
config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({}, config=config)

# 인터럽트 페이로드 출력
print(result["__interrupt__"])
# 예제 출력:
# > [
# >     Interrupt(
# >         value={
# >             'task': 'Please review and edit the generated summary if necessary.',
# >             'generated_summary': 'The cat sat on the mat and looked at the stars.'
# >         },
# >         id='...'
# >     )
# > ]

# 사람이 편집한 입력으로 그래프 재개
edited_summary = "The cat lay on the rug, gazing peacefully at the night sky."
resumed_result = graph.invoke(
    Command(resume={"edited_summary": edited_summary}),
    config=config
)
print(resumed_result)
```

### 도구 호출 검토

![image](https://langchain-ai.github.io/langgraph/concepts/img/human_in_the_loop/tool-call-review.png)

사람이 LLM의 출력을 진행하기 전에 검토하고 편집할 수 있습니다. 이는 LLM이 요청한 도구 호출이 민감하거나 사람의 감독이 필요한 애플리케이션에서 특히 중요합니다.

도구에 사람 승인 단계를 추가하려면:

1. 도구 내에서 `interrupt()`를 사용하여 실행을 일시 중지합니다.
2. 사람 입력을 기반으로 계속하려면 `Command`로 재개합니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.InMemorySaver">InMemorySaver</a> | <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt">interrupt</a> | <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt
from langgraph.prebuilt import create_react_agent

# 사람의 검토/승인이 필요한 민감한 도구의 예
def book_hotel(hotel_name: str):
    """호텔 예약"""
    response = interrupt(
        f"Trying to call \`book_hotel\` with args {{'hotel_name': {hotel_name}}}. "
        "Please approve or suggest edits."
    )
    if response["type"] == "accept":
        pass
    elif response["type"] == "edit":
        hotel_name = response["args"]["hotel_name"]
    else:
        raise ValueError(f"Unknown response type: {response['type']}")
    return f"Successfully booked a stay at {hotel_name}."

checkpointer = InMemorySaver()  # 인메모리 체크포인터 생성

agent = create_react_agent(
    model="anthropic:claude-3-5-sonnet-latest",
    tools=[book_hotel],
    checkpointer=checkpointer,  # 체크포인터 전달
)
```

스레드 ID를 지정하기 위해 `config` 객체를 전달하여 `stream()` 메서드로 에이전트를 실행합니다. 이를 통해 에이전트가 향후 호출에서 동일한 대화를 재개할 수 있습니다.

```python
config = {
   "configurable": {
      "thread_id": "1"
   }
}

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "book a stay at McKittrick hotel"}]},
    config
):
    print(chunk)
    print("\n")
```

> 에이전트가 `interrupt()` 호출에 도달할 때까지 실행되고, 그 지점에서 일시 중지되어 사람의 입력을 기다리는 것을 볼 수 있습니다.

사람 입력을 기반으로 계속하려면 `Command`로 에이전트를 재개합니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command">Command</a></i></sup>

```python
from langgraph.types import Command

for chunk in agent.stream(
    Command(resume={"type": "accept"}),  # 승인으로 재개
    # Command(resume={"type": "edit", "args": {"hotel_name": "McKittrick Hotel"}}),  # 또는 편집으로 재개
    config
):
    print(chunk)
    print("\n")
```

### 모든 도구에 인터럽트 추가하기

*모든* 도구에 인터럽트를 추가하는 래퍼를 만들 수 있습니다. 아래 예제는 [Agent Inbox UI](https://github.com/langchain-ai/agent-inbox) 및 [Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui)와 호환되는 참조 구현을 제공합니다.

```python
# 모든 도구에 휴먼-인-더-루프를 추가하는 래퍼
from typing import Callable
from langchain_core.tools import BaseTool, tool as create_tool
from langchain_core.runnables import RunnableConfig
from langgraph.types import interrupt
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt

def add_human_in_the_loop(
    tool: Callable | BaseTool,
    *,
    interrupt_config: HumanInterruptConfig = None,
) -> BaseTool:
    """휴먼-인-더-루프 검토를 지원하도록 도구를 래핑합니다."""
    if not isinstance(tool, BaseTool):
        tool = create_tool(tool)

    if interrupt_config is None:
        interrupt_config = {
            "allow_accept": True,
            "allow_edit": True,
            "allow_respond": True,
        }

    @create_tool(
        tool.name,
        description=tool.description,
        args_schema=tool.args_schema
    )
    def call_tool_with_interrupt(config: RunnableConfig, **tool_input):
        request: HumanInterrupt = {
            "action_request": {
                "action": tool.name,
                "args": tool_input
            },
            "config": interrupt_config,
            "description": "Please review the tool call"
        }
        response = interrupt([request])[0]
        # 도구 호출 승인
        if response["type"] == "accept":
            tool_response = tool.invoke(tool_input, config)
        # 도구 호출 인자 업데이트
        elif response["type"] == "edit":
            tool_input = response["args"]["args"]
            tool_response = tool.invoke(tool_input, config)
        # 사용자 피드백으로 LLM에 응답
        elif response["type"] == "response":
            user_feedback = response["args"]
            tool_response = user_feedback
        else:
            raise ValueError(f"Unsupported interrupt response type: {response['type']}")

        return tool_response

    return call_tool_with_interrupt
```

도구 *내부*에 추가하지 않고도 래퍼를 사용하여 모든 도구에 `interrupt()`를 추가할 수 있습니다:

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/checkpoints/#langgraph.checkpoint.memory.InMemorySaver">InMemorySaver</a> | <a href="https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.chat_agent_executor.create_react_agent">create_react_agent</a></i></sup>

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent

checkpointer = InMemorySaver()

def book_hotel(hotel_name: str):
   """호텔 예약"""
   return f"Successfully booked a stay at {hotel_name}."

agent = create_react_agent(
    model="anthropic:claude-3-5-sonnet-latest",
    tools=[
        add_human_in_the_loop(book_hotel),  # 래퍼로 도구를 감쌉니다
    ],
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "1"}}

# 에이전트 실행
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "book a stay at McKittrick hotel"}]},
    config
):
    print(chunk)
    print("\n")
```

> 에이전트가 `interrupt()` 호출에 도달할 때까지 실행되고, 그 지점에서 일시 중지되어 사람의 입력을 기다리는 것을 볼 수 있습니다.

사람 입력을 기반으로 계속하려면 `Command`로 에이전트를 재개합니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.Command">Command</a></i></sup>

```python
from langgraph.types import Command

for chunk in agent.stream(
    Command(resume=[{"type": "accept"}]),  # 승인으로 재개
    # Command(resume=[{"type": "edit", "args": {"args": {"hotel_name": "McKittrick Hotel"}}}]),  # 또는 편집으로 재개
    config
):
    print(chunk)
    print("\n")
```

### 사람 입력 유효성 검사

클라이언트 측이 아닌 그래프 자체 내에서 사람이 제공한 입력의 유효성을 검사해야 하는 경우, 단일 노드 내에서 여러 인터럽트 호출을 사용하여 이를 수행할 수 있습니다.

<sup><i>API Reference: <a href="https://langchain-ai.github.io/langgraph/reference/types/#langgraph.types.interrupt">interrupt</a></i></sup>

```python
from langgraph.types import interrupt

def human_node(state: State):
    """유효성 검사가 포함된 사람 노드."""
    question = "What is your age?"

    while True:
        answer = interrupt(question)

        # 답변 유효성 검사, 답변이 유효하지 않으면 다시 입력 요청.
        if not isinstance(answer, int) or answer < 0:
            question = f"'{answer} is not a valid age. What is your age?"
            answer = None
            continue
        else:
            # 답변이 유효하면 계속 진행할 수 있습니다.
            break

    print(f"The human in the loop is {answer} years old.")
    return {
        "age": answer
    }
```
확장 예제: 사용자 입력 유효성 검사
```python
from typing import TypedDict
import uuid

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

# 그래프 상태 정의
class State(TypedDict):
    age: int

# 사람 입력을 요청하고 유효성을 검사하는 노드
def get_valid_age(state: State) -> State:
    prompt = "Please enter your age (must be a non-negative integer)."

    while True:
        user_input = interrupt(prompt)

        # 입력 유효성 검사
        try:
            age = int(user_input)
            if age < 0:
                raise ValueError("Age must be non-negative.")
            break  # 유효한 입력 수신
        except (ValueError, TypeError):
            prompt = f"'{user_input}' is not valid. Please enter a non-negative integer for age."

    return {"age": age}

# 유효한 입력을 사용하는 노드
def report_age(state: State) -> State:
    print(f"✅ Human is {state['age']} years old.")
    return state

# 그래프 구축
builder = StateGraph(State)
builder.add_node("get_valid_age", get_valid_age)
builder.add_node("report_age", report_age)

builder.set_entry_point("get_valid_age")
builder.add_edge("get_valid_age", "report_age")
builder.add_edge("report_age", END)

# 메모리 체크포인터로 그래프 생성
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 첫 번째 인터럽트까지 그래프 실행
config = {"configurable": {"thread_id": uuid.uuid4()}}
result = graph.invoke({}, config=config)
print(result["__interrupt__"])  # 첫 번째 프롬프트: "Please enter your age..."

# 유효하지 않은 입력 시뮬레이션 (예: 정수 대신 문자열)
result = graph.invoke(Command(resume="not a number"), config=config)
print(result["__interrupt__"])  # 유효성 검사 메시지가 포함된 후속 프롬프트

# 두 번째 유효하지 않은 입력 시뮬레이션 (예: 음수)
result = graph.invoke(Command(resume="-10"), config=config)
print(result["__interrupt__"])  # 또 다른 재시도

# 유효한 입력 제공
final_result = graph.invoke(Command(resume="25"), config=config)
print(final_result)  # 유효한 나이가 포함되어야 함
```

## 인터럽트로 디버깅하기

그래프를 디버그하고 테스트하려면 [정적 인터럽트](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/#key-capabilities)(정적 중단점이라고도 함)를 사용하여 그래프 실행을 한 번에 한 노드씩 단계별로 진행하거나 특정 노드에서 그래프 실행을 일시 중지합니다. 정적 인터럽트는 노드가 실행되기 전 또는 후의 정의된 지점에서 트리거됩니다. 컴파일 시간 또는 런타임에 `interrupt_before` 및 `interrupt_after`를 지정하여 정적 인터럽트를 설정할 수 있습니다.

> [!Warning]
> 정적 인터럽트는 휴먼-인-더-루프 워크플로우에 권장되지 **않습니다**. 대신 [동적 인터럽트](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#pause-using-interrupt)를 사용하세요.

1. `graph.invoke`는 `interrupt_before` 및 `interrupt_after` 매개변수와 함께 호출됩니다. 이것은 런타임 구성이며 모든 호출에 대해 변경할 수 있습니다.
2. `interrupt_before`는 노드가 실행되기 전에 실행을 일시 중지해야 하는 노드를 지정합니다.
3. `interrupt_after`는 노드가 실행된 후에 실행을 일시 중지해야 하는 노드를 지정합니다.
4. 그래프는 첫 번째 중단점에 도달할 때까지 실행됩니다.
5. 입력에 `None`을 전달하여 그래프를 재개합니다. 이렇게 하면 다음 중단점에 도달할 때까지 그래프가 실행됩니다.

> [!Note]
> **서브그래프**의 경우 런타임에 정적 중단점을 설정할 수 없습니다. 서브그래프가 있는 경우 컴파일 시간에 중단점을 설정해야 합니다.

Setting static breakpoints
```python
from IPython.display import Image, display
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    input: str

def step_1(state):
    print("---Step 1---")
    pass

def step_2(state):
    print("---Step 2---")
    pass

def step_3(state):
    print("---Step 3---")
    pass

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

# Set up a checkpointer
checkpointer = InMemorySaver() # (1)!

graph = builder.compile(
    checkpointer=checkpointer, # (2)!
    interrupt_before=["step_3"] # (3)!
)

# View
display(Image(graph.get_graph().draw_mermaid_png()))

# Input
initial_input = {"input": "hello world"}

# Thread
thread = {"configurable": {"thread_id": "1"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    print(event)

# This will run until the breakpoint
# You can get the state of the graph at this point
print(graph.get_state(config))

# You can continue the graph execution by passing in \`None\` for the input
for event in graph.stream(None, thread, stream_mode="values"):
    print(event)
```

### Use static interrupts in LangGraph Studio

You can use [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/) to debug your graph. You can set static breakpoints in the UI and then run the graph. You can also use the UI to inspect the graph state at any point in the execution.

![image](https://langchain-ai.github.io/langgraph/concepts/img/human_in_the_loop/static-interrupt.png)

LangGraph Studio is free with [locally deployed applications](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/) using `langgraph dev`.

## Debug with interrupts

To debug and test a graph, use [static interrupts](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/#key-capabilities) (also known as static breakpoints) to step through the graph execution one node at a time or to pause the graph execution at specific nodes. Static interrupts are triggered at defined points either before or after a node executes. You can set static interrupts by specifying `interrupt_before` and `interrupt_after` at compile time or run time.

> [!Warning]
> Static interrupts are **not** recommended for human-in-the-loop workflows. Use [dynamic interrupts](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#pause-using-interrupt) instead.

1. `graph.invoke` is called with the `interrupt_before` and `interrupt_after` parameters. This is a run-time configuration and can be changed for every invocation.
2. `interrupt_before` specifies the nodes where execution should pause before the node is executed.
3. `interrupt_after` specifies the nodes where execution should pause after the node is executed.
4. The graph is run until the first breakpoint is hit.
5. The graph is resumed by passing in `None` for the input. This will run the graph until the next breakpoint is hit.

> [!Note]
> You cannot set static breakpoints at runtime for **sub-graphs**. If you have a sub-graph, you must set the breakpoints at compilation time.

Setting static breakpoints
```python
from IPython.display import Image, display
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    input: str

def step_1(state):
    print("---Step 1---")
    pass

def step_2(state):
    print("---Step 2---")
    pass

def step_3(state):
    print("---Step 3---")
    pass

builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

# Set up a checkpointer
checkpointer = InMemorySaver() # (1)!

graph = builder.compile(
    checkpointer=checkpointer, # (2)!
    interrupt_before=["step_3"] # (3)!
)

# View
display(Image(graph.get_graph().draw_mermaid_png()))

# Input
initial_input = {"input": "hello world"}

# Thread
thread = {"configurable": {"thread_id": "1"}}

# Run the graph until the first interruption
for event in graph.stream(initial_input, thread, stream_mode="values"):
    print(event)

# This will run until the breakpoint
# You can get the state of the graph at this point
print(graph.get_state(config))

# You can continue the graph execution by passing in \`None\` for the input
for event in graph.stream(None, thread, stream_mode="values"):
    print(event)
```

### Use static interrupts in LangGraph Studio

You can use [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/) to debug your graph. You can set static breakpoints in the UI and then run the graph. You can also use the UI to inspect the graph state at any point in the execution.

![image](https://langchain-ai.github.io/langgraph/concepts/img/human_in_the_loop/static-interrupt.png)

LangGraph Studio is free with [locally deployed applications](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/) using `langgraph dev`.

## 고려사항

휴먼-인-더-루프를 사용할 때 유의해야 할 몇 가지 고려사항이 있습니다.

### 부작용이 있는 코드와 함께 사용하기

API 호출과 같이 부작용이 있는 코드는 `interrupt` 뒤에 배치하거나 별도의 노드에 배치하여 중복을 방지합니다. 노드가 재개될 때마다 이러한 코드가 다시 트리거되기 때문입니다.

```python
from langgraph.types import interrupt

def human_node(state: State):
    """유효성 검사가 포함된 사람 노드."""

    answer = interrupt(question)

    api_call(answer) # 인터럽트 뒤에 있으므로 OK
```

```python
from langgraph.types import interrupt

def human_node(state: State):
    """유효성 검사가 포함된 사람 노드."""

    answer = interrupt(question)

    return {
        "answer": answer
    }

def api_call_node(state: State):
    api_call(...) # 별도의 노드에 있으므로 OK
```

### 함수로 호출되는 서브그래프와 함께 사용하기

서브그래프를 함수로 호출할 때, 부모 그래프는 `interrupt`가 트리거된 서브그래프가 호출된 **노드의 시작 부분**부터 실행을 재개합니다. 마찬가지로 **서브그래프**는 `interrupt()` 함수가 호출된 **노드의 시작 부분**부터 재개됩니다.

```python
def node_in_parent_graph(state: State):
    some_code()  # <-- 서브그래프가 재개될 때 다시 실행됩니다.
    # 함수로 서브그래프를 호출합니다.
    # 서브그래프에 `interrupt` 호출이 포함되어 있습니다.
    subgraph_result = subgraph.invoke(some_input)
    ...
```
확장 예제: 부모 그래프와 서브그래프 실행 흐름

3개의 노드가 있는 부모 그래프가 있다고 가정합니다:

**부모 그래프**: `node_1` → `node_2` (서브그래프 호출) → `node_3`

그리고 서브그래프에는 3개의 노드가 있으며, 두 번째 노드에 `interrupt`가 포함되어 있습니다:

**서브그래프**: `sub_node_1` → `sub_node_2` (`interrupt`) → `sub_node_3`

그래프를 재개할 때 실행은 다음과 같이 진행됩니다:

1. 부모 그래프에서 **`node_1` 건너뛰기** (이미 실행됨, 그래프 상태가 스냅샷에 저장됨).
2. 부모 그래프에서 **`node_2`를 처음부터 다시 실행**.
3. 서브그래프에서 **`sub_node_1` 건너뛰기** (이미 실행됨, 그래프 상태가 스냅샷에 저장됨).
4. 서브그래프에서 **`sub_node_2`를 처음부터 다시 실행**.
5. `sub_node_3` 및 후속 노드 계속 진행.

다음은 인터럽트와 함께 서브그래프가 작동하는 방식을 이해하는 데 사용할 수 있는 간략한 예제 코드입니다. 각 노드가 입력된 횟수를 세고 출력합니다.

```python
import uuid
from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.constants import START
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    """그래프 상태."""
    state_counter: int

counter_node_in_subgraph = 0

def node_in_subgraph(state: State):
    """서브그래프의 노드."""
    global counter_node_in_subgraph
    counter_node_in_subgraph += 1  # 이 코드는 다시 실행되지 **않습니다**!
    print(f"Entered \`node_in_subgraph\` a total of {counter_node_in_subgraph} times")

counter_human_node = 0

def human_node(state: State):
    global counter_human_node
    counter_human_node += 1 # 이 코드는 다시 실행됩니다!
    print(f"Entered human_node in sub-graph a total of {counter_human_node} times")
    answer = interrupt("what is your name?")
    print(f"Got an answer of {answer}")

checkpointer = InMemorySaver()

subgraph_builder = StateGraph(State)
subgraph_builder.add_node("some_node", node_in_subgraph)
subgraph_builder.add_node("human_node", human_node)
subgraph_builder.add_edge(START, "some_node")
subgraph_builder.add_edge("some_node", "human_node")
subgraph = subgraph_builder.compile(checkpointer=checkpointer)

counter_parent_node = 0

def parent_node(state: State):
    """이 부모 노드는 서브그래프를 호출합니다."""
    global counter_parent_node

    counter_parent_node += 1 # 이 코드는 재개 시 다시 실행됩니다!
    print(f"Entered \`parent_node\` a total of {counter_parent_node} times")

    # 동일한 키의 서브그래프 업데이트가 부모 그래프와
    # 충돌하지 않는다는 것을 보여주기 위해
    # 그래프 상태의 상태 카운터를 의도적으로 증가시킵니다
    subgraph_state = subgraph.invoke(state)
    return subgraph_state

builder = StateGraph(State)
builder.add_node("parent_node", parent_node)
builder.add_edge(START, "parent_node")

# 인터럽트가 작동하려면 체크포인터가 활성화되어야 합니다!
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {
    "configurable": {
      "thread_id": uuid.uuid4(),
    }
}

for chunk in graph.stream({"state_counter": 1}, config):
    print(chunk)

print('--- Resuming ---')

for chunk in graph.stream(Command(resume="35"), config):
    print(chunk)
```

다음과 같이 출력됩니다

```js
Entered \`parent_node\` a total of 1 times
Entered \`node_in_subgraph\` a total of 1 times
Entered human_node in sub-graph a total of 1 times
{'__interrupt__': (Interrupt(value='what is your name?', id='...'),)}
--- Resuming ---
Entered \`parent_node\` a total of 2 times
Entered human_node in sub-graph a total of 2 times
Got an answer of 35
{'parent_node': {'state_counter': 1}}
```

### 단일 노드에서 여러 인터럽트 사용하기

**단일** 노드 내에서 여러 인터럽트를 사용하는 것은 [사람 입력 유효성 검사](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/#validate-human-input)와 같은 패턴에 유용할 수 있습니다. 그러나 동일한 노드에서 여러 인터럽트를 사용하면 신중하게 처리하지 않으면 예기치 않은 동작이 발생할 수 있습니다.

노드에 여러 인터럽트 호출이 포함되어 있으면 LangGraph는 노드를 실행하는 작업에 특정한 재개 값 목록을 유지합니다. 실행이 재개될 때마다 노드의 시작 부분에서 시작됩니다. 각 인터럽트가 발생할 때마다 LangGraph는 작업의 재개 목록에 일치하는 값이 있는지 확인합니다. 일치는 **엄격하게 인덱스 기반**이므로 노드 내 인터럽트 호출의 순서가 중요합니다.

문제를 피하려면 실행 사이에 노드 구조를 동적으로 변경하지 마세요. 여기에는 인터럽트 호출을 추가, 제거 또는 재정렬하는 것이 포함되며, 이러한 변경은 인덱스 불일치를 초래할 수 있습니다. 이러한 문제는 `Command(resume=..., update=SOME_STATE_MUTATION)`를 통해 상태를 변경하거나 전역 변수에 의존하여 노드 구조를 동적으로 수정하는 것과 같은 비정형적인 패턴에서 자주 발생합니다.

확장 예제: 비결정성을 도입하는 잘못된 코드
```python
import uuid
from typing import TypedDict, Optional

from langgraph.graph import StateGraph
from langgraph.constants import START
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    """그래프 상태."""

    age: Optional[str]
    name: Optional[str]

def human_node(state: State):
    if not state.get('name'):
        name = interrupt("what is your name?")
    else:
        name = "N/A"

    if not state.get('age'):
        age = interrupt("what is your age?")
    else:
        age = "N/A"

    print(f"Name: {name}. Age: {age}")

    return {
        "age": age,
        "name": name,
    }

builder = StateGraph(State)
builder.add_node("human_node", human_node)
builder.add_edge(START, "human_node")

# 인터럽트가 작동하려면 체크포인터가 활성화되어야 합니다!
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {
    "configurable": {
        "thread_id": uuid.uuid4(),
    }
}

for chunk in graph.stream({"age": None, "name": None}, config):
    print(chunk)

for chunk in graph.stream(Command(resume="John", update={"name": "foo"}), config):
    print(chunk)
```
```python
{'__interrupt__': (Interrupt(value='what is your name?', id='...'),)}
Name: N/A. Age: John
{'human_node': {'age': 'John', 'name': 'N/A'}}
```