# 12. Perplexity Clone

LangGraph 기반 Perplexity 스타일 검색 Agent 구현 프로젝트

## 프로젝트 개요

이 프로젝트는 [Perplexity](https://www.perplexity.ai/)와 유사한 웹 검색 기능을 갖춘 AI 어시스턴트를 LangGraph로 구현합니다. 사용자의 질문에 대해 웹 검색을 수행하고, 검색 결과를 기반으로 출처를 포함한 답변을 제공합니다.

## 주요 기능

- **웹 검색 통합**: Tavily API를 사용한 실시간 웹 검색
- **출처 표시**: 답변에 사용된 모든 출처를 번호와 함께 표시
- **멀티턴 대화**: 대화 히스토리를 유지하며 연속적인 질문 지원
- **도메인 필터링**: 특정 도메인 포함/제외 설정 가능
- **LangGraph Studio**: 그래프 시각화 및 디버깅 지원

## 프로젝트 구조

```
12-Perflexity-Clone/
├── README.md              # 프로젝트 문서
├── Perflexity-Clone.ipynb # Jupyter 노트북
└── studio/                # LangGraph Studio 프로젝트
    ├── langgraph.json     # Studio 설정
    ├── requirements.txt   # Python 패키지 의존성
    ├── .env.example       # 환경 변수 템플릿
    ├── states.py          # 상태 스키마 정의
    ├── tools.py           # 웹 검색 도구
    ├── nodes.py           # 그래프 노드 구현
    └── graph.py           # 메인 그래프 정의
```

## 아키텍처

### 상태 스키마 (states.py)

```python
class PerplexityState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]  # 대화 메시지
    search_results: List[dict]  # 웹 검색 결과
    sources: List[str]          # 출처 URL
```

### 그래프 플로우

```
START → agent → [검색 필요?]
                  ├─ Yes → search → agent → ...
                  └─ No  → END
```

1. **agent 노드**: LLM이 질문을 분석하고 검색 필요 여부 결정
2. **search 노드**: Tavily API로 웹 검색 수행
3. **조건부 분기**: 추가 검색 필요 시 반복, 아니면 종료

## 설치 및 실행

### 1. 환경 설정

```bash
cd projects/12-Perplexity-Clone/studio
cp .env.example .env
```

`.env` 파일에 API 키를 입력하세요:
```bash
OPENAI_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

### 2. LangGraph Studio 실행

```bash
cd studio
langgraph dev
```

Studio UI에서 그래프를 시각화하고 테스트할 수 있습니다:
- API: http://127.0.0.1:2024
- Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

### 3. Jupyter 노트북 실행

```bash
# 프로젝트 루트에서
uv run jupyter notebook
```

`Perflexity-Clone.ipynb` 노트북을 열어 실습을 진행하세요.

## 사용 예시

### Python 코드로 실행

```python
from studio.graph import create_perplexity_graph

# 그래프 생성
graph = create_perplexity_graph(
    model_name="gpt-4o",
    max_results=3,
    topic="general"
)

# 실행
config = {"configurable": {"thread_id": "user-session-1"}}
response = graph.invoke(
    {"messages": [("user", "2024년 AI 트렌드는?")]},
    config=config
)

print(response["messages"][-1].content)
```

### 도메인 필터링

```python
# 특정 도메인만 검색
graph = create_perplexity_graph(
    include_domains=["github.com", "python.org"]
)

# 특정 도메인 제외
graph = create_perplexity_graph(
    exclude_domains=["wikipedia.org"]
)
```

## 핵심 개념

### 1. ReAct 패턴
Agent가 추론(Reasoning)과 행동(Acting)을 반복하며 문제를 해결합니다:
- **추론**: "이 질문에 답하려면 최신 정보가 필요하다"
- **행동**: 웹 검색 도구 실행
- **관찰**: 검색 결과 확인
- **답변**: 수집한 정보를 바탕으로 응답 생성

### 2. 도구 호출 (Tool Calling)
LLM이 함수 호출 형식으로 도구 사용을 결정:
```json
{
  "name": "web_search",
  "arguments": {
    "query": "LangGraph tutorial 2024"
  }
}
```

### 3. 체크포인팅 (Checkpointing)
SQLite를 사용한 대화 상태 저장으로 멀티턴 대화 지원:
- 각 `thread_id`별로 대화 히스토리 유지
- 이전 대화 컨텍스트를 활용한 연속 질문 가능

## 원본 프로젝트와의 차이점

**원본 (Streamlit 기반)**
- `create_react_agent` 사용 (추상화된 Agent)
- Streamlit UI로 실시간 스트리밍
- 커스텀 핸들러로 UI 업데이트

**재구성 (LangGraph 기반)**
- 명시적 그래프 구조 (`StateGraph`)
- 각 노드와 엣지를 직접 정의
- LangGraph Studio로 시각화 및 디버깅
- 모듈화된 구조 (states, tools, nodes, graph)

## 확장 아이디어

1. **RAG 통합**: 벡터 DB에서 문서 검색 추가
2. **멀티 소스**: Wikipedia, arXiv 등 추가 검색 소스
3. **스트리밍 응답**: 실시간 토큰 스트리밍 구현
4. **검색 결과 필터링**: 신뢰도 점수 기반 필터링
5. **Human-in-the-loop**: 검색 결과 확인 후 진행

## 참고 자료

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [Tavily Search API](https://tavily.com/)
- [Perplexity AI](https://www.perplexity.ai/)
- [원본 프로젝트](https://github.com/teddylee777/fastcampus-perplexity-clone)

## 라이선스

Apache 2.0