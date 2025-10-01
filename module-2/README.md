# Module 2: 상태 관리와 메모리

LangGraph의 고급 상태 관리 기법과 메모리 시스템을 학습하는 모듈입니다. 상태 스키마 커스터마이징부터 시작하여 외부 데이터베이스를 활용한 지속적 메모리까지 단계별로 진행합니다.

## 📚 학습 내용

### [1. 상태 스키마 (1-state-schema.ipynb)](1-state-schema.ipynb)
- LangGraph 상태 스키마 정의 방법
- TypedDict, Dataclass, Pydantic을 활용한 상태 구조화
- 런타임 데이터 검증과 타입 안전성 확보

### [2. 상태 리듀서 (2-state-reducers.ipynb)](2-state-reducers.ipynb)
- 상태 업데이트 방식 제어하는 리듀서 개념
- 병렬 노드 실행 시 상태 충돌 해결
- 사용자 정의 리듀서와 메시지 처리 패턴

### [3. 멀티 스키마 (3-multiple-schemas.ipynb)](3-multiple-schemas.ipynb)
- 노드 간 Private State 전달 방법
- 그래프 입력/출력 스키마 분리 설계
- 다중 스키마 활용한 유연한 그래프 구조

### [4. 메시지 필터링 및 트리밍 (4-trim-filter-messages.ipynb)](4-trim-filter-messages.ipynb)
- 장기 대화에서 토큰 사용량 최적화
- RemoveMessage를 활용한 메시지 삭제
- trim_messages를 통한 토큰 기반 메시지 제한

### [5. 메시지 요약 챗봇 (5-chatbot-summarization.ipynb)](5-chatbot-summarization.ipynb)
- LLM을 활용한 대화 요약 생성
- MemorySaver를 통한 세션 지속성
- 스레드 기반 대화 관리 시스템

### [6. 외부 메모리 챗봇 (6-chatbot-external-memory.ipynb)](6-chatbot-external-memory.ipynb)
- SQLite 데이터베이스 기반 영구 메모리
- SqliteSaver 체크포인터 활용
- 애플리케이션 재시작 후에도 지속되는 상태 관리

## 🎯 학습 목표

이 모듈을 완료하면 다음을 할 수 있습니다:
- 다양한 상태 스키마 유형과 활용법 이해
- 리듀서를 통한 고급 상태 관리 기법 숙지
- 메모리 효율적인 장기 대화 시스템 구축
- 외부 데이터베이스를 활용한 지속적 메모리 구현

## 🚀 시작하기

1. 상태 관리 기초를 위해 [`1-state-schema.ipynb`](1-state-schema.ipynb)부터 시작하세요
2. 각 노트북을 순서대로 진행하는 것을 권장합니다
3. `studio/` 디렉토리의 파일들은 LangGraph Studio에서 활용할 수 있습니다