---
created: 2025-10-18 00:11:58
updated: 2025-10-18 00:21:27
---
## 개요

LangGraph에서 `Command`와 `Send`는 그래프 내에서 제어 흐름(control flow)을 관리하는 핵심 메커니즘입니다. 두 개념 모두 동적 라우팅을 가능하게 하지만, 사용 목적과 기능 범위에서 차이가 있습니다.

---

## Command란?

### 정의
`Command`는 LangGraph 0.6 버전에서 도입된 객체로, **노드가 상태 업데이트와 제어 흐름을 동시에 처리**할 수 있게 해주는 강력한 도구입니다.

### 주요 특징
- **Edgeless 그래프**: 미리 정의된 엣지 없이도 노드가 다음 실행할 노드를 동적으로 결정
- **상태 업데이트 + 라우팅**: 하나의 반환값으로 상태 수정과 다음 노드 지정을 동시에 처리
- **멀티 에이전트 아키텍처**: 에이전트 간 핸드오프(handoff)를 간편하게 구현
- **계층적 그래프 지원**: 부모 그래프로의 라우팅 지원 (`Command.PARENT`)

### 기본 구조

```python
from langgraph.types import Command
from typing import Literal

def my_node(state: State) -> Command[Literal["next_node", "another_node"]]:
    return Command(
        # 상태 업데이트
        update={"foo": "bar"},
        # 다음 노드 지정
        goto="next_node"
    )
```

### 주요 매개변수
- `update`: 그래프 상태를 업데이트할 데이터 (딕셔너리)
- `goto`: 다음에 실행할 노드 이름 (문자열 또는 Send 객체 리스트)
- `resume`: Human-in-the-loop에서 중단된 실행을 재개할 때 사용
- `graph`: 부모 그래프로 라우팅할 때 사용 (`Command.PARENT`)

---

## Send란?

### 정의
`Send`는 **특정 노드에 특정 데이터를 전달**하는 메시징 메커니즘입니다. 주로 동적 병렬 실행에 사용됩니다.

### 주요 특징
- **동적 Fan-out**: 실행 시점에 병렬로 처리할 작업 개수를 동적으로 결정
- **타겟 지정**: 특정 노드에 특정 입력값을 전달
- **조건부 엣지와 함께 사용**: `add_conditional_edges`와 함께 사용하여 동적 라우팅 구현

### 기본 구조

```python
from langgraph.types import Send

def continue_to_jokes(state: OverallState):
    # 각 주제마다 별도의 joke 노드를 병렬로 실행
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

# 그래프 구성
builder.add_conditional_edges("node_a", continue_to_jokes)
```

### Send 객체 생성

```python
Send(
    node="target_node_name",  # 타겟 노드 이름
    arg={"key": "value"}      # 전달할 데이터
)
```

---

## Command vs Send: 핵심 차이점

| 구분 | Command | Send |
|------|---------|------|
| **주요 목적** | 상태 업데이트 + 제어 흐름 통합 관리 | 특정 노드로 특정 데이터 전달 |
| **반환 위치** | 노드 함수에서 직접 반환 | 조건부 엣지 함수에서 반환하거나 Command의 goto에 포함 |
| **상태 업데이트** | `update` 매개변수로 직접 지원 | 전달하는 데이터(`arg`)만 지정 |
| **사용 시점** | 단일/다중 노드로의 라우팅 + 상태 수정 | 동적 병렬 실행 (fan-out) |
| **엣지 정의** | 불필요 (edgeless 가능) | 조건부 엣지와 함께 사용 |
| **부모 그래프 라우팅** | `graph=Command.PARENT` 지원 | 미지원 |

---

## 관계: Command는 Send의 상위집합

LangGraph 메인테이너의 설명에 따르면:

> **Command can contain multiple sends + other logic (e.g., goto for normal routing). It's more of a superset.**

즉, `Command`는 `Send`의 기능을 포함하면서 추가적인 기능을 제공합니다.

### Command에서 Send 사용하기

```python
def my_node(state: State) -> Command:
    return Command(
        # 여러 개의 Send를 포함한 병렬 실행 (fan-out)
        goto=[Send("process", {"val": i}) for i in range(10)],
        # 동시에 상태도 업데이트
        update={"status": "processing"}
    )
```

---

## 사용 시나리오별 가이드

### 1. 단순 조건부 라우팅

**기존 방식 (Conditional Edge)**
```python
def router(state):
    if state["condition"]:
        return "node_a"
    return "node_b"

builder.add_conditional_edges("start", router, {"node_a": "node_a", "node_b": "node_b"})
```

**Command 방식**
```python
def start_node(state) -> Command[Literal["node_a", "node_b"]]:
    if state["condition"]:
        return Command(update={"status": "path_a"}, goto="node_a")
    return Command(update={"status": "path_b"}, goto="node_b")

# 엣지 정의 불필요
```

### 2. 에이전트 핸드오프 (Multi-Agent)

```python
from langchain_core.tools import tool

@tool
def transfer_to_specialist():
    """전문 에이전트로 작업 이관"""
    return Command(
        goto="specialist_agent",
        update={"messages": [{"role": "user", "content": "이관된 작업입니다"}]},
        graph=Command.PARENT  # 부모 그래프의 노드로 이동
    )
```

### 3. 동적 병렬 실행 (Map-Reduce 패턴)

```python
def map_node(state):
    """여러 작업을 병렬로 실행"""
    items = state["items_to_process"]
    # Send를 사용하여 각 아이템을 병렬 처리
    return [Send("worker", {"item": item}) for item in items]

builder.add_conditional_edges("map_node", map_node)
```

**Command로 Send 포함**
```python
def map_node(state) -> Command:
    """Command로 병렬 실행 + 상태 업데이트"""
    items = state["items_to_process"]
    return Command(
        goto=[Send("worker", {"item": item}) for item in items],
        update={"processing_started": True}
    )
```

### 4. Human-in-the-Loop (HIL)

```python
from langgraph.types import interrupt

def review_node(state):
    """사람의 검토가 필요한 노드"""
    # 실행 중단 및 사람 입력 대기
    human_input = interrupt({"question": "이 결과를 승인하시겠습니까?"})
    return {"approved": human_input}

# 재개 시
graph.invoke(Command(resume={"approved": True}), config)
```

---

## 언제 무엇을 사용해야 할까?

### Command를 사용하는 경우
✅ 노드에서 **상태 업데이트와 라우팅을 동시에** 처리해야 할 때
✅ **멀티 에이전트 시스템**에서 에이전트 간 핸드오프 구현
✅ 부모 그래프로 **계층적 라우팅**이 필요할 때
✅ **Human-in-the-loop** 워크플로에서 중단/재개 처리
✅ 기존 조건부 엣지 로직을 **단순화**하고 싶을 때

### Send를 사용하는 경우
✅ **동적 병렬 실행**(fan-out)이 주요 목적일 때
✅ 실행 시점에 **병렬 작업 개수가 결정**되는 경우
✅ 각 병렬 작업에 **서로 다른 입력값**을 전달해야 할 때
✅ Map-Reduce 패턴 구현

### 조건부 엣지 (기존 방식)를 사용하는 경우
✅ 단순한 정적 라우팅만 필요할 때
✅ 상태 업데이트 없이 **라우팅만** 수행
✅ 그래프 구조를 **명시적으로 시각화**하고 싶을 때

---

## 실전 예제: 요구사항 분석 시스템

### 문제 상황
요구사항 분석 시스템에서 메트릭 평가 노드가 기준을 통과하지 못하면 반성(reflection) 노드로 되돌아가는 피드백 루프가 필요합니다.

### 기존 방식 (조건부 엣지)

```python
def assess_metrics(state):
    # 메트릭 평가 로직
    results = evaluate_metrics(state)
    return {"assessment_results": results}

def routing_function(state):
    if state["assessment_results"]["passed"]:
        return "output_node"
    else:
        return "reflect_node"

builder.add_edge("reflect_node", "assess_metrics")
builder.add_conditional_edges(
    "assess_metrics",
    routing_function,
    {
        "output_node": "output_node",
        "reflect_node": "reflect_node"
    }
)
```

### Command 방식 (개선)

```python
def assess_metrics(state) -> Command[Literal["output_node", "reflect_node"]]:
    results = evaluate_metrics(state)

    if results["passed"]:
        return Command(
            update={
                "assessment_status": "success",
                "assessment_results": results
            },
            goto="output_node"
        )
    else:
        return Command(
            update={
                "assessment_status": "failure",
                "assessment_results": results,
                "rationale": results["gaps"]  # 실패 원인 추가
            },
            goto="reflect_node"
        )

# 엣지 정의 불필요 - 노드만 추가
builder.add_node("assess_metrics", assess_metrics)
builder.add_node("reflect_node", reflect_node)
builder.add_node("output_node", output_node)
```

### 장점
- 조건부 엣지와 라우팅 함수 제거 → **코드 복잡도 감소**
- 상태 업데이트와 라우팅 로직이 한 곳에 → **가독성 향상**
- 실패 시 추가 정보(rationale) 포함 → **컨텍스트 풍부화**

---

## 고급 패턴: Command로 복잡한 멀티 에이전트 구현

### 에이전트 핸드오프 도구 생성

```python
from typing import Annotated
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState, InjectedToolCallId

def create_handoff_tool(agent_name: str, description: str):
    """에이전트 간 핸드오프 도구 생성"""

    @tool(f"transfer_to_{agent_name}", description=description)
    def handoff_tool(
        task_description: Annotated[str, "다음 에이전트가 수행할 작업 설명"],
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        # 작업 설명 메시지 생성
        task_message = {
            "role": "user",
            "content": task_description
        }

        # 핸드오프 확인 메시지
        confirmation_message = {
            "role": "tool",
            "content": f"{agent_name}에게 성공적으로 이관되었습니다.",
            "tool_call_id": tool_call_id,
        }

        return Command(
            goto=agent_name,
            update={
                "messages": state["messages"] + [confirmation_message, task_message]
            },
            graph=Command.PARENT  # 부모 그래프의 에이전트로 라우팅
        )

    return handoff_tool

# 사용 예시
transfer_to_researcher = create_handoff_tool(
    "researcher",
    "리서치 작업을 연구원 에이전트에게 이관"
)
transfer_to_writer = create_handoff_tool(
    "writer",
    "글쓰기 작업을 작가 에이전트에게 이관"
)
```

---

## 성능 고려사항

### Command의 장점
- **복잡도 감소**: 엣지와 라우팅 함수가 불필요하여 그래프 구조 단순화
- **유지보수성**: 로직이 한 곳에 집중되어 수정 용이
- **유연성**: 런타임에 동적으로 라우팅 결정

### 시각화 주의사항
Command를 사용할 때 시각화를 제대로 지원하려면 타입 힌트가 필요합니다:

```python
# ✅ 올바른 시각화 지원
def my_node(state: State) -> Command[Literal["node_a", "node_b"]]:
    return Command(goto="node_a", update={...})

# ❌ 시각화 안 됨
def my_node(state: State) -> Command:
    return Command(goto="node_a", update={...})
```

---

## 마이그레이션 가이드

### 조건부 엣지 → Command

**Before:**
```python
def my_node(state):
    return {"processed": True}

def router(state):
    if state["processed"]:
        return "success_node"
    return "failure_node"

builder.add_node("my_node", my_node)
builder.add_conditional_edges("my_node", router, {
    "success_node": "success_node",
    "failure_node": "failure_node"
})
```

**After:**
```python
def my_node(state) -> Command[Literal["success_node", "failure_node"]]:
    if process_successful(state):
        return Command(
            update={"processed": True},
            goto="success_node"
        )
    return Command(
        update={"processed": False},
        goto="failure_node"
    )

builder.add_node("my_node", my_node)
# 엣지 정의 불필요!
```

---

## 참고 자료

- [공식 블로그: Command 소개](https://blog.langchain.com/command-a-new-tool-for-multi-agent-architectures-in-langgraph)
- [LangGraph 공식 문서 - Low Level Concepts](https://langchain-ai.github.io/langgraph/concepts/low_level)
- [GitHub Discussion: Send vs Command](https://github.com/langchain-ai/langgraph/discussions/4222)
- [Multi-Agent 아키텍처 가이드](https://langchain-ai.github.io/langgraph/concepts/multi_agent)

---

## 요약

- **Command**: 상태 업데이트 + 라우팅을 통합 관리하는 강력한 객체 (Send의 상위집합)
- **Send**: 동적 병렬 실행을 위한 메시징 메커니즘
- **관계**: Command의 `goto`에 Send 리스트를 포함 가능
- **권장**: 현대적인 LangGraph 개발에서는 Command 사용이 권장됨 (코드 간결성, 유지보수성)
