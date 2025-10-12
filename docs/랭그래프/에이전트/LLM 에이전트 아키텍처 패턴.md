---
created: 2025-10-12 00:00:00
tags: [아키텍처, 에이전트, Plan-and-Execute, ReAct, Supervisor]
updated: 2025-10-12 12:21:44
---
## 개요

LLM 에이전트 시스템을 구축할 때 선택할 수 있는 여러 아키텍처 패턴이 있습니다. 각 패턴은 고유한 장점과 한계를 가지고 있으며, 사용 사례에 따라 적절한 패턴을 선택하는 것이 중요합니다.

## 주요 아키텍처 패턴

### 1. ReAct (Reasoning and Acting)

ReAct 패턴은 추론(Reasoning)과 행동(Acting)을 반복적으로 수행하는 에이전트 아키텍처입니다. LLM이 관찰, 사고, 행동의 순환을 통해 작업을 수행합니다.

**특징:**
- 각 단계에서 추론 과정을 명시적으로 표현
- 도구 사용과 추론이 통합된 루프 구조
- 동적이고 적응적인 문제 해결

### 2. Plan-and-Execute

Plan-and-Execute 패턴은 계획 수립과 실행을 분리하는 아키텍처입니다. 먼저 전체 작업 계획을 세운 후, 각 단계를 순차적으로 실행합니다.

**특징:**
- 명확한 계획 단계와 실행 단계 분리
- 구조화된 접근 방식
- 복잡한 작업을 하위 작업으로 분해

### 3. Supervisor (감독자)

Supervisor 아키텍처는 중앙 감독자 에이전트가 여러 작업자 에이전트를 조율하는 멀티 에이전트 시스템입니다. 감독자는 작업을 분배하고 결과를 통합합니다.

**특징:**
- 중앙집중식 제어 구조
- 여러 전문화된 에이전트 간 작업 분배
- 병렬 처리 가능
- 명확한 책임 분리

**LangGraph 지원:**
```bash
pip install -U langgraph-supervisor
```

## 아키텍처 비교 및 분석

Supervisor 아키텍처는 ReAct, Plan-and-Execute 방식과 함께 주요 LLM 에이전트 시스템 패턴 중 하나로 분류되며, 복잡한 작업을 분할·관리하는 구조적 장점과 한계를 분석한 자료가 있습니다.

### 참고 자료

- [LLM 에이전트 아키텍처 비교 - ReAct, Plan-and-Execute, Supervisor](https://syshin0116.github.io/AI/Agent-Architecture-Comparison)
  - 세 가지 주요 아키텍처 패턴의 상세 비교
  - 각 패턴의 장단점 분석
  - 실제 사용 사례 및 적용 시나리오

## 관련 문서

- [[에이전트란 무엇인가요?]]
- [[사전 구축된 에이전트로 빠르게 시작하기 - create_react_agent]]
