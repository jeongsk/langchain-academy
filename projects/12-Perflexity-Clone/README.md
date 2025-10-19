# 12. Perplexity Clone

LangGraph 기반 Perplexity 스타일 검색 Agent 구현 프로젝트

## 프로젝트 개요

이 프로젝트는 [Perplexity](https://www.perplexity.ai/)와 유사한 웹 검색 기능을 갖춘 AI 어시스턴트를 LangGraph로 구현합니다. 사용자의 질문에 대해 웹 검색을 수행하고, 검색 결과를 기반으로 출처를 포함한 답변을 제공합니다.

## 주요 기능

- **웹 검색 통합**: Tavily API를 사용한 실시간 웹 검색
- **출처 표시**: 답변에 사용된 모든 출처를 번호와 함께 표시
- **멀티턴 대화**: 대화 히스토리를 유지하며 연속적인 질문 지원
- **도메인 필터링**: 특정 도메인 포함/제외 설정 가능
- **Streamlit UI**: 직관적인 웹 인터페이스 제공
- **LangGraph Studio**: 그래프 시각화 및 디버깅 지원

## 프로젝트 구조

```
12-Perplexity-Clone/
├── README.md              # 프로젝트 문서
├── app.py                 # Streamlit UI (로컬 모드)
├── app_remote.py          # Streamlit UI (원격 모드)
├── requirements.txt       # UI 의존성
├── .env                   # 환경 변수
├── .streamlit/            # Streamlit 설정
│   └── config.toml        # 테마 설정
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

## 모델 정보

이 프로젝트는 OpenAI의 GPT-4.1 시리즈 모델을 사용합니다.

### 사용 가능한 모델

| 모델 | 특징 | 권장 용도 |
|------|------|-----------|
| **gpt-4.1** | 가장 강력한 성능, 복잡한 추론 | 고품질 답변이 필요한 경우 |
| **gpt-4.1-mini** ⭐ | 빠른 속도, 비용 효율적 (기본값) | 일반적인 사용 |
| **gpt-4.1-nano** | 초경량, 초고속 응답 | 빠른 응답이 중요한 경우 |

### 기본 모델 변경 방법

**Streamlit UI에서:**
사이드바의 '🤖 모델 설정'에서 원하는 모델을 선택하세요.

**Python 코드에서:**

```python
graph = create_perplexity_graph(
    model_name="gpt-4.1",  # 또는 "gpt-4.1-mini", "gpt-4.1-nano"
    max_results=3
)
```

### 상태 스키마 (states.py)

```python
class PerplexityState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # 대화 메시지
    search_results: list[dict]  # 웹 검색 결과
    sources: list[str]          # 출처 URL
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

### 환경 설정

```bash
cd projects/12-Perflexity-Clone

# 환경 변수 설정
cp studio/.env.example .env
# .env 파일에 API 키 입력
```

`.env` 파일에 API 키를 입력하세요:

```bash
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key  # 선택사항
```

### 실행 방법

#### 방법 1: Streamlit UI (로컬 모드) ⭐ 추천

그래프를 직접 로드하여 실행하는 가장 간단한 방법입니다.

```bash
# 패키지 설치
uv pip install -r requirements.txt

# Streamlit 실행
uv run streamlit run app.py
```

브라우저에서 <http://localhost:8501> 열기

**특징:**

- 올인원 방식 (UI + 그래프)
- 설정 변경 즉시 반영
- 로컬 개발에 최적

**사용 방법:**

1. 사이드바에서 모델, 검색 설정, 도메인 필터링 구성
2. '✅ 설정 적용' 버튼 클릭
3. 하단 입력창에 질문 입력
4. AI가 웹 검색하여 출처와 함께 답변 제공

#### 방법 2: Streamlit UI (원격 모드)

LangGraph Studio 서버와 통신하는 방식입니다.

**1단계: LangGraph Studio 서버 실행**

```bash
cd studio
langgraph dev
```

**2단계: Streamlit UI 실행 (새 터미널)**

```bash
cd ..  # 프로젝트 루트로
uv run streamlit run app_remote.py
```

**특징:**

- UI와 그래프 로직 분리
- LangGraph Studio에서 디버깅 가능
- 프로덕션 환경에 적합
- 여러 클라이언트가 동일 그래프 사용 가능

#### 방법 3: LangGraph Studio UI

순수 LangGraph Studio로 테스트하는 방법입니다.

```bash
cd studio
langgraph dev
```

Studio UI에서 그래프를 시각화하고 테스트:

- API: <http://127.0.0.1:2024>
- Studio UI: <https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024>

**특징:**

- 그래프 구조 시각화
- 단계별 실행 및 디버깅
- 상태 검사 가능

#### 방법 4: Python 코드로 직접 실행

```python
from studio.graph import create_perplexity_graph

# 그래프 생성
graph = create_perplexity_graph(
    model_name="gpt-4.1-mini",
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

## 사용 예시

### 기본 질문

```
사용자: "2024년 AI 트렌드는 무엇인가요?"

AI: [웹 검색 실행...]

최근 2024년 AI 트렌드는 다음과 같습니다:

1. **생성형 AI의 발전**: GPT-4, Claude 등 대규모 언어 모델이 더욱 발전...
2. **멀티모달 AI**: 텍스트, 이미지, 음성을 통합적으로 처리...
3. **AI 에이전트**: 자율적으로 작업을 수행하는 AI 에이전트...

**출처**

[1] https://www.example.com/ai-trends-2024
[2] https://www.techreview.com/2024/ai-overview
```

### 도메인 필터링

```python
# GitHub과 Python.org만 검색
graph = create_perplexity_graph(
    include_domains=["github.com", "python.org"]
)

# Wikipedia 제외
graph = create_perplexity_graph(
    exclude_domains=["wikipedia.org"]
)
```

### 멀티턴 대화

```
사용자: "LangGraph가 뭐야?"
AI: [LangGraph에 대한 설명...]

사용자: "그럼 LangChain과의 차이는?"  # 이전 대화 컨텍스트 유지
AI: [차이점 설명...]
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

## Streamlit UI 특징

### 로컬 모드 (app.py)

- **설정 UI**: 사이드바에서 모델, 검색 설정, 도메인 필터링 구성
- **실시간 적용**: 설정 변경 시 즉시 그래프 재생성
- **대화 기록**: 세션 상태로 대화 히스토리 관리
- **검색 상태**: 웹 검색 실행 시 상태 표시
- **커스텀 테마**: Perplexity 스타일 색상 테마

### 원격 모드 (app_remote.py)

- **서버 연결**: LangGraph Studio 서버 URL 설정
- **그래프 조회**: 사용 가능한 그래프 목록 확인
- **스레드 관리**: Thread ID 기반 세션 관리
- **디버깅**: Studio UI에서 실시간 디버깅 가능

## 원본 프로젝트와의 차이점

### 원본 (Streamlit 기반)

- `create_react_agent` 사용 (추상화된 Agent)
- Streamlit UI로 실시간 스트리밍
- 커스텀 핸들러로 UI 업데이트
- 단일 파일 구조

### 재구성 (LangGraph 기반)

- 명시적 그래프 구조 (`StateGraph`)
- 각 노드와 엣지를 직접 정의
- LangGraph Studio로 시각화 및 디버깅
- 모듈화된 구조 (states, tools, nodes, graph)
- 로컬/원격 모드 지원
- Python 3.12+ 최신 타입 힌팅

## 확장 아이디어

1. **RAG 통합**: 벡터 DB에서 문서 검색 추가
2. **멀티 소스**: Wikipedia, arXiv 등 추가 검색 소스
3. **스트리밍 응답**: 실시간 토큰 스트리밍 구현
4. **검색 결과 필터링**: 신뢰도 점수 기반 필터링
5. **Human-in-the-loop**: 검색 결과 확인 후 진행
6. **대화 내보내기**: 대화 기록 저장/불러오기
7. **음성 입력**: 음성을 텍스트로 변환하여 질문

## 트러블슈팅

### API 키 오류

```
Error: Invalid API key
```

→ `.env` 파일에 올바른 API 키가 입력되었는지 확인

### 그래프 초기화 오류

```
Warning: 먼저 사이드바에서 설정을 완료해주세요
```

→ 사이드바에서 '✅ 설정 적용' 버튼 클릭

### 원격 모드 연결 오류

```
Error: 서버 연결 실패
```

→ `langgraph dev` 명령으로 서버가 실행 중인지 확인
→ 서버 URL이 올바른지 확인 (기본: <http://127.0.0.1:2024>)

## Tavily 검색 도구 업데이트 (2025년 10월)

### 변경 사항

`langchain_community.tools.tavily_search` (deprecated) → `langchain-tavily` (권장)

### 주요 개선 사항

1. **최신 기능 지원**: Search와 Extract API 모두 지원
2. **지속적인 업데이트**: 공식 Tavily 통합 패키지
3. **향상된 파라미터**:
   - `search_depth`: "basic" 또는 "advanced"
   - `time_range`: "day", "week", "month", "year"
   - `start_date`, `end_date`: 날짜 범위 필터링
   - `include_answer`: 즉시 답변 제공
   - `include_raw_content`: 원본 HTML 포함
   - `include_images`: 이미지 검색 결과 포함

### 마이그레이션 방법

**이전 (deprecated):**

```python
from langchain_community.tools.tavily_search import TavilySearchResults

tool = TavilySearchResults(
    max_results=3,
    include_domains=["github.com"]
)
```

**현재 (권장):**

```python
from langchain_tavily import TavilySearch

tool = TavilySearch(
    max_results=3,
    include_domains=["github.com"],
    search_depth="basic",  # 새로운 옵션
    include_answer=False,  # 새로운 옵션
)
```

### 동적 파라미터 조정

호출 시 파라미터를 동적으로 변경할 수 있습니다:

```python
# 도구 생성
tool = TavilySearch(max_results=3, topic="general")

# 호출 시 파라미터 변경
result = tool.invoke({
    "query": "LangGraph tutorial",
    "include_domains": ["github.com"],  # 동적 설정
    "search_depth": "advanced"           # 동적 설정
})
```

### 패키지 설치

```bash
# 이전 패키지 제거 (선택사항)
pip uninstall tavily-python

# 새 패키지 설치
pip install -U langchain-tavily
```

## 참고 자료

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [Tavily Search API](https://tavily.com/)
- [Perplexity AI](https://www.perplexity.ai/)
- [Streamlit 문서](https://docs.streamlit.io/)
- [원본 프로젝트](https://github.com/teddylee777/fastcampus-perplexity-clone)

## 라이선스

Apache 2.0
