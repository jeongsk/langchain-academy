---
created: 2025-10-12 02:40:33
updated: 2025-10-12 12:22:38
tags:
  - LangGraph
  - 디자인_패턴
  - 노드_Node
  - 코드_구조
  - 리팩토링
---
[[랭그래프/LangGraph|LangGraph]]에서 노드를 추가할 때 더 나은 방법들을 소개합니다.

## 1. 데코레이터 패턴 (가장 추천)

```python
from langgraph.graph import StateGraph
from functools import wraps

class GraphBuilder:
    def __init__(self, state_schema):
        self.graph = StateGraph(state_schema)
        self.nodes = {}

    def node(self, name=None):
        """노드를 자동으로 등록하는 데코레이터"""
        def decorator(func):
            node_name = name or func.__name__
            self.nodes[node_name] = func
            self.graph.add_node(node_name, func)
            return func
        return decorator

# 사용 예시
builder = GraphBuilder(state_schema)

@builder.node()
def process_input(state):
    return {"result": "processed"}

@builder.node("custom_name")  # 커스텀 이름도 가능
def analyze_data(state):
    return {"analysis": "complete"}
```

## 2. 노드 클래스 패턴

```python
from abc import ABC, abstractmethod

class Node(ABC):
    """노드 베이스 클래스"""
    @property
    def name(self):
        return self.__class__.__name__.lower().replace("node", "")

    @abstractmethod
    def __call__(self, state):
        pass

class ProcessInputNode(Node):
    def __call__(self, state):
        return {"result": "processed"}

class AnalyzeDataNode(Node):
    def __call__(self, state):
        return {"analysis": "complete"}

# 사용
graph = StateGraph(state_schema)
nodes = [ProcessInputNode(), AnalyzeDataNode()]

for node in nodes:
    graph.add_node(node.name, node)
```

## 3. 설정 기반 패턴

```python
from typing import Callable, Dict
from dataclasses import dataclass

@dataclass
class NodeConfig:
    name: str
    func: Callable
    description: str = ""
    tags: list = None

def process_input(state):
    return {"result": "processed"}

def analyze_data(state):
    return {"analysis": "complete"}

# 노드 설정 정의
NODE_CONFIGS = [
    NodeConfig(
        name="input_processor",
        func=process_input,
        description="입력 데이터 처리",
        tags=["preprocessing"]
    ),
    NodeConfig(
        name="data_analyzer",
        func=analyze_data,
        description="데이터 분석",
        tags=["analysis"]
    ),
]

# 그래프 구성
graph = StateGraph(state_schema)
for config in NODE_CONFIGS:
    graph.add_node(config.name, config.func)
```

## 4. 타입 안전 패턴 (TypedDict + Enum)

```python
from enum import Enum
from typing import TypedDict, Callable

class NodeName(str, Enum):
    """노드 이름을 Enum으로 관리"""
    PROCESS_INPUT = "process_input"
    ANALYZE_DATA = "analyze_data"
    GENERATE_OUTPUT = "generate_output"

class NodeRegistry(TypedDict):
    name: NodeName
    handler: Callable

def process_input(state):
    return {"result": "processed"}

def analyze_data(state):
    return {"analysis": "complete"}

# 레지스트리
NODES: list[NodeRegistry] = [
    {"name": NodeName.PROCESS_INPUT, "handler": process_input},
    {"name": NodeName.ANALYZE_DATA, "handler": analyze_data},
]

# 그래프 구성
graph = StateGraph(state_schema)
for node in NODES:
    graph.add_node(node["name"].value, node["handler"])

# 엣지 추가 시에도 타입 안전
graph.add_edge(NodeName.PROCESS_INPUT.value, NodeName.ANALYZE_DATA.value)
```

## 5. 체이닝 패턴 (Fluent API)

```python
class FluentGraphBuilder:
    def __init__(self, state_schema):
        self.graph = StateGraph(state_schema)

    def add_node(self, name, func):
        self.graph.add_node(name, func)
        return self  # 체이닝을 위해 self 반환

    def add_edge(self, from_node, to_node):
        self.graph.add_edge(from_node, to_node)
        return self

    def build(self):
        return self.graph.compile()

# 사용
app = (FluentGraphBuilder(state_schema)
    .add_node("process", process_input)
    .add_node("analyze", analyze_data)
    .add_edge("process", "analyze")
    .build())
```

## 추천 조합

실제 프로젝트에서는 **Enum + 데코레이터 패턴**을 조합하는 것을 추천합니다:

```python
from enum import Enum
from langgraph.graph import StateGraph

class NodeName(str, Enum):
    PROCESS = "process_input"
    ANALYZE = "analyze_data"

class MyGraph:
    def __init__(self, state_schema):
        self.graph = StateGraph(state_schema)
        self._register_nodes()

    def _register_nodes(self):
        """모든 노드를 자동 등록"""
        self.graph.add_node(NodeName.PROCESS, self.process_input)
        self.graph.add_node(NodeName.ANALYZE, self.analyze_data)

    def process_input(self, state):
        return {"result": "processed"}

    def analyze_data(self, state):
        return {"analysis": "complete"}

    def build(self):
        self.graph.add_edge(NodeName.PROCESS, NodeName.ANALYZE)
        return self.graph.compile()
```

## 각 패턴의 장단점

### 데코레이터 패턴

- **장점**: 깔끔한 문법, 자동 등록, 가독성 높음
- **단점**: 클래스 기반 노드에는 적용하기 어려움

### 노드 클래스 패턴

- **장점**: OOP 원칙 준수, 재사용성 높음, 테스트 용이
- **단점**: 보일러플레이트 코드 증가

### 설정 기반 패턴

- **장점**: 노드 정보 중앙 관리, 동적 구성 가능
- **단점**: 런타임 오류 가능성

### 타입 안전 패턴

- **장점**: IDE 자동완성 지원, 타입 체크로 버그 예방
- **단점**: Enum 관리 필요

### 체이닝 패턴

- **장점**: 직관적인 그래프 구성, 유창한 API
- **단점**: 복잡한 그래프에서는 가독성 저하 가능

## 패턴 선택 가이드

| 프로젝트 규모 | 추천 패턴 |
|------------|---------|
| 소규모 (노드 < 5개) | 데코레이터 패턴 |
| 중규모 (노드 5-20개) | Enum + 클래스 조합 |
| 대규모 (노드 > 20개) | 설정 기반 + 타입 안전 패턴 |

이 방법들은 **타입 안전성, 유지보수성, 확장성**을 모두 고려한 패턴들입니다.

## 관련 문서

- [[LangGraph 기본 개념]]
- [[상태 관리 패턴]]
- [[그래프 설계 베스트 프랙티스]]
