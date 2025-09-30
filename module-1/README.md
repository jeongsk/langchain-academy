# Module 1: LangGraph 입문

LangGraph의 기본 개념과 핵심 구성 요소를 학습하는 모듈입니다. 그래프, 노드, 에지의 기초부터 시작하여 메모리를 가진 에이전트 구축까지 단계별로 진행합니다.

## 📚 학습 내용

### [1. 기초 설정 (1-basics.ipynb)](1-basics.ipynb)
- LangChain Academy 소개 및 환경 설정
- 채팅 모델과 도구(Tools) 기본 사용법
- OpenAI API 및 Tavily 검색 도구 설정

### [2. 간단한 그래프 (2-simple-graph.ipynb)](2-simple-graph.ipynb)
- LangGraph의 핵심 개념: State, Nodes, Edges
- 3개의 노드와 조건부 에지를 가진 기본 그래프 구조
- StateGraph 클래스 사용법과 그래프 컴파일

### [3. 체인 구축 (3-chain.ipynb)](3-chain.ipynb)
- 채팅 메시지를 상태로 사용하는 방법
- 채팅 모델에 도구 연결 및 도구 호출 실행
- MessagesState와 Reducers 개념 이해

### [4. 라우터 (4-router.ipynb)](4-router.ipynb)
- 사용자 입력에 따른 조건부 라우팅 구현
- ToolNode와 tools_condition 사용법
- LangGraph Studio 소개 및 활용

### [5. 에이전트 (5-agent.ipynb)](5-agent.ipynb)
- ReAct 패턴을 활용한 에이전트 구축
- Act(행동) → Observe(관찰) → Reason(추론) 순환 구조
- 복수 도구를 활용한 복합적 작업 처리

### [6. 에이전트 메모리 (6-agent-memory.ipynb)](6-agent-memory.ipynb)
- MemorySaver를 활용한 대화 상태 지속성
- Thread ID를 통한 세션 관리
- 연속적 대화가 가능한 에이전트 구현

## 🎯 학습 목표

이 모듈을 완료하면 다음을 할 수 있습니다:
- LangGraph의 기본 구조와 개념 이해
- 상태 관리와 메시지 처리 방법 숙지
- 도구를 활용한 에이전트 구축
- 메모리 기능을 가진 대화형 시스템 개발

## 🚀 시작하기

1. 환경 설정을 위해 [`1-basics.ipynb`](1-basics.ipynb)부터 시작하세요
2. 각 노트북을 순서대로 진행하는 것을 권장합니다
3. `studio/` 디렉토리의 파일들은 LangGraph Studio에서 활용할 수 있습니다