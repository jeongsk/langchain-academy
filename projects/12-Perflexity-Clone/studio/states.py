"""
Perplexity Clone - State Definitions
상태 스키마 정의
"""

from typing import Annotated, TypedDict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class PerplexityState(TypedDict):
    """Perplexity Agent 상태 스키마

    Attributes:
        messages: 대화 메시지 리스트 (자동으로 메시지 추가)
        search_results: 웹 검색 결과 저장
        sources: 출처 정보 리스트
    """
    messages: Annotated[List[BaseMessage], add_messages]
    search_results: List[dict]  # 검색 결과 저장
    sources: List[str]  # 출처 URL 저장
