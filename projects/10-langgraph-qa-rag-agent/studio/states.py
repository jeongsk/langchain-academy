from typing import Annotated, TypedDict

from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    question: Annotated[str, "User question"]
    documents: Annotated[list[Document], "answer for context documents"]
    generation: Annotated[str, "LLM generation/answer"]
