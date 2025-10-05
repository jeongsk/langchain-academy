from langchain_tavily import TavilySearch


def create_web_search_tool(max_results=6):
    web_search_tool = TavilySearch(max_results=max_results)
    return web_search_tool
