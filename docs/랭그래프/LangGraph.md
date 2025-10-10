---
created: 2025-10-04 18:15:39
updated: 2025-10-10 23:47:02
---
[![버전](https://img.shields.io/pypi/v/langgraph.svg)](https://pypi.org/project/langgraph/)
[![다운로드](https://static.pepy.tech/badge/langgraph/month)](https://pepy.tech/project/langgraph)
[![오픈 이슈](https://img.shields.io/github/issues-raw/langchain-ai/langgraph)](https://github.com/langchain-ai/langgraph/issues)
[![문서](https://img.shields.io/badge/docs-latest-blue)](https://langchain-ai.github.io/langgraph/)

Klarna, Replit, Elastic 등 에이전트의 미래를 만들어가는 기업들의 신뢰를 받는 LangGraph는 오래 실행되는 상태 저장 에이전트를 구축, 관리, 배포하기 위한 로우-레벨 오케스트레이션 프레임워크입니다.

## 시작하기

LangGraph를 설치합니다:

```
pip install -U langgraph
```

그런 다음, [미리 빌드된 컴포넌트를 사용](https://langchain-ai.github.io/langgraph/agents/agents/)하여 에이전트를 생성합니다:

```python
# 모델을 호출하려면 `pip install -qU "langchain[anthropic]"` 명령어를 실행하세요.

from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """주어진 도시에 대한 날씨 정보를 가져옵니다."""
    return f"{city}는 항상 맑음입니다!"

agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt="당신은 도움이 되는 어시스턴트입니다"
)

# 에이전트 실행
agent.invoke(
    {"messages": [{"role": "user", "content": "sf의 날씨는 어떤가요"}]}
)
```

더 자세한 정보는 [빠른 시작](https://langchain-ai.github.io/langgraph/agents/agents/)을 참조하세요. 또는, 사용자 정의 가능한 아키텍처, 장기 메모리 및 기타 복잡한 작업 처리를 갖춘 [에이전트 워크플로우](https://langchain-ai.github.io/langgraph/concepts/low_level/)를 구축하는 방법을 배우려면 [LangGraph 기본 튜토리얼](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/)을 참조하세요.

## 핵심 이점

LangGraph는 오래 실행되는 모든 상태 저장 워크플로우나 에이전트를 위한 로우-레벨 지원 인프라를 제공합니다. LangGraph는 프롬프트나 아키텍처를 추상화하지 않으며, 다음과 같은 핵심적인 이점을 제공합니다:

- [내구성 있는 실행](https://langchain-ai.github.io/langgraph/concepts/durable_execution/): 실패에도 지속되고 장기간 실행될 수 있으며, 중단된 지점부터 정확히 자동 재개되는 에이전트를 구축합니다.
- [휴먼-인-더-루프](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/): 실행 중 어느 시점에서든 에이전트 상태를 검사하고 수정하여 원활하게 인간의 감독을 통합합니다.
- [포괄적인 메모리](https://langchain-ai.github.io/langgraph/concepts/memory/): 진행 중인 추론을 위한 단기 작업 메모리와 세션 간 장기 영구 메모리를 모두 갖춘 진정한 상태 저장 에이전트를 생성합니다.
- [LangSmith를 이용한 디버깅](http.www.langchain.com/langsmith): 실행 경로를 추적하고, 상태 전환을 캡처하며, 상세한 런타임 메트릭을 제공하는 시각화 도구를 통해 복잡한 에이전트 행동에 대한 깊은 가시성을 확보합니다.
- [프로덕션-레디 배포](https://langchain-ai.github.io/langgraph/concepts/deployment_options/): 상태를 저장하고 오래 실행되는 워크플로우의 고유한 과제를 처리하도록 설계된 확장 가능한 인프라를 통해 정교한 에이전트 시스템을 자신 있게 배포합니다.

## LangGraph 생태계

LangGraph는 단독으로 사용할 수도 있지만, 모든 LangChain 제품과 원활하게 통합되어 개발자에게 에이전트 구축을 위한 완전한 도구 모음을 제공합니다. LLM 애플리케이션 개발을 개선하려면 LangGraph를 다음과 함께 사용하세요:

- [LangSmith](http.www.langchain.com/langsmith) — 에이전트 평가 및 관찰 기능에 유용합니다. 성능이 저하된 LLM 앱 실행을 디버깅하고, 에이전트 궤적을 평가하며, 프로덕션 환경에서 가시성을 확보하고, 시간이 지남에 따라 성능을 개선합니다.
- [LangGraph 플랫폼](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/) — 오래 실행되는 상태 저장 워크플로우를 위해 특별히 제작된 배포 플랫폼을 사용하여 에이전트를 손쉽게 배포하고 확장할 수 있습니다. 팀 간에 에이전트를 발견, 재사용, 구성 및 공유하고, [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)의 시각적 프로토타이핑을 통해 빠르게 반복 작업을 수행할 수 있습니다.
- [LangChain](https://python.langchain.com/docs/introduction/) – LLM 애플리케이션 개발을 간소화하기 위한 통합 및 구성 가능한 컴포넌트를 제공합니다.

> [!NOTE]
> LangGraph의 JS 버전을 찾고 계신가요? [JS 리포지토리](https://github.com/langchain-ai/langgraphjs)와 [JS 문서](https://langchain-ai.github.io/langgraphjs/)를 참조하세요.

## 추가 자료

- [가이드](./guides/index): 스트리밍, 메모리 및 영속성 추가, 디자인 패턴(예: 분기, 서브그래프 등)과 같은 주제에 대한 빠르고 실행 가능한 코드 스니펫입니다.
- [레퍼런스](./reference/graphs): 핵심 클래스, 메서드, 그래프 및 체크포인팅 API 사용 방법, 그리고 더 높은 수준의 사전 빌드된 컴포넌트에 대한 상세한 레퍼런스입니다.
- [예제](https://langchain-ai.github.io/langgraph/examples/): LangGraph 시작에 대한 안내 예제입니다.
- [LangChain 포럼](https://forum.langchain.com/): 커뮤니티와 연결하여 모든 기술적인 질문, 아이디어, 피드백을 공유하세요.
- [LangChain 아카데미](https://academy.langchain.com/courses/intro-to-langgraph): 무료 구조화된 과정에서 LangGraph의 기본을 배우세요.
- [템플릿](https://langchain-ai.github.io/langgraph/concepts/template_applications/): 복제하고 적용할 수 있는 일반적인 에이전트 워크플로우(예: ReAct 에이전트, 메모리, 검색 등)를 위한 사전 빌드된 참조 앱입니다.
- [사례 연구](https://www.langchain.com/built-with-langgraph): 업계 리더들이 LangGraph를 사용하여 AI 애플리케이션을 대규모로 출시하는 방법을 들어보세요.

## 감사의 말

LangGraph는 [Pregel](https://research.google/pubs/pub37252/)과 [Apache Beam](https://beam.apache.org/)에서 영감을 받았습니다. 공개 인터페이스는 [NetworkX](https://networkx.org/documentation/latest/)에서 영감을 얻었습니다. LangGraph는 LangChain의 제작사인 LangChain Inc.에 의해 만들어졌지만, LangChain 없이도 사용할 수 있습니다.
