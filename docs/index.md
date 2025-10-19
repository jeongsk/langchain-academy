---
title: LangGraph Academy
created: 2025-10-10 22:00:53
updated: 2025-10-19 11:48:12
---

LangGraph로 AI 에이전트를 만드는 방법을 공부하고 있습니다. 생각보다 개념이 어렵지 않은데, 막상 실전에서 어떻게 활용할지 고민이 됩니다. 이 문서들은 공부하면서 이해한 내용과 삽질했던 경험들을 정리한 것입니다.

## 학습 내용

1. **LangGraph 입문** - 처음엔 그래프라는 개념이 낯설었는데, 노드와 엣지로 워크플로우를 표현한다는 것이 점점 이해가 되기 시작했습니다
2. **상태 관리와 메모리** - 에이전트가 대화 맥락을 기억하는 것이 생각보다 중요합니다
3. **Human-in-the-Loop** - AI가 모든 것을 자동으로 하는 것이 아니라, 필요할 때 사람이 개입할 수 있는 구조가 실무에서는 더 유용합니다
4. **고급 LangGraph 기술** - 병렬 처리 같은 최적화 기법들입니다. 아직 완벽히 이해하지 못한 부분도 있습니다
5. **LangGraph 메모리 심화** - 메모리 관리가 생각보다 복잡했습니다. 특히 장기 기억 부분이 그렇습니다
6. **LangGraph 서버 배포 및 연결** - 로컬에서 실행하는 것과 실제 서비스는 또 다른 이야기입니다

## 시작하기

- [Foundation Introduction to LangGraph](Foundation%20Introduction%20to%20LangGraph.md) - 여기서부터 시작했습니다
- [개발 환경 설정](개발%20환경%20설정.md) - 처음에 환경 설정하면서 헤맸던 부분들을 정리했습니다

## 참고 자료

- [랭그래프](랭그래프/LangGraph.md) - 공식 문서를 보면서 정리한 내용입니다
- [랭그래프 공식 문서 1.0 한국어 번역](https://langchain-docs.jeongsk.work/oss/python/langgraph/overview) - 한국어로 번역된 공식 문서입니다
- [프롬프트 엔지니어링](프롬프트%20엔지니어링/index.md) - 프롬프트를 잘 작성하는 것이 생각보다 중요합니다
- [Google 생성형 AI 기반 에이전트 가이드](https://www.kaggle.com/whitepaper-agents?utm_source=pytorchkr&ref=pytorchkr) - Google이 공개한 생성형 AI 기반 Agents 개요 및 구현 가이드입니다. (PDF, 영문 42p)
- [OpenAI, 에이전트 제작을 위한 실전 가이드](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) - OpenAI가 공개한 에이전트 제작 가이드입니다. (PDF, 영문 34p)
- [Anthropic의 다중 에이전트 연구 시스템](https://www.anthropic.com/engineering/multi-agent-research-system) - Anthropic의 다중 에이전트 연구 시스템에 대한 기술 블로그입니다.
- [Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems](https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/preview?tab=t.0#heading=h.pxcur8v2qagu) - Google CTO Office 수석 디렉터 Antonio Gulli의 LLM 시스템 접목 경험과 통찰을 담은 책입니다.
