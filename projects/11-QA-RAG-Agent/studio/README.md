# LangGraph QA RAG Agent

LangGraph를 활용한 고급 RAG(Retrieval Augmented Generation) 기반 질의응답 에이전트입니다. 벡터 스토어 검색, 웹 검색, 문서 필터링, 답변 검증 등의 기능을 통해 정확하고 근거 있는 답변을 제공합니다.

## 주요 기능

### 1. 지능형 라우팅
- 사용자 질문을 분석하여 벡터 스토어 검색 또는 일반 답변 생성으로 자동 라우팅
- LangGraph 및 RAG 관련 질문은 검색 파이프라인으로 전달

### 2. 질문 확장 및 재작성
- 사용자 질문을 코드 검색에 최적화된 형태로 자동 변환
- 의미적 의도를 파악하여 더 나은 검색 결과 도출

### 3. 하이브리드 검색
- **벡터 검색**: FAISS 기반 임베딩 검색
- **리랭킹**: Cohere Rerank를 통한 검색 결과 최적화
- **웹 검색**: Tavily를 활용한 실시간 웹 정보 수집

### 4. 문서 필터링
- 검색된 문서의 관련성을 자동으로 평가
- 불필요한 문서를 제거하여 답변 품질 향상

### 5. 답변 검증
- **Groundedness 체크**: 답변이 검색된 문서에 근거하는지 검증
- **관련성 체크**: 답변이 질문을 제대로 해결했는지 평가
- 검증 실패 시 자동으로 재검색 또는 질문 재작성

### 6. 출처 인용
- 모든 답변에 출처 문서 명시
- 신뢰할 수 있는 정보 제공

## 시스템 아키텍처

```
사용자 질문
    ↓
[라우팅 노드]
    ↓
┌─────────────┬──────────────┐
↓             ↓              ↓
일반 답변   질문 확장   질문 재작성
             ↓              ↓
        [문서 검색]      [RAG 답변]
             ↓              ↓
      [문서 필터링]   [답변 검증]
             ↓              ↓
    ┌────────┴────────┐    ↓
    ↓                 ↓    ↓
[웹 검색]      [RAG 답변]  종료
    ↓                 ↓
    └─────────────────┘
```

## 설치 및 설정

### 1. 환경 설정

```bash
# 가상환경 생성 (권장)
python -m venv .venv

# 가상환경 활성화
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. API 키 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 API 키를 입력하세요:

```bash
cp .env.example .env
```

`.env` 파일에 다음 API 키를 설정하세요:

- **OPENAI_API_KEY** (필수): [OpenAI Platform](https://platform.openai.com/api-keys)
- **LANGSMITH_API_KEY** (선택): [LangSmith](https://smith.langchain.com/)
- **COHERE_API_KEY** (필수): [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
- **TAVILY_API_KEY** (필수): [Tavily](https://tavily.com/)

### 3. 벡터 스토어 준비

벡터 스토어는 `../faiss_index` 경로에 있어야 합니다. FAISS 인덱스가 없다면 먼저 생성해야 합니다.

## 실행 방법

### LangGraph Studio에서 실행

```bash
# LangGraph Studio 실행
langgraph dev
```

브라우저에서 자동으로 열리는 Studio UI를 통해 그래프를 시각화하고 테스트할 수 있습니다.

### Python 스크립트로 실행

```python
from graph import graph

# 그래프 실행
result = graph.invoke({
    "messages": [{"role": "user", "content": "LangGraph에서 상태 관리는 어떻게 하나요?"}]
})

print(result["messages"][-1].content)
```

## 프로젝트 구조

```
studio/
├── graph.py          # 메인 그래프 정의
├── nodes.py          # 노드 구현 (검색, 필터링, 답변 생성 등)
├── states.py         # 상태 정의
├── tools.py          # 도구 정의 (웹 검색)
├── retrievers.py     # 리트리버 설정
├── requirements.txt  # 의존성 목록
├── langgraph.json   # LangGraph 설정
└── .env             # 환경 변수 (생성 필요)
```

## 주요 노드 설명

- **QueryRewriteNode**: 질문을 검색에 최적화된 형태로 재작성
- **RetrieveNode**: 벡터 스토어에서 관련 문서 검색
- **FilteringDocumentsNode**: 검색된 문서의 관련성 평가 및 필터링
- **WebSearchNode**: Tavily를 통한 웹 검색
- **RagAnswerNode**: 검색된 문서를 기반으로 답변 생성
- **GeneralAnswerNode**: 일반적인 질문에 대한 직접 답변

## 기술 스택

- **LangGraph**: 워크플로우 오케스트레이션
- **LangChain**: LLM 애플리케이션 프레임워크
- **OpenAI GPT-4o-mini**: 언어 모델
- **FAISS**: 벡터 검색
- **Cohere Rerank**: 검색 결과 리랭킹
- **Tavily**: 웹 검색
- **LangSmith**: 추적 및 모니터링 (선택)

## 라이센스

MIT

## 문의

문제가 발생하거나 질문이 있으시면 이슈를 등록해 주세요.