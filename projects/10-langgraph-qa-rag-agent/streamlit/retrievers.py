from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings


def init_retriever(fetch_k=30, top_n=8):
    # 임베딩 모델 초기화
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # 벡터 스토어 불러오기
    vector_store = FAISS.load_local(
        "../faiss_index",
        embeddings,
        allow_dangerous_deserialization=True,
    )

    # Retriever 설정
    retriever = vector_store.as_retriever(search_kwargs={"k": fetch_k})

    # CohereRerank 설정
    compressor = CohereRerank(model="rerank-v3.5", top_n=20)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=retriever,
    )

    return compression_retriever
