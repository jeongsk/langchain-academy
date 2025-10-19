"""
Perplexity Clone - Graph Nodes
그래프 노드 정의
"""

from typing import Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_openai import ChatOpenAI

from states import PerplexityState


def create_agent_node(model: ChatOpenAI, system_prompt: str):
    """
    Agent 노드 생성 팩토리 함수

    Args:
        model: OpenAI 채팅 모델
        system_prompt: 시스템 프롬프트

    Returns:
        function: Agent 노드 함수
    """

    def agent_node(state: PerplexityState) -> dict:
        """
        LLM Agent 노드 - 사용자 질문을 처리하고 도구 호출 결정

        Args:
            state: 현재 상태

        Returns:
            dict: 업데이트된 메시지
        """
        messages = state["messages"]

        # 시스템 프롬프트 추가
        messages_with_system = [{"role": "system", "content": system_prompt}] + messages

        # LLM 호출
        response = model.invoke(messages_with_system)

        return {"messages": [response]}

    return agent_node


def search_node(state: PerplexityState) -> dict:
    """
    웹 검색 실행 노드

    Args:
        state: 현재 상태

    Returns:
        dict: 검색 결과가 포함된 ToolMessage
    """
    messages = state["messages"]
    last_message = messages[-1]

    # 도구 호출 정보 추출
    tool_calls = last_message.tool_calls
    search_results = []
    tool_messages = []

    for tool_call in tool_calls:
        # 실제 검색은 graph.py에서 바인딩된 도구를 통해 수행됨
        # 여기서는 ToolMessage 형식으로 반환
        tool_messages.append(
            ToolMessage(
                content=str(tool_call),
                tool_call_id=tool_call["id"],
            )
        )

    return {
        "messages": tool_messages,
        "search_results": search_results,
    }


def should_continue(state: PerplexityState) -> Literal["search", "end"]:
    """
    다음 노드 결정 - 검색이 필요한지 확인

    Args:
        state: 현재 상태

    Returns:
        str: "search" 또는 "end"
    """
    messages = state["messages"]
    last_message = messages[-1]

    # 도구 호출이 있으면 검색 노드로
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "search"

    # 도구 호출이 없으면 종료
    return "end"


def format_final_response(state: PerplexityState) -> dict:
    """
    최종 응답 포맷팅 노드

    Args:
        state: 현재 상태

    Returns:
        dict: 포맷팅된 최종 메시지
    """
    messages = state["messages"]
    sources = state.get("sources", [])

    # 마지막 AI 메시지에 출처 추가
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and sources:
        formatted_sources = "\n\n**출처**\n\n" + "\n".join(
            f"[{i + 1}] {source}" for i, source in enumerate(sources)
        )
        updated_content = last_message.content + formatted_sources
        updated_message = AIMessage(content=updated_content)
        return {"messages": [updated_message]}

    return {}
