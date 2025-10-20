# Module 3: Human-in-the-Loop

LangGraph에서 사람이 개입할 수 있는 워크플로우를 구현하는 방법을 학습하는 모듈입니다. 스트리밍부터 시작하여 중단점, 상태 편집, 동적 중단점, 시간 여행까지 단계별로 진행합니다.

## 📚 학습 내용

### [1. 스트리밍과 중단 (1-streaming-interruption.ipynb)](1-streaming-interruption.ipynb)

- LangGraph의 스트리밍 기능과 다양한 스트리밍 모드
- `values`와 `updates` 모드를 통한 그래프 상태 스트리밍
- 토큰 단위 스트리밍과 `.astream_events` 메서드 활용
- LangGraph API를 통한 스트리밍 구현

### [2. 중단점 (2-breakpoints.ipynb)](2-breakpoints.ipynb)

- 사용자 승인을 위한 중단점(Breakpoints) 설정
- `interrupt_before` 옵션을 통한 그래프 실행 제어
- 중단점에서 사용자 입력을 받고 승인 프로세스 구현
- LangGraph API를 사용한 중단점 관리

### [3. 상태 편집과 사람 피드백 (3-edit-state-human-feedback.ipynb)](3-edit-state-human-feedback.ipynb)

- 중단점에서 그래프 상태를 직접 편집하는 방법
- `update_state`를 사용한 상태 수정과 메시지 덮어쓰기
- 사용자 피드백을 위한 placeholder 노드 구현
- `as_node` 매개변수를 통한 특정 노드로서의 상태 업데이트

### [4. 동적 중단점 (4-dynamic-breakpoints.ipynb)](4-dynamic-breakpoints.ipynb)

- `NodeInterrupt`를 사용한 조건부 중단점 구현
- 그래프가 스스로 동적으로 중단하는 메커니즘
- 중단 이유를 사용자에게 전달하는 방법
- 내부 로직에 따른 조건부 중단 처리

### [5. 시간 여행 (5-time-travel.ipynb)](5-time-travel.ipynb)

- 과거 상태를 탐색하고 재생하는 시간 여행 기능
- `get_state_history`를 통한 상태 히스토리 조회
- 특정 체크포인트에서 그래프 재실행(Replaying)
- 분기(Forking)를 통한 대안 경로 탐색

## 🎯 학습 목표

이 모듈을 완료하면 다음을 할 수 있습니다:

- Human-in-the-Loop의 세 가지 주요 동기 이해 (승인, 디버깅, 편집)
- 다양한 스트리밍 모드를 활용한 실시간 상태 모니터링
- 중단점을 통한 사용자 승인 워크플로우 구현
- 그래프 상태를 동적으로 편집하고 사용자 피드백 반영
- 동적 중단점을 통한 조건부 제어 흐름 구현
- 시간 여행 기능을 활용한 디버깅과 대안 경로 탐색

## 🚀 시작하기

1. 환경 설정을 위해 [`1-streaming-interruption.ipynb`](1-streaming-interruption.ipynb)부터 시작하세요
2. 각 노트북을 순서대로 진행하는 것을 권장합니다
3. `studio/` 디렉토리의 파일들은 LangGraph Studio에서 활용할 수 있습니다
   - `agent.py`: 기본 에이전트 구현
   - `dynamic_breakpoints.py`: 동적 중단점 예제
   - `langgraph.json`: Studio 설정 파일
