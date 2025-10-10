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

## 🎯 학습 목표

이 모듈을 완료하면 다음을 할 수 있습니다:

- LangGraph 프로젝트를 독립적인 서버로 패키징하고 배포할 수 있습니다.
- `RemoteRunnable`을 사용하여 원격 그래프와 상호작용할 수 있습니다.
- 클라이언트-서버 아키텍처에서 LangGraph를 효과적으로 활용할 수 있습니다.

## 🚀 시작하기

1. LangGraph 서버를 만드는 방법을 배우기 위해 [`1-creating.ipynb`](1-creating.ipynb)부터 시작하세요.
2. 각 노트북을 순서대로 진행하며 서버 생성과 클라이언트 연결 과정을 학습하세요.
