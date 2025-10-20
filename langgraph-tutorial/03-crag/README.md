# CRAG (Corrective RAG)

## 개요

Corrective RAG(CRAG) 패턴을 LangGraph로 구현하는 프로젝트입니다. 검색된 문서의 품질을 평가하고, 필요시 웹 검색을 통해 보완하여 답변의 정확도를 높이는 시스템을 구축합니다.

## 주요 내용

- Corrective RAG 패턴의 이해
- 문서 관련성 평가 메커니즘
- 웹 검색 폴백 전략
- 검색 결과 재순위화(Reranking)
- LangGraph를 활용한 동적 검색 워크플로우

## 노트북

- [03-CRAG.ipynb](./03-CRAG.ipynb): CRAG 시스템 구현

## 학습 목표

- RAG의 한계와 CRAG의 개선 방법 이해
- 검색 품질 평가 및 보정 기법 습득
- 동적 검색 워크플로우 설계 능력 향상
