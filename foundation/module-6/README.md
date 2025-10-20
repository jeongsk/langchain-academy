# Module 6: LangGraph 서버 배포 및 연결

LangGraph로 구축한 그래프를 원격 서버로 배포하고, 클라이언트에서 해당 서버에 연결하여 사용하는 방법을 학습합니다.

## 📚 학습 내용

### [1. LangGraph 서버 생성 (1-creating.ipynb)](1-creating.ipynb)

- `langgraph` CLI를 사용하여 LangGraph 프로젝트를 패키징하는 방법
- FastAPI를 기반으로 LangGraph 그래프를 API 엔드포인트로 노출시키는 방법
- 원격에서 실행 가능한 서버를 구성하는 과정

### [2. LangGraph 서버에 연결 (2-connecting.ipynb)](2-connecting.ipynb)

- `RemoteRunnable`을 사용하여 원격 LangGraph 서버에 연결하는 방법
- 클라이언트 입장에서 서버의 그래프를 호출하고 스트리밍 응답을 처리하는 방법
- 원격 실행을 통해 분산된 환경에서 LangGraph를 활용하는 사례

### [3. 더블 텍스팅 처리 (3-double-texting.ipynb)](3-double-texting.ipynb)

- 사용자가 연속으로 메시지를 보낼 때 발생하는 더블 텍스팅(Double Texting) 상황 처리 방법
- 동시 실행 관리 전략: Reject(거부), Enqueue(큐에 추가), Interrupt(중단), Rollback(롤백)
- 각 전략의 특징과 실제 채팅 애플리케이션에서의 활용 방법

### [4. 어시스턴트 활용 (4-assistant.ipynb)](4-assistant.ipynb)

- LangGraph의 어시스턴트(Assistants) 개념과 설정 방법
- 그래프에 설정(configuration)을 제공하여 다양한 버전의 어시스턴트 생성하기
- 개인용/업무용 등 용도별로 구분된 어시스턴트를 만들고 관리하는 방법
- SDK를 사용한 어시스턴트 검색, 업데이트, 삭제 작업

## 🎯 학습 목표

이 모듈을 완료하면 다음을 할 수 있습니다:

- LangGraph 프로젝트를 독립적인 서버로 패키징하고 배포할 수 있습니다.
- `RemoteRunnable`을 사용하여 원격 그래프와 상호작용할 수 있습니다.
- 클라이언트-서버 아키텍처에서 LangGraph를 효과적으로 활용할 수 있습니다.

## 🚀 시작하기

1. LangGraph 서버를 만드는 방법을 배우기 위해 [`1-creating.ipynb`](1-creating.ipynb)부터 시작하세요.
2. 각 노트북을 순서대로 진행하며 서버 생성과 클라이언트 연결 과정을 학습하세요.
