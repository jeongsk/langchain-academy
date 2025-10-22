---
title: Tavily Search & Extract - LangChain 통합 가이드
created: 2025-10-18 09:04:21
updated: 2025-10-18 09:08:03
tags:
  - LangChain
  - LangGraph
  - Tavily
  - 웹검색
  - API
  - 에이전트
  - RAG
  - Python
  - 튜토리얼
---
> [!warning] **경고**
> [`langchain_community.tools.tavily_search.tool`](https://python.langchain.com/integrations/tools/tavily_search/)은 더 이상 권장되지 않습니다. 현재는 여전히 작동하지만, [Search](https://docs.tavily.com/documentation/integrations/#tavily-search)와 [Extract](https://docs.tavily.com/documentation/integrations/#tavily-extract) 기능을 모두 지원하고 최신 기능으로 지속적으로 업데이트되는 새로운 `langchain-tavily` Python 패키지로 마이그레이션할 것을 강력히 권장합니다.

[langchain-tavily](https://pypi.org/project/langchain-tavily/) Python 패키지는 [[LangGraph|LangGraph]] 및 LangChain [[에이전트란 무엇인가요?|에이전트]]에서 사용할 수 있는 [TavilySearch](https://docs.tavily.com/documentation/integrations/#tavily-search)와 [TavilyExtract](https://docs.tavily.com/documentation/integrations/#tavily-extract)를 모두 포함하는 Tavily의 공식 통합 패키지입니다.

## 설치

```
pip install -U langchain-tavily
```

### 인증 정보

Tavily API 키를 설정해야 합니다. [이 사이트](https://app.tavily.com/sign-in)를 방문하여 계정을 생성하면 API 키를 받을 수 있습니다.

```python
import getpass
import os

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")
```

여기서는 Tavily 검색 도구의 인스턴스를 생성하는 방법을 보여줍니다. 이 도구는 검색을 커스터마이징할 수 있는 다양한 매개변수를 받습니다. 인스턴스를 생성한 후 간단한 쿼리로 도구를 호출합니다. 이 도구를 사용하면 Tavily의 Search API 엔드포인트를 통해 검색 쿼리를 수행할 수 있습니다.

### 인스턴스 생성

도구는 인스턴스 생성 시 다양한 매개변수를 받습니다:

- `max_results` (선택, int): 반환할 검색 결과의 최대 개수. 기본값은 5입니다.
- `topic` (선택, str): 검색 카테고리. "general", "news", "finance" 중 하나를 선택할 수 있습니다. 기본값은 "general"입니다.
- `include_answer` (선택, bool): 결과에 원본 쿼리에 대한 답변을 포함합니다. 기본값은 False입니다.
- `include_raw_content` (선택, bool): 각 검색 결과의 정제되고 파싱된 HTML을 포함합니다. 기본값은 False입니다.
- `include_images` (선택, bool): 응답에 쿼리 관련 이미지 목록을 포함합니다. 기본값은 False입니다.
- `include_image_descriptions` (선택, bool): 각 이미지에 대한 설명 텍스트를 포함합니다. 기본값은 False입니다.
- `search_depth` (선택, str): 검색의 깊이. "basic" 또는 "advanced" 중 하나입니다. 기본값은 "basic"입니다.
- `time_range` (선택, str): 현재 날짜로부터 거슬러 올라가는 시간 범위(게시 날짜 기준)로 결과를 필터링합니다 - "day", "week", "month", "year" 중 하나입니다. 기본값은 None입니다.
- `start_date` (선택, str): 지정된 시작 날짜(게시 날짜) 이후의 모든 결과를 반환합니다. YYYY-MM-DD 형식으로 작성해야 합니다. 기본값은 None입니다.
- `end_date` (선택, str): 지정된 종료 날짜 이전의 모든 결과를 반환합니다. YYYY-MM-DD 형식으로 작성해야 합니다. 기본값은 None입니다.
- `include_domains` (선택, List\[str\]): 특정 도메인만 포함하는 도메인 목록. 최대 300개 도메인. 기본값은 None입니다.
- `exclude_domains` (선택, List\[str\]): 특정 도메인을 제외하는 도메인 목록. 최대 150개 도메인. 기본값은 None입니다.

사용 가능한 매개변수에 대한 포괄적인 개요는 [Tavily Search API 문서](https://docs.tavily.com/documentation/api-reference/endpoint/search)를 참조하세요.

```python
from langchain_tavily import TavilySearch

tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # start_date=None,
    # end_date=None,
    # include_domains=None,
    # exclude_domains=None
)
```

### 인자를 전달하여 직접 호출하기

Tavily 검색 도구는 호출 시 다음 인자를 받습니다:

- `query` (필수): 자연어 검색 쿼리
- 다음 인자들도 호출 시 설정할 수 있습니다: `include_images`, `search_depth`, `time_range`, `include_domains`, `exclude_domains`, `include_images`, `start_date`, `end_date`
- 신뢰성과 성능 상의 이유로, 응답 크기에 영향을 미치는 특정 매개변수는 호출 시 수정할 수 없습니다: `include_answer`와 `include_raw_content`. 이러한 제한은 예기치 않은 컨텍스트 윈도우 문제를 방지하고 일관된 결과를 보장합니다.

참고: 선택적 인자는 에이전트가 동적으로 설정할 수 있습니다. 인스턴스 생성 시 인자를 설정한 후 다른 값으로 도구를 호출하면, 도구는 호출 시 전달한 값을 사용합니다.

```python
# 기본 쿼리
tool.invoke({"query": "What happened at the last wimbledon"})
```

출력:

```python
{
    'query': 'What happened at the last wimbledon',
    'follow_up_questions': None,
    'answer': None,
    'images': [],
    'results': [
        {
            'url': 'https://en.wikipedia.org/wiki/Wimbledon_Championships',
            'title': 'Wimbledon Championships - Wikipedia',
            'content': 'Due to the COVID-19 pandemic, Wimbledon 2020 was cancelled ...',
            'score': 0.62365627198,
            'raw_content': None
        },
        # ...
        {
            'url': 'https://www.cbsnews.com/news/wimbledon-men-final-carlos-alcaraz-novak-djokovic/',
            'title': "Carlos Alcaraz beats Novak Djokovic at Wimbledon men's final to ...",
            'content': 'In attendance on Sunday was Catherine, the Princess of Wales ...',
            'score': 0.5154731446,
            'raw_content': None
        }
    ],
    'response_time': 2.3
}
```

### 에이전트 도구 호출

도구를 에이전트에 바인딩하여 에이전트 실행기와 함께 직접 사용할 수 있습니다. 이를 통해 에이전트는 Tavily 검색 도구에 사용 가능한 인자를 동적으로 설정할 수 있습니다. 아래 예제에서 에이전트에게 "세계에서 가장 인기 있는 스포츠는 무엇입니까? 위키피디아 소스만 포함하세요"라고 요청하면, 에이전트는 동적으로 인자를 설정하고 Tavily 검색 도구를 호출합니다: `tavily_search`를 `{'query': 'most popular sport in the world', 'include_domains': ['wikipedia.org'], 'search_depth': 'basic'}`로 호출

```python
# !pip install -qU langchain langchain-openai langchain-tavily
from typing import Any, Dict, Optional
import datetime
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.schema import HumanMessage, SystemMessage

# LLM 초기화
llm = init_chat_model(model="gpt-4o", model_provider="openai", temperature=0)

# Tavily Search 도구 초기화
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

# 'agent_scratchpad'를 포함한 프롬프트 설정
today = datetime.datetime.today().strftime("%D")
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a helpful reaserch assistant, you will be given a query and you will need to
    search the web for the most relevant information. The date today is {today}."""),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # 도구 호출에 필요
])

# 도구를 사용할 수 있는 에이전트 생성
agent = create_openai_tools_agent(
    llm=llm,
    tools=[tavily_search_tool],
    prompt=prompt
)

# 도구 실행을 처리할 에이전트 실행기 생성
agent_executor = AgentExecutor(agent=agent, tools=[tavily_search_tool], verbose=True)

user_input = "What is the most popular sport in the world? include only wikipedia sources"

# 입력을 딕셔너리로 올바르게 구성
response = agent_executor.invoke({"messages": [HumanMessage(content=user_input)]})
```

## Tavily Extract

여기서는 Tavily 추출 도구의 인스턴스를 생성하는 방법을 보여줍니다. 인스턴스를 생성한 후 URL 목록으로 도구를 호출합니다. 이 도구를 사용하면 Tavily의 Extract API 엔드포인트를 통해 URL에서 콘텐츠를 추출할 수 있습니다.

### 인스턴스 생성

도구는 인스턴스 생성 시 다양한 매개변수를 받습니다:

- `extract_depth` (선택, str): 추출의 깊이. "basic" 또는 "advanced" 중 하나입니다. 기본값은 "basic"입니다.
- `include_images` (선택, bool): 추출에 이미지를 포함할지 여부. 기본값은 False입니다.

사용 가능한 매개변수에 대한 포괄적인 개요는 [Tavily Extract API 문서](https://docs.tavily.com/documentation/api-reference/endpoint/extract)를 참조하세요.

```python
from langchain_tavily import TavilyExtract

tool = TavilyExtract(
    extract_depth="advanced",
    include_images=False,
)
```

### 인자를 전달하여 직접 호출하기

Tavily 추출 도구는 호출 시 다음 인자를 받습니다:

- `urls` (필수): 콘텐츠를 추출할 URL 목록.
- `extract_depth`와 `include_images` 모두 호출 시 설정할 수 있습니다.

참고: 선택적 인자는 에이전트가 동적으로 설정할 수 있습니다. 인스턴스 생성 시 인자를 설정한 후 다른 값으로 도구를 호출하면, 도구는 호출 시 전달한 값을 사용합니다.

```python
# URL에서 콘텐츠 추출
result = tool.invoke({
    "urls": ["https://en.wikipedia.org/wiki/Lionel_Messi"]
})
```

출력:

```python
{
    'results': [{
        'url': 'https://en.wikipedia.org/wiki/Lionel_Messi',
        'raw_content': 'Lionel Messi\nLionel Andrés "Leo" Messi...',
        'images': []
    }],
    'failed_results': [],
    'response_time': 0.79
}
```

## Tavily 연구 에이전트

이 예제는 Tavily의 검색 및 추출 Langchain 도구를 사용하여 강력한 웹 연구 에이전트를 구축하는 방법을 보여줍니다.

### 기능

- 인터넷 검색: Tavily의 검색 API를 사용하여 웹에서 최신 정보를 쿼리합니다
- 콘텐츠 추출: 웹 페이지에서 특정 콘텐츠를 추출하고 분석합니다
- 원활한 통합: OpenAI의 함수 호출 기능과 함께 작동하여 신뢰할 수 있는 도구 사용을 제공합니다

```python
# !pip install -qU langchain langchain-openai langchain-tavily
from typing import Any, Dict, Optional
import datetime
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch, TavilyExtract
from langchain.schema import HumanMessage, SystemMessage

# LLM 초기화
llm = ChatOpenAI(temperature=0, model="gpt-4o")

# Tavily Search 도구 초기화
tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)

# Tavily Extract 도구 초기화
tavily_extract_tool = TavilyExtract()

tools = [tavily_search_tool, tavily_extract_tool]

# 'agent_scratchpad'를 포함한 프롬프트 설정
today = datetime.datetime.today().strftime("%D")
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a helpful reaserch assistant, you will be given a query and you will need to
    search the web for the most relevant information then extract content to gain more insights. The date today is {today}."""),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),  # 도구 호출에 필요
])

# 도구를 사용할 수 있는 에이전트 생성
agent = create_openai_tools_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# 도구 실행을 처리할 에이전트 실행기 생성
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

user_input = "Research the latest developments in quantum computing and provide a detailed summary of how it might impact cybersecurity in the next decade."

# 입력을 딕셔너리로 올바르게 구성
response = agent_executor.invoke({"messages": [HumanMessage(content=user_input)]})
```
