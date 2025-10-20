"""
Perplexity Clone - Tools
웹 검색 도구 정의 (langchain-tavily 사용)
"""

from langchain_core.tools import tool
from langchain_tavily import TavilySearch


def create_search_tool(
    max_results: int = 3,
    topic: str = "general",
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None,
    search_depth: str = "basic",
    include_answer: bool = False,
    include_raw_content: bool = False,
    include_images: bool = False,
) -> TavilySearch:
    """
    웹 검색 도구 생성 (최신 langchain-tavily 패키지 사용)

    Args:
        max_results: 최대 검색 결과 수 (기본값: 3)
        topic: 검색 주제 ("general", "news", "finance" 중 하나, 기본값: "general")
        include_domains: 포함할 도메인 리스트 (최대 300개)
        exclude_domains: 제외할 도메인 리스트 (최대 150개)
        search_depth: 검색 깊이 ("basic" 또는 "advanced", 기본값: "basic")
        include_answer: 원본 쿼리에 대한 답변 포함 여부 (기본값: False)
        include_raw_content: 정제된 HTML 포함 여부 (기본값: False)
        include_images: 이미지 목록 포함 여부 (기본값: False)

    Returns:
        TavilySearch: 설정된 Tavily 검색 도구

    Note:
        - langchain-tavily는 langchain_community.tools.tavily_search를 대체합니다
        - 최신 기능과 지속적인 업데이트를 제공합니다
        - 호출 시에도 동적으로 파라미터 조정 가능 (include_domains, exclude_domains 등)
    """
    # TavilySearch 도구 생성
    search_tool = TavilySearch(
        max_results=max_results,
        topic=topic,
        search_depth=search_depth,
        include_answer=include_answer,
        include_raw_content=include_raw_content,
        include_images=include_images,
        include_domains=include_domains,
        exclude_domains=exclude_domains,
    )

    # 도구 메타데이터 설정
    search_tool.name = "web_search"
    search_tool.description = (
        "웹에서 최신 정보를 검색하는 도구입니다. "
        "사용자의 질문에 답하기 위해 추가 정보가 필요할 때 사용하세요. "
        "\n\n"
        "검색 결과는 다음을 포함합니다:\n"
        "- url: 웹 페이지 URL\n"
        "- title: 페이지 제목\n"
        "- content: 관련 콘텐츠 요약\n"
        "- score: 관련성 점수 (0-1)\n"
        "\n"
        "호출 시 다음 파라미터를 동적으로 설정할 수 있습니다:\n"
        "- query (필수): 검색 쿼리\n"
        "- include_domains: 포함할 도메인 리스트\n"
        "- exclude_domains: 제외할 도메인 리스트\n"
        "- search_depth: 'basic' 또는 'advanced'\n"
        "- include_images: 이미지 포함 여부"
    )

    return search_tool


@tool
def format_sources(search_results: list[dict]) -> str:
    """
    검색 결과를 출처 형식으로 포맷팅

    Args:
        search_results: Tavily 검색 결과 리스트
            각 결과는 {'url': str, 'title': str, 'content': str, 'score': float} 형식

    Returns:
        str: 포맷팅된 출처 문자열 (중복 제거됨)

    Example:
        >>> results = [
        ...     {'url': 'https://example.com', 'title': 'Example'},
        ...     {'url': 'https://example.com', 'title': 'Duplicate'},  # 중복
        ... ]
        >>> format_sources(results)
        '[1] https://example.com'
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
