# LangGraph Issue #4748: 부모 그래프 상태 업데이트 시 서브그래프 상태 손실

**출처**: https://github.com/langchain-ai/langgraph/issues/4748
**작성일**: 2025-10-18

## 문제 요약

부모 그래프의 상태를 업데이트하면 서브그래프의 상태가 손실되고, 서브그래프가 중단된 지점부터 재개되지 않고 처음부터 다시 시작되는 버그입니다.

## 상세 설명

### 발생 조건
- 중단(interrupt) 기능을 사용하는 그래프와 서브그래프
- 서브그래프의 노드가 중단된 후, 부모 그래프의 상태를 `update_state()`로 업데이트하는 경우

### 문제점
1. **상태 손실**: 서브그래프 노드에서 실행된 결과가 부모 그래프의 상태에 반영되지 않음
2. **실행 흐름 손실**: 서브그래프가 중단된 지점부터 계속되지 않고 처음부터 재실행됨

## 예제 코드 구조

### 서브그래프 구성
```python
class State(TypedDict):
    foo: bool
    bar: bool

# 서브그래프
subgraph_builder = StateGraph(State)
subgraph_builder.add_node("subgraph_node_1", subgraph_node_1)  # foo를 True로 설정
subgraph_builder.add_node("subgraph_node_2", subgraph_node_2)
subgraph = subgraph_builder.compile(
    interrupt_after=["subgraph_node_1", "subgraph_node_2"]
)
```

### 부모 그래프 구성
```python
builder = StateGraph(State)
builder.add_node("node1", node1)
builder.add_node("node2", subgraph)  # 서브그래프를 노드로 추가
builder.add_node("node3", node3)

graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_after=["node1", "node3"]
)
```

### 문제 재현 시나리오
```python
# 1. 초기 실행 - subgraph_node_1에서 중단됨
graph.stream({"foo": False, "bar": False}, config)

# 2. 계속 실행 (None 전달)
graph.stream(None, config)

# 3. 부모 그래프 상태 업데이트
new_config = graph.update_state(config, {"bar": True})

# 4. 다시 계속 실행
graph.stream(None, new_config)  # 여기서 문제 발생!
```

## 예상 vs 실제 동작

### 예상 동작 ✓
1. `node1` 실행
2. `subgraph_node_1` 실행 (foo = True로 설정)
3. **[상태 업데이트: bar = True]**
4. `subgraph_node_2` 실행 (중단된 지점부터 계속)
5. 최종 상태: `{'foo': True, 'bar': True}`

### 실제 동작 ✗
1. `node1` 실행
2. `subgraph_node_1` 실행 (foo = True로 설정)
3. **[상태 업데이트: bar = True]**
4. `subgraph_node_1` 실행 (처음부터 다시 시작! 초기 상태로 덮어씀)
5. 최종 상태: `{'foo': False, 'bar': True}`

## 영향 범위

이 버그는 다음과 같은 사용 사례에 영향을 미칩니다:

- **Human-in-the-loop 패턴**: 서브그래프 실행 중 사용자 입력으로 상태를 수정하는 경우
- **동적 상태 관리**: 서브그래프 실행 중간에 외부 이벤트나 조건에 따라 상태를 업데이트해야 하는 경우
- **복잡한 워크플로우**: 여러 서브그래프가 중첩되어 있고 상태를 공유하는 경우

## 시스템 정보

- **OS**: Linux (Ubuntu 22.04)
- **Python**: 3.12.7
- **langchain_core**: 0.3.60
- **langgraph_sdk**: 0.1.69
- **langsmith**: 0.3.42

## 관련 학습 모듈

- **Module 3**: Human-in-the-loop (중단점, 상태 편집, 타임 트래블)
- **Module 4**: 병렬화, 서브그래프, Map-Reduce 패턴

## 해결 방법 (임시)

이 버그가 수정될 때까지 다음과 같은 우회 방법을 고려할 수 있습니다:

1. **서브그래프 중단 회피**: 가능하면 서브그래프 내부에서 중단하지 않고, 부모 그래프 레벨에서만 중단
2. **상태 업데이트 타이밍 조정**: 서브그래프가 완전히 종료된 후에 상태를 업데이트
3. **서브그래프 상태 별도 관리**: 서브그래프 전용 상태 키를 사용하여 부모 그래프 상태 업데이트의 영향 최소화

## 참고사항

이 문제는 LangGraph의 체크포인팅 메커니즘과 서브그래프 실행 컨텍스트 간의 상호작용에서 발생하는 것으로 보입니다. 부모 그래프의 상태를 업데이트할 때 서브그래프의 실행 포인터가 제대로 보존되지 않는 것이 근본 원인일 가능성이 높습니다.
