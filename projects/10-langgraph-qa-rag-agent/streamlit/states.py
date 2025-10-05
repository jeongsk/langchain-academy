from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    question: Annotated[str, "User question"]
    documents: Annotated[list[str], "answer for context documents"]
