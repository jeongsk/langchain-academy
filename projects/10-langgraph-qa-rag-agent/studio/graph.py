import getpass
import os

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from nodes import (
    FilteringDocumentsNode,
    GeneralAnswerNode,
    QueryRewriteNode,
    RagAnswerNode,
    RetrieveNode,
    WebSearchNode,
    answer_groundedness_check,
    decide_to_web_search_node,
    routing_node,
)
from retrievers import init_retriever
from states import State

load_dotenv("./.env", override=True)


def _set_env(var: str):
    env_value = os.environ.get(var)
    if not env_value:
        env_value = getpass.getpass(f"{var}: ")

    os.environ[var] = env_value


os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "10-langgraph-qa-rag-agent"
_set_env("LANGSMITH_API_KEY")
_set_env("OPENAI_API_KEY")


retriever = init_retriever()

builder = StateGraph(State)

# 노드
builder.add_node("query_expand", QueryRewriteNode())  # 질문 재작성
builder.add_node("query_rewrite", QueryRewriteNode())  # 질문 재작성
builder.add_node("web_search", WebSearchNode())  # 웹 검색
builder.add_node("retrieve", RetrieveNode(retriever))  # 문서 검색
builder.add_node("grade_documents", FilteringDocumentsNode())  # 문서 평가
builder.add_node("general_answer", GeneralAnswerNode())  # 일반 답변 생성
builder.add_node("rag_answer", RagAnswerNode())  # RAG 답변 생성

# 엣지
builder.add_conditional_edges(
    START,
    routing_node,
    {
        "query_expansion": "query_expand",  # 웹 검색으로 라우팅
        "general_answer": "general_answer",  # 벡터스토어로 라우팅
    },
)

builder.add_edge("query_expand", "retrieve")
builder.add_edge("retrieve", "grade_documents")
builder.add_conditional_edges(
    "grade_documents",
    decide_to_web_search_node,
    {
        "web_search": "web_search",  # 웹 검색 필요
        "rag_answer": "rag_answer",  # RAG 답변 생성 가능
    },
)
builder.add_edge("query_rewrite", "rag_answer")
builder.add_conditional_edges(
    "rag_answer",
    answer_groundedness_check,
    {
        "relevant": END,
        "not relevant": "web_search",
        "not grounded": "query_rewrite",
    },
)
builder.add_edge("web_search", "rag_answer")

graph = builder.compile()
