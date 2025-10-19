---
created: 2025-10-19 03:54:44
updated: 2025-10-19 03:54:44
tags:
  - AI_에이전트
  - Deep_Agents
  - LangGraph
  - 아키텍처
  - 튜토리얼
---
# Deep Agents From Scratch

"deep-agents-from-scratch"는 [[랭그래프/에이전트/에이전트란 무엇인가요?|LLM 기반 에이전트]] 개발에서 주목받고 있는 고급 아키텍처로, 복잡하고 장기적인 연구/코딩/분석 작업을 수행할 수 있게 설계된 오픈소스 패키지 및 프레임워크입니다. 직접 구현 과정을 살펴보고 관련 프로젝트와 학습 자원을 소개합니다.

### 소개 및 주요 개념

Deep Agents는 기존의 툴 호출 순환(Loop) 방식 에이전트보다 뛰어난 "플래닝", "컨텍스트 관리", "서브 에이전트 위임", "파일 시스템 연동" 등으로 복잡하고 다단계 작업을 수행합니다. 대표적인 예시로 LangGraph, Claude Code, Manus 등이 활용되며, 최근 `deepagents`, `deep_agents_from_scratch` 등 오픈소스 Python 패키지로 누구나 직접 구현할 수 있습니다.

### 오픈소스 및 설치 방법

- 주요 오픈소스:
  - [deep_agents_from_scratch (LangChain)](https://github.com/langchain-ai/deep_research_from_scratch)
  - [deepagents (LangChain)](https://github.com/langchain-ai/deepagents)

- 설치 예시(Python 3.11+, `uv`, `.env` 사용):

  ```shell
  git clone https://github.com/langchain-ai/deep_agents_from_scratch
  cd deep_agents_from_scratch
  uv sync
  touch .env  # API키 저장
  ```

- 주요 패키지: pip로 설치 가능

  ```shell
  pip install deepagents
  ```

### 구조 및 핵심 컴포넌트

- **상세 시스템 프롬프트**: 플래닝(할 일 작성), 리서치(인터넷 검색), 서브에이전트(특화 작업 위임), 파일시스템(메모/기록).
- **플래닝 툴 (예: todo_write)**: 에이전트가 포함할 작업 리스트를 생성하여 실행 흐름 전체에 계획을 노출.
- **컨텍스트 및 상태 저장**: 파일 시스템이나 가상 파일로 데이터를 기록/조회.
- **서브에이전트 위임**: 특정 작업은 별도 에이전트(예: 비판적 검토, 세부 리서치)에 위임.

### 실습 및 학습 자료

- 실습형 튜토리얼:
  - Datacamp: Deep Agents 개념/데모
  - LangGraph 기반 실전 구현
  - STEP별 상세 튜토리얼

- 영상 자료:
  - 유튜브: deepagents로 Deep Research 구조 직접 구축

### 맞춤형 구현 요령

- 필요한 툴(예: 검색, 요약, 문서화)과 프롬프트(명령/예시)를 직접 정의해 `create_deep_agent` 함수에 전달하면 쉽게 커스텀 딥 에이전트를 생성할 수 있습니다.

### 참고/활용 예시

| 프로젝트명                   | 설명                       | 주요 기술     | 링크                   |
|-----------------------------|----------------------------|--------------|------------------------|
| deep_agents_from_scratch    | 복수 단계 딥 에이전트 샘플 | LangGraph, Python | <https://github.com/langchain-ai/deep-agents-from-scratch> |
| deepagents                  | 커스텀 딥 에이전트          | LangChain, Python | <https://github.com/langchain-ai/deepagents> |
| deep_research_from_scratch  | 심층 리서치 에이전트 제작   | LangGraph, OpenAI 등 | <https://github.com/langchain-ai/deep_research_from_scratch> |
| Composio+LlamaIndex         | LlamaIndex 기반 리서치 에이전트 | LlamaIndex, ExaAI | <https://dev.to/composiodev/building-an-open-source-deep-research-agent-from-scratch-using-llamaindex-composio-exaai-4j9b> |

### 요약

Deep Agents는 LLM 도구를 이용해 복합적이고 장기적인 작업을 자동화하는 고급 에이전트 제작 패턴입니다. 다양한 오픈소스 패키지와 실습 자료, 튜토리얼을 활용하면 직접 구조를 이해하고 구현까지 할 수 있습니다.
