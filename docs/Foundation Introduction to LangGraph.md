---
created: 2025-10-10 21:42:28
updated: 2025-10-19 11:12:38
tags:
  - LangGraph
  - 학습_가이드
  - MOC
---
## 소개

[[index|LangGraph Academy]]의 LangGraph 입문 과정에 오신 것을 환영합니다! 본 과정은 기초부터 시작하여 점차 고급 주제로 나아가는 여섯 개의 모듈로 구성되어 있습니다.

각 모듈에는 핵심 개념을 안내하는 동영상 강의와 해당 노트북이 포함되어 있습니다. 또한 각 모듈에는 '**studio**' 하위 디렉터리가 마련되어 있으며, 여기에는 LangGraph API와 Studio를 활용하여 탐구할 관련 그래프 세트가 포함되어 있습니다.

## 목차

### [모듈 1: LangGraph 입문](https://github.com/jeongsk/langchain-academy/blob/main/foundation/module-1/README.md)

LangGraph의 기본 개념과 핵심 구성 요소를 학습하는 모듈입니다. 그래프, 노드, 에지의 기초부터 시작하여 메모리를 가진 에이전트 구축까지 단계별로 진행합니다.

### [모듈 2: 상태 관리와 메모리](https://github.com/jeongsk/langchain-academy/blob/main/foundation/module-2/README.md)

LangGraph의 고급 상태 관리 기법과 메모리 시스템을 학습하는 모듈입니다. 상태 스키마 커스터마이징부터 시작하여 외부 데이터베이스를 활용한 지속적 메모리까지 단계별로 진행합니다.

### [모듈 3: Human-in-the-Loop](https://github.com/jeongsk/langchain-academy/blob/main/foundation/module-3/README.md)

LangGraph에서 사람이 개입할 수 있는 워크플로우를 구현하는 방법을 학습하는 모듈입니다. 스트리밍부터 시작하여 중단점, 상태 편집, 동적 중단점, 시간 여행까지 단계별로 진행합니다.

### [모듈 4: 고급 LangGraph 기술](https://github.com/jeongsk/langchain-academy/blob/main/foundation/module-4/README.md)

LangGraph의 병렬 처리, 서브그래프, 맵리듀스 등 고급 기능을 학습하고, 이를 활용하여 리서치 어시스턴트를 구축합니다.

### [모듈 5: LangGraph 메모리 심화](https://github.com/jeongsk/langchain-academy/blob/main/foundation/module-5/README.md)

LangGraph의 고급 메모리 관리 기법을 학습하는 모듈입니다. `BaseStore`를 활용한 메모리 저장소 커스터마이징부터 `StateSchema`를 이용한 복잡한 상태 관리까지 다룹니다.

### [모듈 6: LangGraph 서버 배포 및 연결](https://github.com/jeongsk/langchain-academy/blob/main/foundation/module-6/README.md)

LangGraph로 구축한 그래프를 원격 서버로 배포하고, 클라이언트에서 해당 서버에 연결하여 사용하는 방법을 학습합니다.

## 다음 단계

Foundation 과정을 완료한 후에는:

- **[Ambient Agents 프로젝트](https://github.com/jeongsk/langchain-academy/blob/main/ambient-agents/README.md)**: 실전 프로젝트로 학습한 내용 적용
- **[Tutorial](https://github.com/jeongsk/langchain-academy/blob/main/tutorial/README.md)**: 다양한 패턴과 예제 탐구

## 시작하기

본 강좌를 시작하기 전에 [개발 환경 설정](개발%20환경%20설정.md) 페이지를 참조하여 필요한 환경을 구성해주세요.

## 학습 방법

1. 각 모듈은 순서대로 학습하는 것을 권장합니다
2. 각 모듈의 노트북을 실행하며 실습해보세요
3. LangGraph Studio를 활용하여 시각적으로 그래프를 확인하고 테스트해보세요
4. 각 모듈의 프로젝트를 직접 구현해보며 이해를 깊게 하세요

> [!tip] "팁"
> LangSmith를 함께 사용하면 에이전트의 실행 과정을 더 자세히 관찰하고 디버깅할 수 있습니다.

## 리소스

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [GitHub 저장소](https://github.com/jeongsk/langchain-academy)
