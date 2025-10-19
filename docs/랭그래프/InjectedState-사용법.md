# InjectedState: 도구(Tool)에서 그래프 상태(State)에 접근하기

`InjectedState`는 LangGraph에서 도구(Tool)를 정의할 때, 해당 도구가 현재 그래프의 전체 상태(state)에 접근할 수 있도록 해주는 특별한 타입 어노테이션입니다.

일반적으로 도구는 특정 입력값만 받아서 처리하지만, 때로는 도구가 작업을 수행하기 위해 현재까지 진행된 그래프의 전체적인 맥락이나 정보(즉, 상태)가 필요한 경우가 있습니다. 이때 `InjectedState`를 사용하면, LangGraph가 도구를 호출할 때 현재 그래프의 상태 객체를 해당 인자에 자동으로 주입해줍니다.

## 왜 InjectedState를 사용할까요?

1. **효율적인 상태 접근**: 도구가 LLM을 다시 호출하지 않고도 그래프의 현재 상태(예: 이전 메시지, 중간 결과 등)에 직접 접근하여 필요한 정보를 사용할 수 있습니다.
2. **토큰 사용량 감소**: 상태 정보를 얻기 위해 LLM에 추가적인 프롬프트를 보내지 않아도 되므로, 토큰 사용량을 절약할 수 있습니다.
3. **동적인 도구 실행**: 도구가 현재 상태를 기반으로 분기 처리 등 동적인 로직을 수행할 수 있게 됩니다. 예를 들어, 상태에 특정 정보가 있을 때만 다른 동작을 하도록 구현할 수 있습니다.
4. **라우팅 성능 향상**: 라우터(conditional edge)가 상태에 따라 다음 노드를 결정해야 할 때, `InjectedState`를 활용하면 불필요한 LLM 호출을 줄여 지연 시간을 단축하고 성능을 높일 수 있습니다.

## 사용 방법

`InjectedState`를 사용하려면, 도구로 사용할 함수의 파라미터에 `Annotated` 타입을 사용하여 `InjectedState`를 명시해주면 됩니다.

- `Annotated[전체_상태_타입, InjectedState()]` 와 같은 형태로 사용합니다.

### 예제 코드

다음은 사용자의 이름(name)을 상태에 저장하고, 도구가 해당 이름을 사용하여 인사말을 생성하는 간단한 예제입니다.

```python
import os
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, END

# .env 파일에서 API 키 로드
from dotenv import load_dotenv
load_dotenv()

# 1. 상태 정의 (State)
class MyState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    name: str  # 사용자의 이름을 저장할 필드

# 2. 도구 정의 (Tool)
# InjectedState를 사용하여 현재 상태(MyState)를 주입받습니다.
def get_greeting(state: Annotated[MyState, InjectedState()]):
    """사용자의 이름으로 인사말을 생성하는 도구"""
    name = state.get("name")
    if not name:
        return "안녕하세요! 성함을 알려주시겠어요?"
    return f"안녕하세요, {name}님!"

# 3. LLM 및 노드 설정
llm = ChatOpenAI(model="gpt-4o")
tools = [get_greeting]
llm_with_tools = llm.bind_tools(tools)

# 에이전트 노드: LLM을 호출하여 메시지를 처리
def agent_node(state: MyState):
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": [result]}

# 도구 노드: 도구를 실행
tool_node = ToolNode(tools)

# 4. 그래프 생성
graph_builder = StateGraph(MyState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", tool_node)

# 5. 엣지 연결
graph_builder.set_entry_point("agent")
graph_builder.add_conditional_edges(
    "agent",
    tools_condition, # 도구 호출이 있으면 "tools" 노드로, 없으면 END로 분기
)
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()

# 6. 그래프 실행
# 처음에는 이름 정보가 없는 상태로 시작
initial_state = {
    "messages": [HumanMessage(content="인사말을 만들어주세요.")],
    "name": "" 
}
print("--- 이름 정보가 없을 때 ---")
for chunk in graph.stream(initial_state, stream_mode="values"):
    print(chunk)

# 이름 정보가 있는 상태로 실행
initial_state_with_name = {
    "messages": [HumanMessage(content="인사말을 만들어주세요.")],
    "name": "홍길동"
}
print("\n--- 이름 정보가 있을 때 ---")
for chunk in graph.stream(initial_state_with_name, stream_mode="values"):
    print(chunk)

```

### 실행 결과

```
--- 이름 정보가 없을 때 ---
{'agent': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_abc', 'function': {'arguments': '{}', 'name': 'get_greeting'}, 'type': 'tool'}]})]}}
{'tools': {'messages': [ToolMessage(content='안녕하세요! 성함을 알려주시겠어요?', tool_call_id='call_abc')]}}
{'agent': {'messages': [AIMessage(content='안녕하세요! 성함을 알려주시겠어요?')]}}
{'__end__': {'messages': [HumanMessage(content='인사말을 만들어주세요.'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_abc', 'function': {'arguments': '{}', 'name': 'get_greeting'}, 'type': 'tool'}]}), ToolMessage(content='안녕하세요! 성함을 알려주시겠어요?', tool_call_id='call_abc'), AIMessage(content='안녕하세요! 성함을 알려주시겠어요?')], 'name': ''}}

--- 이름 정보가 있을 때 ---
{'agent': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_def', 'function': {'arguments': '{}', 'name': 'get_greeting'}, 'type': 'tool'}]})]}}
{'tools': {'messages': [ToolMessage(content='안녕하세요, 홍길동님!', tool_call_id='call_def')]}}
{'agent': {'messages': [AIMessage(content='안녕하세요, 홍길동님!')]}}
{'__end__': {'messages': [HumanMessage(content='인사말을 만들어주세요.'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_def', 'function': {'arguments': '{}', 'name': 'get_greeting'}, 'type': 'tool'}]}), ToolMessage(content='안녕하세요, 홍길동님!', tool_call_id='call_def'), AIMessage(content='안녕하세요, 홍길동님!')], 'name': '홍길동'}}
```

위 예제에서 `get_greeting` 도구는 `state: Annotated[MyState, InjectedState()]`를 통해 현재 `MyState` 객체 전체를 주입받습니다. 그리고 `state.get("name")` 코드를 통해 상태에 저장된 `name` 값에 접근하여 분기 처리를 수행하는 것을 볼 수 있습니다. 이 과정에서 LLM은 `get_greeting` 도구를 호출하라는 결정만 내렸을 뿐, `name` 값을 직접 다루지는 않았습니다.
