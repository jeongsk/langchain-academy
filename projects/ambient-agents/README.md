# Project: Ambient Agents with LangGraph

## 소개

Ambient Agents 프로젝트 시리즈에 오신 것을 환영합니다!

LangChain Academy는 LangGraph를 활용한 앰비언트 에이전트 구축 과정을 선보입니다. LangChain의 목표는 에이전트 애플리케이션 구축을 최대한 용이하게 하는 것이며, **모델의 발전과 함께 에이전트의 상호 작용 방식도 변화하고 있습니다.** 과거에는 대부분 채팅 인터페이스를 통해 한 번에 하나의 상호 작용을 처리했지만, AI의 자율 수행 능력은 7개월마다 두 배로 증가하고 있습니다.

이러한 확장된 모델 기능은 새로운 종류의 에이전트 상호 작용을 가능하게 합니다. 이제 에이전트는 Slack 메시지나 GitHub 이슈와 같은 **이벤트 스트림에 의해 자율적으로 트리거될 수 있으며**, 백그라운드에서 장기간 여러 작업을 수행할 수 있게 되었습니다. 즉각적인 사용자 응답이 필요한 채팅 에이전트와 달리, 앰비언트 에이전트는 장기 실행되는 복잡한 작업을 위해 설계되었습니다.

각 프로젝트는 실제 사용 사례를 바탕으로 구성되어 있으며, Foundation 과정에서 학습한 개념들을 실무에 적용하는 방법을 배웁니다. 모든 프로젝트에는 상세한 노트북과 LangGraph Studio 통합이 포함되어 있습니다.

## Ambient Agents란?

**Ambient Agents**는 사용자의 환경과 맥락을 이해하고, 지속적으로 상태를 추적하며, 필요한 시점에 적절한 행동을 취하는 지능형 에이전트를 의미합니다.

### 핵심 특징

- **맥락 인식**: 사용자의 현재 상황과 과거 이력을 이해합니다
- **상태 유지**: 대화 및 작업 상태를 지속적으로 관리합니다
- **능동적 행동**: 필요시 스스로 판단하여 행동합니다
- **적응성**: 환경 변화에 따라 동적으로 대응합니다

### 확장성과 영향력

앰비언트 에이전트를 사용하면 **영향력을 크게 확장하여 수천 개의 에이전트를 백그라운드에서 실행하며 복잡한 워크플로우를 자동화하고 오케스트레이션할 수 있습니다.** 중요한 것은 '앰비언트'가 완전 자율을 의미하지 않는다는 점입니다. 루프에 사람이 개입하는 것이 중요합니다. 이는 작업을 승인하거나 거부하고, 도구 호출을 편집하고, 질문에 답변하며, 에이전트의 상태를 수정하는 등의 형태로 이루어집니다.

이러한 **인간-에이전트 상호 작용은 결과의 품질과 신뢰도를 높이고, 시간이 지남에 따라 에이전트의 메모리 및 성능을 향상시키는 데 기여합니다.**

### LangGraph 플랫폼의 역할

LangGraph는 이러한 요구 사항을 염두에 두고 설계된 에이전트 오케스트레이션 프레임워크입니다:

- **지속성 레이어**: 사용자가 에이전트 상태를 쉽게 보고, 다시 방문하고, 수정할 수 있도록 하는 'Human-in-the-loop' 상호 작용 패턴을 지원합니다
- **확장 가능한 인프라**: 장기 실행 또는 버스트 워크로드에 이상적인 에이전트를 대규모로 실행할 수 있는 인프라를 제공합니다
- **모니터링 및 개선**: LangSmith는 관찰 가능성, 평가 및 프롬프트 엔지니어링을 위한 플랫폼을 제공하여 장기 실행 에이전트를 모니터링하고 개선하는 데 효과적입니다

## 학습 목표

### 과정 개요

이 과정에서는 **이메일 관리를 위한 자체 앰비언트 에이전트를 구축하는 단계를 안내합니다.** 이메일 관리는 거의 보편적이지만 많은 사람들이 자동화하고 싶어하는 작업입니다. 학습자들은 LangGraph의 기본 사항을 익히고 이를 사용하여 이메일 에이전트를 구축하게 됩니다.

### 핵심 학습 내용

이 프로젝트 시리즈를 통해 다음을 달성할 수 있습니다:

1. **기본 에이전트 구축**
   - LangGraph를 사용한 이메일 관리 에이전트 구현
   - 복잡한 상태를 관리하는 에이전트 설계 및 구현
   - 실시간 맥락을 추적하고 활용하는 시스템 구축

2. **평가 및 모니터링**
   - LangSmith를 사용하여 에이전트를 평가하는 방법 학습
   - 장기 실행 에이전트의 성능 모니터링 및 개선

3. **Human-in-the-loop 통합**
   - 이메일 보내기와 같은 민감한 작업을 승인하기 위한 'Human-in-the-loop' 기능 추가
   - 사용자 경험을 개선하는 워크플로우 구현

4. **메모리 및 적응성**
   - 에이전트가 시간이 지남에 따라 피드백을 기억하고 적응할 수 있도록 메모리 통합
   - 지속적인 학습을 통한 성능 향상

5. **배포 및 프로덕션**
   - LangGraph 플랫폼을 사용하여 에이전트 배포
   - 프로덕션 수준의 에이전트 시스템 운영

### 과정 완료 후

이 과정을 마치면:
- 작동하는 이메일 에이전트를 갖게 되며
- 광범위한 실제 작업에 대한 앰비언트 에이전트를 구축하고 배포할 수 있는 역량을 갖추게 됩니다

## 선수 지식

이 프로젝트 시리즈를 시작하기 전에 다음 내용을 이해하고 있는 것을 권장합니다:

### 필수
- [Foundation Module 1-2](../../langgraph-foundation/module-1/README.md): LangGraph 기초 및 상태 관리
- Python 프로그래밍 기본
- LLM API 사용 경험 (OpenAI 등)

### 권장
- [Foundation Module 3-4](../../langgraph-foundation/module-3/README.md): Human-in-the-loop 및 고급 패턴
- [Foundation Module 5-6](../../langgraph-foundation/module-5/README.md): 메모리 관리 및 배포

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

- **[Tutorial](../../langgraph-tutorial/README.md)**: 다양한 고급 패턴 및 예제 탐구
- 자신만의 Ambient Agent 프로젝트 구축
- LangGraph 커뮤니티에 기여

## 리소스

### 공식 강의
- [LangChain Academy - Ambient Agents 강의실](https://academy.langchain.com/courses/take/ambient-agents/lessons/66147171-course-overview)

### 문서 및 플랫폼
- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [GitHub 저장소](https://github.com/langchain-ai)
