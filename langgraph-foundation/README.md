# Foundation Introduction to LangGraph

## 소개

LangGraph 입문 과정에 오신 것을 환영합니다! 본 과정은 기초부터 시작하여 점차 고급 주제로 나아가는 여섯 개의 모듈로 구성되어 있습니다.

각 모듈에는 핵심 개념을 안내하는 동영상 강의와 해당 노트북이 포함되어 있습니다. 또한 각 모듈에는 **studio** 하위 디렉터리가 마련되어 있으며, 여기에는 LangGraph API와 Studio를 활용하여 탐구할 관련 그래프 세트가 포함되어 있습니다.

## 학습 목표

이 Foundation 시리즈를 통해 다음을 학습할 수 있습니다:

- LangGraph의 핵심 개념과 구성 요소
- 상태 관리와 메모리 시스템 구현
- Human-in-the-loop 워크플로우 설계
- 병렬 처리 및 서브그래프 활용
- 고급 메모리 관리 기법
- 프로덕션 배포 및 클라이언트 연결

## 모듈 구성

### [Module 1: LangGraph 입문](./module-1/README.md)

LangGraph의 기본 개념과 핵심 구성 요소를 학습하는 모듈입니다. 그래프, 노드, 에지의 기초부터 시작하여 메모리를 가진 에이전트 구축까지 단계별로 진행합니다.

**주요 내용:**

- 그래프 기초 (Nodes, Edges, State)
- 간단한 체인 구현
- 라우터 패턴
- 도구를 사용하는 에이전트

### [Module 2: 상태 관리와 메모리](./module-2/README.md)

LangGraph의 고급 상태 관리 기법과 메모리 시스템을 학습하는 모듈입니다. 상태 스키마 커스터마이징부터 시작하여 외부 데이터베이스를 활용한 지속적 메모리까지 단계별로 진행합니다.

**주요 내용:**

- 상태 스키마 커스터마이징
- Reducers를 활용한 상태 업데이트 제어
- 메시지 트리밍 및 필터링
- SQLite를 활용한 외부 메모리

### [Module 3: Human-in-the-Loop](./module-3/README.md)

LangGraph에서 사람이 개입할 수 있는 워크플로우를 구현하는 방법을 학습하는 모듈입니다. 스트리밍부터 시작하여 중단점, 상태 편집, 동적 중단점, 시간 여행까지 단계별로 진행합니다.

**주요 내용:**

- 스트리밍 구현
- 중단점(Breakpoints) 설정
- 상태 편집 및 재실행
- 동적 중단점
- 시간 여행 (Time Travel)

### [Module 4: 고급 LangGraph 기술](./module-4/README.md)

LangGraph의 병렬 처리, 서브그래프, 맵리듀스 등 고급 기능을 학습하고, 이를 활용하여 리서치 어시스턴트를 구축합니다.

**주요 내용:**

- 병렬 처리 (Parallelization)
- 서브그래프 (Sub-graphs)
- 맵리듀스 패턴 (Map-Reduce)
- 리서치 어시스턴트 구현

### [Module 5: LangGraph 메모리 심화](./module-5/README.md)

LangGraph의 고급 메모리 관리 기법을 학습하는 모듈입니다. `BaseStore`를 활용한 메모리 저장소 커스터마이징부터 `StateSchema`를 이용한 복잡한 상태 관리까지 다룹니다.

**주요 내용:**

- BaseStore 인터페이스
- StateSchema를 활용한 상태 관리
- Redis 통합
- 메모리 최적화 기법

### [Module 6: LangGraph 서버 배포 및 연결](./module-6/README.md)

LangGraph로 구축한 그래프를 원격 서버로 배포하고, 클라이언트에서 해당 서버에 연결하여 사용하는 방법을 학습합니다.

**주요 내용:**

- LangGraph 서버 배포
- 클라이언트 SDK 사용
- API 엔드포인트 활용
- 프로덕션 환경 설정

## 학습 경로

1. **기초 (Module 1-2)**: LangGraph 핵심 개념과 상태 관리 마스터
2. **중급 (Module 3-4)**: Human-in-the-loop 및 고급 패턴 활용
3. **고급 (Module 5-6)**: 메모리 심화 및 프로덕션 배포

## 다음 단계

Foundation 과정을 완료한 후에는:

- **[Ambient Agents](../projects/ambient-agents/README.md)**: 실전 프로젝트로 학습한 내용 적용
- **[Tutorial](../langgraph-tutorial/README.md)**: 다양한 패턴과 예제 탐구

## 리소스

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangSmith](https://smith.langchain.com/)
