---
created: 2025-10-18 00:00:00
updated: 2025-10-18 00:21:40
---

## 개요

LangGraph의 `Command` 객체는 그래프 실행 중에 **상태 업데이트**와 **제어 흐름**을 제어하는 강력한 프리미티브입니다. `Command`는 크게 두 가지 주요 사용 패턴을 가지고 있습니다:

1. **`Command(update={...})`**: 상태를 업데이트하고 제어 흐름을 지정
2. **`Command(resume=...)`**: 중단된 그래프 실행을 재개

## Command(update={...})

### 용도

노드 내에서 **상태를 업데이트**하면서 동시에 **다음 노드로의 이동**을 지정할 때 사용합니다.

### 주요 특징

- **상태 업데이트와 제어 흐름을 동시에 처리**
- 조건부 로직과 함께 사용 가능
- 멀티 에이전트 핸드오프 패턴에서 주로 활용
- 노드 실행의 일반적인 흐름 중에 사용

### 사용 예시

#### 1. 기본 상태 업데이트와 라우팅

```python
from langgraph.types import Command
from typing import Literal

def my_node(state: State) -> Command[Literal["my_other_node"]]:
    return Command(
        # 상태 업데이트
        update={"foo": "bar"},
        # 제어 흐름 - 다음 노드 지정
        goto="my_other_node"
    )
```

#### 2. 조건부 로직과 함께 사용

```python
def my_node(state: State) -> Command[Literal["node_a", "node_b"]]:
    if state["foo"] == "bar":
        return Command(
            update={"result": "condition met"},
            goto="node_a"
        )
    else:
        return Command(
            update={"result": "condition not met"},
            goto="node_b"
        )
```

#### 3. 도구 내부에서 상태 업데이트

```python
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, InjectedToolCallId

@tool
def update_user_name(
    new_name: str,
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """사용자 이름을 단기 메모리에 업데이트합니다."""
    return Command(update={
        "user_name": new_name,
        "messages": [
            ToolMessage(
                f"사용자 이름을 {new_name}으로 업데이트했습니다.",
                tool_call_id=tool_call_id
            )
        ]
    })
```

#### 4. 부모 그래프로 이동하기 (멀티 에이전트 핸드오프)

서브그래프 내부에서 부모 그래프의 다른 노드로 이동할 때:

```python
def create_handoff_tool(*, agent_name: str, description: str | None = None):
    """에이전트 간 핸드오프를 위한 도구 생성"""

    @tool
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"{agent_name}으로 성공적으로 이동했습니다.",
            "tool_call_id": tool_call_id,
        }
        return Command(
            goto=agent_name,
            update={"messages": state["messages"] + [tool_message]},
            graph=Command.PARENT,  # 부모 그래프에서 이동
        )

    return handoff_tool
```

### 주요 사용 시나리오

- ✅ 노드 실행 중 상태 변경과 다음 노드 지정을 동시에 수행
- ✅ 멀티 에이전트 시스템에서 에이전트 간 핸드오프
- ✅ 도구 실행 결과로 상태를 업데이트
- ✅ 조건부 라우팅과 상태 변경을 함께 처리

---

## Command(resume=...)

### 용도

`interrupt()`로 **일시 중단된 그래프 실행을 재개**할 때 사용합니다. 휴먼-인-더-루프(Human-in-the-Loop) 워크플로우에서 핵심적인 역할을 합니다.

### 주요 특징

- **중단 지점에서 사용자 입력을 제공하여 실행 재개**
- `interrupt()` 함수와 쌍으로 사용
- 중단된 노드는 **처음부터 다시 실행**됨
- Python의 `input()`과 유사하지만, 중단 지점이 아닌 노드 시작부터 재실행

### 사용 예시

#### 1. 기본 사용법

```python
from langgraph.types import interrupt, Command

def human_node(state: State):
    # 그래프 실행 일시 중단 및 사용자에게 정보 표시
    value = interrupt({
        "text_to_revise": state["some_text"]
    })

    # 사용자가 제공한 값으로 상태 업데이트
    return {
        "some_text": value
    }

# 그래프를 체크포인터와 함께 컴파일
graph = graph_builder.compile(checkpointer=checkpointer)

# 인터럽트에 도달할 때까지 실행
config = {"configurable": {"thread_id": "some_id"}}
result = graph.invoke({"some_text": "original text"}, config=config)

# 중단 정보 확인
print(result['__interrupt__'])
# [Interrupt(value={'text_to_revise': 'original text'}, ...)]

# 사용자 입력을 제공하여 재개
graph.invoke(Command(resume="Edited text"), config=config)
# {'some_text': 'Edited text'}
```

#### 2. 승인/거부 패턴

```python
def human_approval(state: State) -> Command[Literal["approved_path", "rejected_path"]]:
    is_approved = interrupt({
        "question": "이 출력을 승인하시겠습니까?",
        "llm_output": state["llm_output"]
    })

    if is_approved:
        return Command(goto="approved_path")
    else:
        return Command(goto="rejected_path")

# 실행 및 중단
result = graph.invoke({}, config=config)

# 승인으로 재개
graph.invoke(Command(resume=True), config=config)
```

#### 3. 상태 검토 및 편집

```python
def human_editing(state: State):
    result = interrupt({
        "task": "LLM 출력을 검토하고 필요한 수정을 해주세요.",
        "llm_generated_summary": state["llm_generated_summary"]
    })

    # 편집된 텍스트로 상태 업데이트
    return {
        "llm_generated_summary": result["edited_text"]
    }

# 편집된 텍스트로 재개
graph.invoke(
    Command(resume={"edited_text": "편집된 텍스트"}),
    config=config
)
```

#### 4. 도구 호출 검토

```python
def book_hotel(hotel_name: str):
    """호텔 예약 - 사용자 승인 필요"""
    response = interrupt(
        f"'book_hotel'을 {{'hotel_name': {hotel_name}}}로 호출하려 합니다. "
        "승인하거나 편집을 제안해주세요."
    )

    if response["type"] == "accept":
        pass
    elif response["type"] == "edit":
        hotel_name = response["args"]["hotel_name"]
    else:
        raise ValueError(f"알 수 없는 응답 타입: {response['type']}")

    return f"{hotel_name}에 성공적으로 예약했습니다."

# 승인으로 재개
agent.stream(Command(resume={"type": "accept"}), config)

# 또는 편집으로 재개
agent.stream(
    Command(resume={"type": "edit", "args": {"hotel_name": "다른 호텔"}}),
    config
)
```

#### 5. 여러 인터럽트 동시 재개

병렬로 실행되는 여러 노드가 모두 중단된 경우:

```python
# 모든 인터럽트 정보 가져오기
state = graph.get_state(config)

# 인터럽트 ID를 키로 하는 재개 값 매핑
resume_map = {
    i.id: f"edited text for {i.value['text_to_revise']}"
    for i in state.interrupts
}

# 한 번에 모든 인터럽트 재개
graph.invoke(Command(resume=resume_map), config=config)
```

#### 6. 사용자 입력 유효성 검사

```python
def human_node(state: State):
    """유효성 검사가 포함된 사용자 입력 노드"""
    question = "나이를 입력해주세요:"

    while True:
        answer = interrupt(question)

        # 답변 유효성 검사
        if not isinstance(answer, int) or answer < 0:
            question = f"'{answer}'는 유효한 나이가 아닙니다. 다시 입력해주세요:"
            continue
        else:
            break

    return {"age": answer}

# 잘못된 입력
graph.invoke(Command(resume="not a number"), config)
# 다시 인터럽트 발생

# 유효한 입력
graph.invoke(Command(resume=25), config)
# 정상 진행
```

### 주요 사용 시나리오

- ✅ 휴먼-인-더-루프 워크플로우
- ✅ 사용자 승인이 필요한 작업
- ✅ 사용자에게 상태를 보여주고 편집 받기
- ✅ 민감한 도구 호출 검토
- ✅ 사용자 입력 유효성 검사

---

## 핵심 차이점 요약

| 특징 | `Command(update={...})` | `Command(resume=...)` |
|------|------------------------|----------------------|
| **주요 용도** | 상태 업데이트 + 제어 흐름 | 중단된 실행 재개 |
| **사용 시점** | 노드 실행 중 | `interrupt()` 후 재개 시 |
| **상태 변경** | 새로운 상태 값 설정 | 중단 지점에 값 제공 |
| **실행 흐름** | 다음 노드 지정 (`goto`) | 중단된 노드를 처음부터 재실행 |
| **체크포인터 필요** | 선택적 | **필수** |
| **주요 패턴** | 멀티 에이전트 핸드오프, 조건부 라우팅 | 휴먼-인-더-루프, 승인 워크플로우 |

## 함께 사용하기

두 패턴은 함께 사용될 수도 있습니다:

```python
def approval_node(state: State) -> Command[Literal["approved", "rejected"]]:
    """승인 후 상태를 업데이트하며 다음 노드로 이동"""

    is_approved = interrupt({
        "question": "승인하시겠습니까?",
        "data": state["data"]
    })

    # resume으로 재개된 후, update와 goto로 상태 변경 및 라우팅
    if is_approved:
        return Command(
            update={"status": "approved", "timestamp": datetime.now()},
            goto="approved"
        )
    else:
        return Command(
            update={"status": "rejected", "timestamp": datetime.now()},
            goto="rejected"
        )

# 첫 실행 - 중단됨
result = graph.invoke(input_data, config)

# 재개 - update와 goto가 함께 실행됨
graph.invoke(Command(resume=True), config)
```

## 중요 고려사항

### `Command(resume=...)`를 사용할 때

1. **노드 재실행**: `interrupt()` 이후의 코드만 실행되는 것이 아니라, **노드 전체가 처음부터 다시 실행**됩니다.

2. **부작용 주의**: API 호출 같은 부작용이 있는 코드는 `interrupt()` **뒤**에 배치하거나 별도 노드로 분리해야 합니다.

```python
# ❌ 나쁜 예
def human_node(state: State):
    api_call()  # interrupt 전에 있으면 재개 시마다 다시 호출됨
    answer = interrupt(question)
    return {"answer": answer}

# ✅ 좋은 예 1: interrupt 뒤에 배치
def human_node(state: State):
    answer = interrupt(question)
    api_call(answer)  # interrupt 뒤에 있으므로 한 번만 호출
    return {"answer": answer}

# ✅ 좋은 예 2: 별도 노드로 분리
def human_node(state: State):
    answer = interrupt(question)
    return {"answer": answer}

def api_call_node(state: State):
    api_call(state["answer"])
```

3. **서브그래프와 함께 사용**: 서브그래프 내부에서 `interrupt()`가 발생하면, 서브그래프를 **호출한 부모 노드**도 처음부터 재실행됩니다.

### `Command(update={...})`를 사용할 때

1. **반환 타입 명시**: `Command`를 반환하는 노드는 타입 힌트에 가능한 목적지 노드를 명시해야 합니다.

```python
# ✅ 올바른 타입 힌트
def my_node(state: State) -> Command[Literal["node_a", "node_b"]]:
    return Command(update={...}, goto="node_a")

# ❌ 타입 힌트 없음 - 그래프 렌더링 실패 가능
def my_node(state: State):
    return Command(update={...}, goto="node_a")
```

2. **Conditional Edges vs Command**: 상태 업데이트가 필요 없으면 `add_conditional_edges`를 사용하고, 상태 변경과 라우팅을 동시에 하려면 `Command`를 사용하세요.

## 참고 문서

- [LangGraph 휴먼-인-더-루프 가이드](../휴먼-인-더-루프/휴먼-인-더-루프%20사용하기.md)
- [Graph API 개념](./Graph%20API%20개념.md)
- [멀티 에이전트 시스템 구축](../멀티%20에이전트/멀티%20에이전트%20시스템%20구축%20가이드.md)
