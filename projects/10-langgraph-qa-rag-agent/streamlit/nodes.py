from abc import ABC, abstractmethod
from typing import Annotated, Literal

from chains import (
    create_answer_grade_chain,
    create_groundedness_checker_chain,
    create_retrieval_grader_chain,
)
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from states import State
from tools import create_web_search_tool


class BaseNode(ABC):
    def __init__(self, **kwargs):
        self.name = "BaseNode"
        self.verbose = False
        if "verbose" in kwargs:
            self.verbose = kwargs["verbose"]

    @abstractmethod
    def execute(self, state: State) -> State:
        pass

    def logging(self, method_name, **kwargs):
        if self.verbose:
            print(f"[{self.name}] {method_name}")
            for key, value in kwargs.items():
                print(f"{key}: {value}")

    def __call__(self, state: State):
        return self.execute(state)


class RouteQuery(BaseModel):
    binary_score: Annotated[
        Literal[1, 0],
        Field(
            ...,
            description="사용자 질문이 벡터 스토어 검색이 필요한지 여부를 판단합니다."
            "벡터 스토어에는 LangGraph 와 RAG(Retrieval Augmented Generation) 관련 소스 코드와 문서가 포함되어 있습니다."
            "관련 있는 경우는 1를 반환합니다."
            "질문이 소스 코드 또는 문서와 관련된지 판단할 수 없는 경우 1을 반환하십시오."
            "답변을 모르는 경우 1를 반환하십시오."
            "그 외에는 모두 0을 반환합니다.",
        ),
    ]


class RouteQuestionNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "RouteQuestionNode"
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        ).with_structured_output(RouteQuery)

    def execute(self, state: State) -> str:
        question = state["question"]
        evaluation = self.llm.invoke({"question": question})

        if evaluation.binary_score == 1:
            return "query_expansion"
        else:
            return "general_answer"


class RewriteQuery(BaseModel):
    improved_question: Annotated[
        str,
        Field(
            ...,
            description="질문 재작성 도구로, 입력된 질문을 CODE SEARCH(github repository)에 최적화된 더 나은 버전으로 변환합니다."
            "기존 질문의 근본적인 의미적 의도/의미를 추론하세요."
            "영어로 작성하세요.",
        ),
    ]


class QueryRewriteNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "QueryRewriteNode"
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        ).with_structured_output(RewriteQuery)

    def execute(self, state: State) -> State:
        question = state["question"]
        response = self.llm.invoke({"question": question})
        return {
            "question": response.improved_question,
        }


class RetrieveNode(BaseNode):
    def __init__(self, retriever, **kwargs):
        super().__init__(**kwargs)
        self.name = "RetrieveNode"
        self.retriever = retriever

    def execute(self, state: State) -> State:
        question = state["question"]
        documents = self.retriever.invoke(question)
        return State(documents=documents)


class GeneralAnswerNode(BaseNode):
    def __init__(self, llm, **kwargs):
        super().__init__(**kwargs)
        self.name = "GeneralAnswerNode"
        self.llm = llm

    def execute(self, state: State) -> State:
        question = state["question"]
        answer = self.llm.invoke(question)
        return State(generation=answer.content)


class RagAnswerNode(BaseNode):
    def __init__(self, rag_chain, **kwargs):
        super().__init__(**kwargs)
        self.name = "RagAnswerNode"
        self.rag_chain = rag_chain

    def execute(self, state: State) -> State:
        question = state["question"]
        documents = state["documents"]
        answer = self.rag_chain.invoke({"context": documents, "question": question})
        return State(generation=answer)


class FilteringDocumentsNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "FilteringDocumentsNode"
        self.retrieval_grader = create_retrieval_grader_chain()

    def execute(self, state: State) -> State:
        question = state["question"]
        documents = state["documents"]

        filtered_docs = []
        for d in documents:
            score = self.retrieval_grader.invoke(
                {"question": question, "document": d.page_content}
            )
            if score.binary_score == "yes":
                filtered_docs.append(d)

        return State(documents=filtered_docs)


class WebSearchNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "WebSearchNode"
        self.web_search_tool = create_web_search_tool()

    def execute(self, state: State) -> State:
        question = state["question"]
        web_results = self.web_search_tool.invoke({"query": question})
        web_results_docs = [
            Document(
                page_content=web_result["content"],
                metadata={"source": web_result["url"]},
            )
            for web_result in web_results
        ]
        return State(documents=web_results_docs)


class AnswerGroundednessCheckNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "AnswerGroundednessCheckNode"
        self.groundedness_checker = create_groundedness_checker_chain()
        self.relevant_answer_checker = create_answer_grade_chain()

    def execute(self, state: State) -> State:
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]

        score = self.groundedness_checker.invoke(
            {"documents": documents, "generation": generation}
        )

        if score.binary_score == "yes":
            score = self.relevant_answer_checker.invoke(
                {"question": question, "generation": generation}
            )
            if score.binary_score == "yes":
                return "relevant"
            else:
                return "not relevant"
        else:
            return "not grounded"


# 추가 정보 검색 필요성 여부 평가 노드
def decide_to_web_search_node(state):
    # 문서 검색 결과 가져오기
    filtered_docs = state["documents"]

    if len(filtered_docs) < 2:
        return "web_search"
    else:
        return "rag_answer"
