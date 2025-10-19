"""
Perplexity Clone - Streamlit UI (Remote Graph)
LangGraph Studio 서버와 통신하는 버전
"""

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langgraph_sdk import get_client
import uuid
import os
from dotenv import load_dotenv
import asyncio


# 환경 변수 로드
load_dotenv()

# AsyncRunner: async 함수를 별도 스레드에서 실행하는 헬퍼
from concurrent.futures import ThreadPoolExecutor

class AsyncRunner:
    """
    Streamlit 환경에서 async 함수를 안전하게 실행하기 위한 헬퍼 클래스
    각 async 호출을 별도 스레드의 독립적인 event loop에서 실행하여
    event loop 충돌을 방지합니다.
    """
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
    
    def run(self, async_func, *args, **kwargs):
        """
        async 함수를 별도 스레드의 새 event loop에서 실행
        
        Args:
            async_func: 실행할 async 함수
            *args, **kwargs: async 함수에 전달할 인자
        
        Returns:
            async 함수의 실행 결과
        """
        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(async_func(*args, **kwargs))
            finally:
                loop.close()
        
        future = self.executor.submit(_run)
        return future.result()
    
    def run_generator(self, async_gen_func, *args, **kwargs):
        """
        async generator를 동기 리스트로 변환
        
        Args:
            async_gen_func: 실행할 async generator 함수
            *args, **kwargs: async generator 함수에 전달할 인자
        
        Returns:
            generator에서 yield된 모든 항목의 리스트
        """
        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                async def collect():
                    results = []
                    async for item in async_gen_func(*args, **kwargs):
                        results.append(item)
                    return results
                return loop.run_until_complete(collect())
            finally:
                loop.close()
        
        future = self.executor.submit(_run)
        return future.result()



# 페이지 설정
st.set_page_config(
    page_title="Perplexity Clone (Remote)",
    page_icon="🔍",
    layout="wide",
)

# 제목 및 설명
st.title("🔍 Perplexity Clone (Remote)")
st.markdown(
    """
    LangGraph Studio 서버와 통신하는 **웹 검색 Agent**입니다.
    질문하시면 웹에서 정보를 검색하여 **출처와 함께** 답변을 제공합니다.
    """
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "client" not in st.session_state:
    st.session_state.client = None

if "server_url" not in st.session_state:
    st.session_state.server_url = os.getenv("LANGGRAPH_API_URL", "http://127.0.0.1:2024")

if "async_runner" not in st.session_state:
    st.session_state.async_runner = AsyncRunner()

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")

    # 서버 URL 설정
    st.subheader("🌐 서버 연결")
    server_url = st.text_input(
        "LangGraph Studio URL",
        value=st.session_state.server_url,
        help="LangGraph Studio 서버 주소 (예: http://127.0.0.1:2024)"
    )

    if st.button("🔌 연결", use_container_width=True):
        try:
            with st.spinner("서버 연결 중..."):
                st.session_state.client = get_client(url=server_url)
                st.session_state.server_url = server_url
                st.success("✅ 서버에 연결되었습니다!")

                # 사용 가능한 그래프 목록 조회 (동기 방식)
                try:
                    assistants = st.session_state.async_runner.run(
                        st.session_state.client.assistants.search
                    )
                    if assistants:
                        st.info(f"사용 가능한 그래프: {len(assistants)}개")
                except Exception as search_error:
                    # 검색 실패는 무시 (연결은 성공)
                    pass
        except Exception as e:
            st.error(f"❌ 연결 실패: {str(e)}")

    st.divider()

    # 대화 초기화 버튼
    if st.button("🔄 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.divider()

    # 현재 스레드 정보
    st.caption(f"Thread ID: `{st.session_state.thread_id[:8]}...`")

    st.divider()
    st.caption("Made with LangGraph 🦜🔗")


# 서버 연결 상태 확인
if st.session_state.client is None:
    st.warning("⚠️ 먼저 사이드바에서 LangGraph Studio 서버에 연결해주세요.")
    st.info("""
    **연결 방법:**
    1. 터미널에서 `cd projects/12-Perplexity-Clone/studio` 실행
    2. `langgraph dev` 명령으로 서버 시작
    3. 사이드바에서 '🔌 연결' 버튼 클릭
    """)
    st.stop()


# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자 입력
if user_input := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(user_input)

    # 대화 기록에 추가
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("🔍 검색 중..."):
            # 응답 컨테이너
            response_container = st.empty()
            search_status_container = st.container()

            try:
                # 입력 메시지
                input_data = {
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                }

                # 그래프 이름 (langgraph.json에 정의된 이름)
                graph_name = "perplexity_agent"

                # 스트리밍 실행 (AsyncRunner 사용)
                full_response = ""
                tool_calls_made = []

                # async generator를 동기 리스트로 변환
                chunks = st.session_state.async_runner.run_generator(
                    st.session_state.client.runs.stream,
                    st.session_state.thread_id,
                    graph_name,
                    input=input_data,
                    stream_mode="values"
                )

                # 수집된 chunk들을 순회하며 처리
                for chunk in chunks:
                    # 메시지 이벤트 처리
                    if "messages" in chunk:
                        last_message = chunk["messages"][-1]

                        # AI 메시지인 경우
                        if last_message.get("type") == "ai":
                            # 도구 호출 확인
                            if "tool_calls" in last_message and last_message["tool_calls"]:
                                for tool_call in last_message["tool_calls"]:
                                    tool_id = tool_call.get("id")
                                    if tool_id not in tool_calls_made:
                                        tool_calls_made.append(tool_id)
                                        with search_status_container:
                                            st.info(f"🔍 웹 검색 실행 중: `{tool_call.get('name')}`")

                            # 최종 응답
                            if last_message.get("content"):
                                full_response = last_message["content"]
                                response_container.markdown(full_response)


                # 대화 기록에 추가
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

            except Exception as e:
                st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                st.exception(e)


# 하단 정보
st.divider()
with st.expander("ℹ️ 사용 방법"):
    st.markdown("""
    ### 사용 방법 (Remote 모드)

    1. **서버 시작**: 터미널에서 `langgraph dev` 실행
    2. **연결**: 사이드바에서 서버 URL 확인 후 '🔌 연결' 클릭
    3. **질문 입력**: 하단 입력창에 질문 입력
    4. **응답 확인**: AI가 웹에서 정보를 검색하여 출처와 함께 답변 제공

    ### 장점

    - **개발/프로덕션 분리**: UI와 그래프 로직 분리
    - **스케일링**: 여러 클라이언트가 동일한 그래프 서버 사용 가능
    - **디버깅**: LangGraph Studio UI에서 실시간 디버깅
    - **배포**: 그래프 서버를 별도로 배포 가능

    ### 로컬 모드 vs Remote 모드

    - **app.py**: 그래프를 직접 로드하여 실행 (간단, 올인원)
    - **app_remote.py**: LangGraph Studio 서버와 통신 (프로덕션 환경)
    """)

with st.expander("🔧 서버 정보"):
    if st.session_state.client:
        st.write(f"**서버 URL**: `{st.session_state.server_url}`")
        st.write(f"**Thread ID**: `{st.session_state.thread_id}`")

        if st.button("🔍 사용 가능한 그래프 조회"):
            try:
                assistants = st.session_state.async_runner.run(
                    st.session_state.client.assistants.search
                )
                st.json([{"name": a["name"], "graph_id": a["graph_id"]} for a in assistants])
            except Exception as e:
                st.error(f"조회 실패: {str(e)}")
