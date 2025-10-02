# Module 5: LangGraph 메모리 심화

LangGraph의 고급 메모리 관리 기법을 학습하는 모듈입니다. `BaseStore`를 활용한 메모리 저장소 커스터마이징부터 `StateSchema`를 이용한 복잡한 상태 관리까지 다룹니다.

## 📚 학습 내용

### [1. 메모리 저장소 (1-memory_store.ipynb)](1-memory_store.ipynb)
- `BaseStore` 인터페이스 이해 및 활용
- Redis를 이용한 원격 메모리 저장소 구축
- `MemorySaver`와 `BaseStore` 연동 방법

### [2. 메모리 스키마: 프로필 (2-memoryschema_profile.ipynb)](2-memoryschema_profile.ipynb)
- `StateSchema`를 활용한 상태 구조 정의
- 사용자 프로필과 같은 정적 정보 관리
- `at_leat_once` 필드를 이용한 상태 업데이트 보장

### [3. 메모리 스키마: 컬렉션 (3-memoryschema_collection.ipynb)](3-memoryschema_collection.ipynb)
- `StateSchema`를 이용한 동적 컬렉션(리스트) 관리
- 메시지 히스토리, 문서 목록 등 가변적인 데이터 처리
- `do_not_persist` 필드를 이용한 비영속성 상태 관리

### [4. 메모리 에이전트 (4-memory_agent.ipynb)](4-memory_agent.ipynb)
- `StateSchema`로 정의된 메모리 구조를 가진 에이전트 구축
- 복잡한 상태를 기반으로 동작하는 대화형 시스템 구현
- 영속성 있는 메모리를 활용한 개인화된 에이전트 개발

## 🎯 학습 목표

이 모듈을 완료하면 다음을 할 수 있습니다:
- `BaseStore`를 구현하여 원하는 저장소(Redis, DB 등)에 대화 상태를 저장
- `StateSchema`를 사용하여 복잡하고 구조화된 메모리 모델링
- 정적 데이터와 동적 데이터를 함께 관리하는 방법 숙지
- 개인화된 정보를 기억하고 활용하는 고급 에이전트 개발

## 🚀 시작하기

1. 각 노트북을 순서대로 진행하며 LangGraph의 고급 메모리 관리 기법을 익힙니다.
2. `studio/` 디렉토리의 파일들은 LangGraph Studio에서 활용할 수 있습니다.