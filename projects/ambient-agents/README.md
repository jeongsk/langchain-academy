# Project: Ambient Agents with LangGraph

## 소개

Ambient Agents 프로젝트 시리즈에 오신 것을 환영합니다! 이 과정은 LangGraph를 활용하여 실전 프로젝트를 구현하며 학습하는 프로젝트 중심 실습 과정입니다.

각 프로젝트는 실제 사용 사례를 바탕으로 구성되어 있으며, Foundation 과정에서 학습한 개념들을 실무에 적용하는 방법을 배웁니다. 모든 프로젝트에는 상세한 노트북과 LangGraph Studio 통합이 포함되어 있습니다.

## Ambient Agents란?

**Ambient Agents**는 사용자의 환경과 맥락을 이해하고, 지속적으로 상태를 추적하며, 필요한 시점에 적절한 행동을 취하는 지능형 에이전트를 의미합니다. 이러한 에이전트는:

- **맥락 인식**: 사용자의 현재 상황과 과거 이력을 이해합니다
- **상태 유지**: 대화 및 작업 상태를 지속적으로 관리합니다
- **능동적 행동**: 필요시 스스로 판단하여 행동합니다
- **적응성**: 환경 변화에 따라 동적으로 대응합니다

## 학습 목표

이 프로젝트 시리즈를 통해 다음을 달성할 수 있습니다:

- 복잡한 상태를 관리하는 에이전트 설계 및 구현
- 실시간 맥락을 추적하고 활용하는 시스템 구축
- 다중 에이전트 협업 패턴 적용
- Human-in-the-loop 워크플로우를 통한 사용자 경험 개선
- 프로덕션 수준의 에이전트 시스템 배포

## 선수 지식

이 프로젝트 시리즈를 시작하기 전에 다음 내용을 이해하고 있는 것을 권장합니다:

### 필수
- [Foundation Module 1-2](../foundation/module-1/README.md): LangGraph 기초 및 상태 관리
- Python 프로그래밍 기본
- LLM API 사용 경험 (OpenAI 등)

### 권장
- [Foundation Module 3-4](../foundation/module-3/README.md): Human-in-the-loop 및 고급 패턴
- [Foundation Module 5-6](../foundation/module-5/README.md): 메모리 관리 및 배포

## 프로젝트 구성

### [Project 1: [프로젝트 제목]](./project-1/README.md)

[프로젝트 1의 개요 및 주요 학습 내용]

**주요 내용:**
- [핵심 개념 1]
- [핵심 개념 2]
- [핵심 개념 3]

### [Project 2: [프로젝트 제목]](./project-2/README.md)

[프로젝트 2의 개요 및 주요 학습 내용]

**주요 내용:**
- [핵심 개념 1]
- [핵심 개념 2]
- [핵심 개념 3]

### [Project 3: [프로젝트 제목]](./project-3/README.md)

[프로젝트 3의 개요 및 주요 학습 내용]

**주요 내용:**
- [핵심 개념 1]
- [핵심 개념 2]
- [핵심 개념 3]

## 환경 설정

### Python 버전

Python 3.12 이상을 사용하는 것을 권장합니다.

```bash
python3 --version
```

### 의존성 설치

프로젝트 루트에서 다음 명령을 실행하세요:

```bash
# uv를 사용하여 환경 동기화
uv sync

# 또는 가상환경 활성화 후 사용
source .venv/bin/activate
```

### API 키 설정

각 프로젝트의 studio 디렉토리에 `.env` 파일을 생성해야 합니다:

```bash
# 모든 프로젝트의 .env 파일 생성 (예시)
for i in {1..6}; do
  cp ambient-agents/project-$i/studio/.env.example ambient-agents/project-$i/studio/.env
  echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > ambient-agents/project-$i/studio/.env
done
```

필요한 API 키:
- `OPENAI_API_KEY`: OpenAI API 사용 ([가입하기](https://openai.com/))
- `LANGSMITH_API_KEY`: LangSmith 추적 ([가입하기](https://smith.langchain.com/))

## LangGraph Studio 사용하기

각 프로젝트는 LangGraph Studio와 통합되어 있어, 그래프를 시각적으로 탐색하고 테스트할 수 있습니다.

### Studio 시작하기

```bash
cd ambient-agents/project-1/studio/
langgraph dev
```

브라우저에서 다음 URL로 접속:
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 🚀 API: http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

## 학습 경로

1. **Project 1-2**: 기본 Ambient Agent 패턴 익히기
2. **Project 3-4**: 복잡한 상태 관리 및 멀티 에이전트
3. **Project 5-6**: 고급 기능 및 프로덕션 배포

## 다음 단계

프로젝트를 완료한 후에는:

- **[Tutorial](../tutorial/README.md)**: 다양한 고급 패턴 및 예제 탐구
- 자신만의 Ambient Agent 프로젝트 구축
- LangGraph 커뮤니티에 기여

## 리소스

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [GitHub 저장소](https://github.com/langchain-ai)
