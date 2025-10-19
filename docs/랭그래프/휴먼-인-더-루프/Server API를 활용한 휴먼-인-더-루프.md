---
created: 2025-10-15 00:40:29
updated: 2025-10-15 00:48:22
source: https://docs.langchain.com/langsmith/add-human-in-the-loop
tags:
  - LangGraph
  - 휴먼_인_더_루프
  - Server_API
  - SDK
  - 튜토리얼
  - 중단_Interrupt
---
[[랭그래프/에이전트/에이전트란 무엇인가요?|에이전트]]나 워크플로우에서 도구 호출을 검토하고 편집하며 승인하려면, [[랭그래프/LangGraph|LangGraph]]의 [[랭그래프/휴먼-인-더-루프/휴먼-인-더-루프 개요|휴먼-인-더-루프]] 기능을 사용하세요. 이 문서는 특히 [[랭그래프/LangGraph 배포 가이드|배포된 LangGraph 서버]]와 상호작용하는 방법을 다룹니다.

## 동적 인터럽트

```python
from langgraph_sdk import get_client
from langgraph_sdk.schema import Command

client = get_client(url=<DEPLOYMENT_URL>)

# "agent"라는 이름으로 배포된 그래프 사용
assistant_id = "agent"

# 스레드 생성
thread = await client.threads.create()
thread_id = thread["thread_id"]

# 중단이 발생할 때까지 그래프 실행
result = await client.runs.wait(
    thread_id,
    assistant_id,
    input={"some_text": "original text"}   # (1)!
)

print(result['__interrupt__']) # (2)!
# > [
# >     {
# >         'value': {'text_to_revise': 'original text'},
# >         'resumable': True,
# >         'ns': ['human_node:fc722478-2f21-0578-c572-d9fc4dd07c3b'],
# >         'when': 'during'
# >     }
# > ]

# 그래프 재개
print(await client.runs.wait(
    thread_id,
    assistant_id,
    command=Command(resume="Edited text")   # (3)!
))
# > {'some_text': 'Edited text'}
```

1. 초기 상태와 함께 그래프가 호출됩니다.
2. 그래프가 중단에 도달하면 페이로드와 메타데이터가 포함된 중단 객체를 반환합니다.
3. `Command(resume=...)`를 사용하여 그래프를 재개하며, 사용자 입력을 주입하여 실행을 계속합니다.

다음은 LangGraph API 서버에서 실행할 수 있는 예시 그래프입니다. 자세한 내용은 [LangSmith 빠른 시작 가이드](https://docs.langchain.com/langsmith/deployment-quickstart)를 참조하세요.

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
    value = interrupt( # (1)!
        {
            "text_to_revise": state["some_text"] # (2)!
        }
    )
    return {
        "some_text": value # (3)!
    }

# 그래프 빌드
graph_builder = StateGraph(State)
graph_builder.add_node("human_node", human_node)
graph_builder.add_edge(START, "human_node")
graph = graph_builder.compile()
```

1. `interrupt(...)`는 `human_node`에서 실행을 일시 중지하고, 주어진 페이로드를 사용자에게 표시합니다.
2. JSON 직렬화 가능한 모든 값을 `interrupt` 함수에 전달할 수 있습니다. 여기서는 수정할 텍스트를 포함하는 딕셔너리를 사용합니다.
3. 재개되면 `interrupt(...)`의 반환 값은 사용자가 제공한 입력이 되며, 이는 상태를 업데이트하는 데 사용됩니다.

실행 중인 LangGraph API 서버가 있으면 [LangGraph SDK](https://docs.langchain.com/langsmith/python-sdk)를 사용하여 상호작용할 수 있습니다.

```python
from langgraph_sdk import get_client
from langgraph_sdk.schema import Command

client = get_client(url=<DEPLOYMENT_URL>)

# "agent"라는 이름으로 배포된 그래프 사용
assistant_id = "agent"

# 스레드 생성
thread = await client.threads.create()
thread_id = thread["thread_id"]

# 중단이 발생할 때까지 그래프 실행
result = await client.runs.wait(
    thread_id,
    assistant_id,
    input={"some_text": "original text"}   # (1)!
)

print(result['__interrupt__']) # (2)!
# > [
# >     {
# >         'value': {'text_to_revise': 'original text'},
# >         'resumable': True,
# >         'ns': ['human_node:fc722478-2f21-0578-c572-d9fc4dd07c3b'],
# >         'when': 'during'
# >     }
# > ]

# 그래프 재개
print(await client.runs.wait(
    thread_id,
    assistant_id,
    command=Command(resume="Edited text")   # (3)!
))
# > {'some_text': 'Edited text'}
```

1. 초기 상태와 함께 그래프가 호출됩니다.
2. 그래프가 중단에 도달하면 페이로드와 메타데이터가 포함된 중단 객체를 반환합니다.
3. `Command(resume=...)`를 사용하여 그래프를 재개하며, 사용자 입력을 주입하여 실행을 계속합니다.

## 정적 인터럽트

정적 중단(정적 브레이크포인트라고도 함)은 노드 실행 전후에 트리거됩니다. 컴파일 시 `interrupt_before`와 `interrupt_after`를 지정하여 정적 중단을 설정할 수 있습니다:

```python
graph = graph_builder.compile( # (1)!
    interrupt_before=["node_a"], # (2)!
    interrupt_after=["node_b", "node_c"], # (3)!
)
```

1. 브레이크포인트는 `compile` 시점에 설정됩니다.
2. `interrupt_before`는 노드가 실행되기 전에 실행을 일시 중지할 노드를 지정합니다.
3. `interrupt_after`는 노드가 실행된 후에 실행을 일시 중지할 노드를 지정합니다.

또는 런타임에 정적 중단을 설정할 수도 있습니다:

```python
await client.runs.wait( # (1)!
    thread_id,
    assistant_id,
    inputs=inputs,
    interrupt_before=["node_a"], # (2)!
    interrupt_after=["node_b", "node_c"] # (3)!
)
```

1. `interrupt_before`와 `interrupt_after` 파라미터와 함께 `client.runs.wait`을 호출합니다. 이는 런타임 구성이며 호출할 때마다 변경할 수 있습니다.
2. `interrupt_before`는 노드가 실행되기 전에 실행을 일시 중지할 노드를 지정합니다.
3. `interrupt_after`는 노드가 실행된 후에 실행을 일시 중지할 노드를 지정합니다.

다음 예제는 정적 중단을 추가하는 방법을 보여줍니다:

```python
from langgraph_sdk import get_client

client = get_client(url=<DEPLOYMENT_URL>)

# "agent"라는 이름으로 배포된 그래프 사용
assistant_id = "agent"

# 스레드 생성
thread = await client.threads.create()
thread_id = thread["thread_id"]

# 브레이크포인트에 도달할 때까지 그래프 실행
result = await client.runs.wait(
    thread_id,
    assistant_id,
    input=inputs   # (1)!
)

# 그래프 재개
await client.runs.wait(
    thread_id,
    assistant_id,
    input=None   # (2)!
)
```

1. 첫 번째 브레이크포인트에 도달할 때까지 그래프가 실행됩니다.
2. 입력에 `None`을 전달하여 그래프를 재개합니다. 이렇게 하면 다음 브레이크포인트에 도달할 때까지 그래프가 실행됩니다.

## 더 알아보기

- [휴먼-인-더-루프 개념 가이드](https://docs.langchain.com/oss/python/langgraph/interrupts): LangGraph의 휴먼-인-더-루프 기능에 대해 자세히 알아보세요.
- [일반적인 패턴](https://docs.langchain.com/oss/python/langgraph/interrupts#common-patterns): 작업 승인/거부, 사용자 입력 요청, 도구 호출 검토, 사용자 입력 검증과 같은 패턴을 구현하는 방법을 알아보세요.

---

[GitHub에서 이 페이지의 소스 편집하기](https://github.com/langchain-ai/edit/main/src/langsmith/add-human-in-the-loop.mdx)

[이전: Streaming API](https://docs.langchain.com/langsmith/streaming)

[다음: Server API를 사용한 타임 트래블](https://docs.langchain.com/langsmith/human-in-the-loop-time-travel)
