"""
Perplexity Clone - Main Graph
메인 LangGraph 구성
"""

import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI

from .states import PerplexityState
from .nodes import create_agent_node, should_continue
from .tools import create_search_tool


# 시스템 프롬프트 정의
SYSTEM_PROMPT = """당신은 Perplexity와 같은 유용한 AI 어시스턴트입니다. 사용자의 질문에 답변하는 것이 당신의 임무입니다.

사용 가능한 도구:
- web_search: 웹에서 최신 정보를 검색하는 도구

질문에 답변하기 위해 추가 정보가 필요하면 도구를 사용하세요.

###

다음 지침을 따르세요:

1. 답변 작성 시:
- 출처 문서의 정보를 기반으로 번호가 매겨진 출처를 사용하세요 (예: [1], [2])
- 마크다운 형식을 사용하세요
- 사용자의 질문과 동일한 언어로 답변을 작성하세요

2. 도구를 사용한 경우 반드시 출처를 포함해야 합니다.

출처 형식:
- 보고서에 사용된 모든 출처를 포함하세요
- 관련 웹사이트의 전체 링크 또는 특정 문서 경로를 제공하세요
- 각 출처를 줄바꿈으로 구분하세요. 마크다운에서 줄바꿈을 만들려면 각 줄 끝에 공백 2개를 사용하세요.
- 다음과 같이 표시됩니다:

**출처**

[1] 링크 또는 문서 이름
[2] 링크 또는 문서 이름

3. 출처를 반드시 결합하세요. 예를 들어 다음은 올바르지 않습니다:

[3] https://ai.meta.com/blog/meta-llama-3-1/
[4] https://ai.meta.com/blog/meta-llama-3-1/

중복된 출처가 없어야 합니다. 다음과 같이 간단히 표시해야 합니다:

[3] https://ai.meta.com/blog/meta-llama-3-1/

4. 최종 검토:
- 답변이 필요한 구조를 따르는지 확인하세요
- 모든 지침을 따랐는지 확인하세요"""


def create_perplexity_graph(
    model_name: str = "gpt-4.1-mini",
    max_results: int = 3,
    topic: str = "general",
    include_domains: list = None,
    exclude_domains: list = None,
    checkpointer=None,
):
    """
    Perplexity 스타일의 검색 Agent 그래프 생성

    Args:
        model_name: OpenAI 모델 이름 (기본값: gpt-4.1-mini)
            - gpt-4.1: 가장 강력한 모델
            - gpt-4.1-mini: 빠르고 비용 효율적 (기본값)
            - gpt-4.1-nano: 초경량, 초고속 모델
        max_results: 최대 검색 결과 수
        topic: 검색 주제 ("general", "news", "finance" 중 하나)
        include_domains: 포함할 도메인 리스트
        exclude_domains: 제외할 도메인 리스트
        checkpointer: 체크포인터 (메모리 저장용)

    Returns:
        CompiledGraph: 컴파일된 LangGraph
    """
    # 검색 도구 생성
    search_tool = create_search_tool(
        max_results=max_results,
        topic=topic,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
    )

    # LLM 모델 설정 (도구 바인딩)
    model = ChatOpenAI(model=model_name, temperature=0)
    model = model.bind_tools([search_tool])

    # 그래프 빌더 생성
    builder = StateGraph(PerplexityState)

    # Agent 노드 추가
    agent_node = create_agent_node(model, SYSTEM_PROMPT)
    builder.add_node("agent", agent_node)

    # 도구 노드 추가 (LangGraph의 ToolNode 사용)
    tool_node = ToolNode([search_tool])
    builder.add_node("search", tool_node)

    # 엣지 추가
    builder.add_edge(START, "agent")

    # 조건부 엣지: agent -> search 또는 END
    builder.add_conditional_edges(
        "agent",
        should_continue,
        {
            "search": "search",
            "end": END,
        },
    )

    # search 후 다시 agent로
    builder.add_edge("search", "agent")

    # 체크포인터 설정 (메모리)
    if checkpointer is None:
        # SqliteSaver를 올바르게 초기화 (context manager 사용 안 함)
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        checkpointer = SqliteSaver(conn)

    # 그래프 컴파일
    graph = builder.compile(checkpointer=checkpointer)

    return graph


# 기본 그래프 인스턴스 (LangGraph Studio용)
# Studio용으로는 파일 기반 DB 사용
_conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
_checkpointer = SqliteSaver(_conn)
graph = create_perplexity_graph(checkpointer=_checkpointer)
