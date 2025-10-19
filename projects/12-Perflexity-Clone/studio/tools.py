"""
Perplexity Clone - Tools
웹 검색 도구 정의
"""

from typing import List
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


def create_search_tool(
    max_results: int = 3,
    topic: str = "general",
    include_domains: List[str] = None,
    exclude_domains: List[str] = None,
) -> TavilySearchResults:
    """
    웹 검색 도구 생성

    Args:
        max_results: 최대 검색 결과 수 (기본값: 3)
        topic: 검색 주제 ("general" 또는 "news")
        include_domains: 포함할 도메인 리스트
        exclude_domains: 제외할 도메인 리스트

    Returns:
        TavilySearchResults: 설정된 Tavily 검색 도구
    """
    search_kwargs = {
        "max_results": max_results,
        "topic": topic,
    }

    if include_domains:
        search_kwargs["include_domains"] = include_domains

    if exclude_domains:
        search_kwargs["exclude_domains"] = exclude_domains

    search_tool = TavilySearchResults(**search_kwargs)
    search_tool.name = "web_search"
    search_tool.description = (
        "웹에서 정보를 검색하는 도구입니다. "
        "사용자의 질문에 답하기 위해 최신 정보가 필요할 때 사용하세요. "
        "검색 결과는 제목, URL, 내용, 신뢰도 점수를 포함합니다."
    )

    return search_tool


@tool
def format_sources(search_results: List[dict]) -> str:
    """
    검색 결과를 출처 형식으로 포맷팅

    Args:
        search_results: Tavily 검색 결과 리스트

    Returns:
        str: 포맷팅된 출처 문자열
    """
    if not search_results:
        return ""

    sources = []
    seen_urls = set()

    for i, result in enumerate(search_results, 1):
        url = result.get("url", "")
        if url and url not in seen_urls:
            sources.append(f"[{i}] {url}")
            seen_urls.add(url)

    return "\n".join(sources)
