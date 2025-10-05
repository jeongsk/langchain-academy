from abc import ABC, abstractmethod
from typing import Annotated, Literal

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
        question = state.get("question")
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
        question = state.get("question")
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
        question = state.get("question")
        documents = self.retriever.invoke(question)
        return {
            "documents": documents,
        }


class GeneralAnswerNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "GeneralAnswerNode"
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )

    def execute(self, state: State) -> State:
        response = self.llm.invoke(state.get("messages"))
        return {
            "messages": [response],
            "question": "",
            "documents": [],
        }


class RagAnswerNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "RagAnswerNode"
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        )
        self.system_prompt = """당신은 RAG(Retrieval Augmented Generation) 기반 코드 어시스턴트입니다.
제공된 소스 코드와 문서를 기반으로 질문에 답변합니다.

## 핵심 원칙

- 제공된 CONTEXT 내의 정보만 사용
- 답변을 모르는 경우 솔직히 모른다고 응답
- 외부 정보 추측 금지
- 모든 답변은 한국어로 작성

## 답변 작성 가이드

### 1. 코드 중심 답변
- 가능한 한 많은 예제 코드 포함
- 전체 코드 스니펫 작성 권장
- 실행 가능한 완전한 코드 제공

### 2. 출처 인용
- CONTEXT 내 각 문서의 출처 확인
- 관련 진술 옆에 인라인 인용 표기: [1], [2], ...
- 중복 출처는 하나로 통합
- 답변 하단에 출처 목록 작성

**출처 표기 형식:**
```
**출처**
- [1] 문서명.md (또는 전체 URL)
- [2] 문서명.md (또는 전체 URL)
```

**출처 표기 예시:**
- `<source>assistant/docs/llama3_1.md" page="7"</source>` → [1] llama3_1.md
- 마크다운 줄바꿈: 각 줄 끝에 공백 두 개 사용

## 입력 데이터

### CONTEXT
질문에 답변할 때 사용할 수 있는 소스 코드 및 문서:

{context}

### 질문
사용자의 질문:

{question}

## 최종 체크리스트

답변 제출 전 다음 사항을 확인하세요:

- [ ] CONTEXT 정보만 사용했는가?
- [ ] 전체 코드 스니펫이 포함되었는가?
- [ ] 출처가 올바르게 인용되었는가?
- [ ] 중복 출처가 제거되었는가?
- [ ] 한국어로 작성되었는가?
- [ ] 단계별 논리적 설명이 포함되었는가?

---

질문에 대한 답변과 출처:
"""

    def execute(self, state: State) -> State:
        question = state.get("question")
        documents = state.get("documents")
        response = self.llm.invoke(
            self.system_prompt.format(
                context=documents,
                question=question,
            )
        )
        return {
            "messages": [response],
            "question": "",
            "documents": [],
        }


# 문서 평가를 위한 데이터 모델 정의
class GradeDocuments(BaseModel):
    """검색된 문서의 관련성 검증"""

    binary_score: Annotated[
        Literal[1, 0],
        Field(
            ..., description="Context 문서가 질문과 관련이 있는가? 1 또는 0 으로 답변"
        ),
    ]


class FilteringDocumentsNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "FilteringDocumentsNode"
        self.llm = ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
        ).with_structured_output(GradeDocuments)

    def execute(self, state: State) -> State:
        question = state.get("question")
        documents = state.get("documents")

        filtered_docs: list[Document] = []
        for doc in documents:
            response = self.llm.invoke(f"{question}\n\n{doc}")
            if response.binary_score == 1:
                filtered_docs.append(doc)
            continue

        return {
            "documents": filtered_docs,
        }


class WebSearchNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "WebSearchNode"
        self.web_search_tool = create_web_search_tool()

    def execute(self, state: State) -> State:
        question = state.get("question")
        web_results = self.web_search_tool.invoke({"query": question})

        documents: list[Document] = []
        for r in web_results["results"]:
            documents.append(
                Document(
                    page_content=f"# {r['title']}\n\n{r['content']}",
                    metadata={
                        "source": r["url"],
                        "score": r["score"],
                    },
                )
            )

        return {
            "documents": documents,
        }


class GroundednessChecker(BaseModel):
    binary_score: Annotated[
        Literal[1, 0],
        Field(
            ...,
            description="LLM 답변이 검색된 사실 집합에 근거하거나 이를 뒷받침하는지 평가하는 채점 도구입니다."
            "답변이 사실 집합에 근거하거나 이를 뒷받침하면 1을 반환하고, 그렇지 않으면 0을 반환하세요.",
        ),
    ]


class RelevantAnswerChecker(BaseModel):
    binary_score: Annotated[
        Literal[1, 0],
        Field(
            ...,
            description="답변이 질문을 해결했는지 평가하는 채점 도구입니다."
            "질문에 대한 답변이 해결되었다면 1을 반환하고, 그렇지 않다면 0을 반환하세요.",
        ),
    ]


class AnswerGroundednessCheckNode(BaseNode):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "AnswerGroundednessCheckNode"
        llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
        self.groundedness_checker = llm.with_structured_output(GroundednessChecker)
        self.relevant_answer_checker = llm.with_structured_output(RelevantAnswerChecker)

    def execute(self, state: State) -> State:
        question = state.get("question")
        documents = state.get("documents")
        generation = state.get("generation")

        response = self.groundedness_checker.invoke(
            f"Set of facts: \n\n {documents} \n\n LLM generation: {generation}"
        )

        if response.binary_score == 1:
            response = self.relevant_answer_checker.invoke(
                f"User question: \n\n {question} \n\n LLM generation: {generation}"
            )
            if response.binary_score == 1:
                return "relevant"
            else:
                return "not relevant"
        else:
            return "not grounded"


# 추가 정보 검색 필요성 여부 평가 노드
def decide_to_web_search_node(state):
    documents = state.get("documents")

    if len(documents) < 2:
        return "web_search"
    else:
        return "rag_answer"
