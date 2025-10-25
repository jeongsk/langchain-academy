---
title: 3. 프롬프트 엔지니어링
created: 2025-10-07 22:06:23
updated: 2025-10-25 21:16:13
tags:
  - 컨텍스트_엔지니어링
  - 프롬프트_엔지니어링
  - AI_에이전트
  - MOC
---

[[에이전트란 무엇인가요?|AI 에이전트]]를 위한 효과적인 프롬프트 엔지니어링 기법을 학습하는 섹션입니다.

## 개요

프롬프트 엔지니어링은 AI 모델과 효과적으로 소통하기 위한 핵심 기술입니다. 특히 [[LangGraph|LangGraph]]와 같은 에이전트 시스템에서는 더욱 중요한 역할을 합니다.

## 주요 내용

### 컨텍스트 엔지니어링
- [[컨텍스트 엔지니어링의 부상|컨텍스트 엔지니어링의 부상]] - 프롬프트 엔지니어링에서 컨텍스트 엔지니어링으로의 진화
- [[에이전트를 위한 효과적인 컨텍스트 엔지니어링|에이전트를 위한 효과적인 컨텍스트 엔지니어링]] - 주의력 예산, 압축, 적시 검색 전략

### 에이전트 설계
- [[효과적인 AI 에이전트 구축하기|효과적인 AI 에이전트 구축하기]] - Anthropic의 에이전트 구축 베스트 프랙티스
  - 워크플로우와 에이전트 구분
  - 5가지 워크플로우 패턴 (프롬프트 체이닝, 라우팅, 병렬화, 조율자-작업자, 평가자-최적화자)
  - 도구 설계 및 ACI(에이전트-컴퓨터 인터페이스) 원칙
  - 실무 적용 사례

### 프롬프트 최적화
- [[모델이 프롬프트를 작성하게 하라|모델이 프롬프트를 작성하게 하라]] - AI를 활용한 프롬프트 자동 생성

## 관련 리소스

### LangGraph 에이전트 패턴
- [[워크플로우와 에이전트 패턴|워크플로우와 에이전트 패턴]] - LangGraph에서의 구현 방법
- [[에이전트 아키텍처 개념|에이전트 아키텍처 개념]] - 다양한 아키텍처 패턴
- [[멀티 에이전트 시스템|멀티 에이전트 시스템]] - 조율자-작업자 및 슈퍼바이저 패턴

### 외부 리소스
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.claude.com/ko/docs/build-with-claude/prompt-engineering/overview)
- [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
