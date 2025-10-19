"""
Perplexity Clone - Streamlit UI
LangGraph 기반 웹 검색 Agent UI
"""

import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from studio.graph import create_perplexity_graph

# 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Perplexity Clone",
    page_icon="🔍",
    layout="wide",
)

# 제목 및 설명
st.title("🔍 Perplexity Clone")
st.markdown(
    """
    LangGraph 기반 **웹 검색 Agent**입니다.
    질문하시면 웹에서 정보를 검색하여 **출처와 함께** 답변을 제공합니다.
    """
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "graph" not in st.session_state:
    st.session_state.graph = None

if "graph_config" not in st.session_state:
    st.session_state.graph_config = {
        "model_name": "gpt-4.1-mini",
        "max_results": 3,
        "topic": "general",
        "include_domains": [],
        "exclude_domains": [],
    }

# 사이드바 설정
with st.sidebar:
    st.header("⚙️ 설정")

    # 대화 초기화 버튼
    if st.button("🔄 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.divider()

    # 모델 설정
    st.subheader("🤖 모델 설정")
    model_name = st.selectbox(
        "LLM 모델",
        ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"],
        index=1,
        key="model_select",
    )

    # 검색 설정
    st.subheader("🔍 검색 설정")
    max_results = st.slider(
        "최대 검색 결과 수",
        min_value=1,
        max_value=10,
        value=3,
        key="max_results_slider",
    )

    topic = st.selectbox("검색 주제", ["general", "news"], index=0, key="topic_select")

    # 도메인 필터링
    st.subheader("🌐 도메인 필터링")

    # 포함할 도메인
    st.write("**포함할 도메인**")
    new_include_domain = st.text_input(
        "도메인 추가 (예: github.com)",
        key="new_include_domain",
        placeholder="github.com",
    )

    if st.button("➕ 추가", key="add_include_domain"):
        if (
            new_include_domain
            and new_include_domain
            not in st.session_state.graph_config["include_domains"]
        ):
            st.session_state.graph_config["include_domains"].append(new_include_domain)
            st.rerun()

    # 등록된 포함 도메인 목록
    if st.session_state.graph_config["include_domains"]:
        for idx, domain in enumerate(st.session_state.graph_config["include_domains"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"✓ {domain}")
            with col2:
                if st.button("❌", key=f"del_include_{idx}"):
                    st.session_state.graph_config["include_domains"].pop(idx)
                    st.rerun()

    st.divider()

    # 제외할 도메인
    st.write("**제외할 도메인**")
    new_exclude_domain = st.text_input(
        "도메인 추가 (예: wikipedia.org)",
        key="new_exclude_domain",
        placeholder="wikipedia.org",
    )

    if st.button("➕ 추가", key="add_exclude_domain"):
        if (
            new_exclude_domain
            and new_exclude_domain
            not in st.session_state.graph_config["exclude_domains"]
        ):
            st.session_state.graph_config["exclude_domains"].append(new_exclude_domain)
            st.rerun()

    # 등록된 제외 도메인 목록
    if st.session_state.graph_config["exclude_domains"]:
        for idx, domain in enumerate(st.session_state.graph_config["exclude_domains"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.text(f"✓ {domain}")
            with col2:
                if st.button("❌", key=f"del_exclude_{idx}"):
                    st.session_state.graph_config["exclude_domains"].pop(idx)
                    st.rerun()

    st.divider()

    # 그래프 생성/업데이트 버튼
    if st.button("✅ 설정 적용", type="primary", use_container_width=True):
        with st.spinner("그래프 생성 중..."):
            st.session_state.graph_config.update(
                {
                    "model_name": model_name,
                    "max_results": max_results,
                    "topic": topic,
                }
            )

            # 그래프 생성
            st.session_state.graph = create_perplexity_graph(
                model_name=st.session_state.graph_config["model_name"],
                max_results=st.session_state.graph_config["max_results"],
                topic=st.session_state.graph_config["topic"],
                include_domains=st.session_state.graph_config["include_domains"]
                or None,
                exclude_domains=st.session_state.graph_config["exclude_domains"]
                or None,
                checkpointer=SqliteSaver.from_conn_string(":memory:"),
            )
            st.success("✅ 설정이 적용되었습니다!")

    st.divider()
    st.caption("Made with LangGraph 🦜🔗")


# 이전 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자 입력
if user_input := st.chat_input("질문을 입력하세요..."):
    # 그래프가 초기화되지 않은 경우
    if st.session_state.graph is None:
        st.warning("⚠️ 먼저 사이드바에서 '✅ 설정 적용' 버튼을 눌러주세요.")
    else:
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(user_input)

        # 대화 기록에 추가
        st.session_state.messages.append({"role": "user", "content": user_input})

        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("🔍 검색 중..."):
                # 응답 컨테이너
                response_container = st.empty()
                search_status_container = st.container()

                # 그래프 실행 설정
                config = {"configurable": {"thread_id": st.session_state.thread_id}}

                # 입력 메시지
                input_messages = {"messages": [HumanMessage(content=user_input)]}

                try:
                    # 스트리밍 실행
                    full_response = ""
                    tool_calls_made = []

                    for event in st.session_state.graph.stream(
                        input_messages, config, stream_mode="values"
                    ):
                        # 마지막 메시지 추출
                        if "messages" in event:
                            last_message = event["messages"][-1]

                            # AI 메시지인 경우
                            if isinstance(last_message, AIMessage):
                                # 도구 호출이 있는 경우
                                if (
                                    hasattr(last_message, "tool_calls")
                                    and last_message.tool_calls
                                ):
                                    for tool_call in last_message.tool_calls:
                                        if tool_call not in tool_calls_made:
                                            tool_calls_made.append(tool_call)
                                            with search_status_container:
                                                st.info(
                                                    f"🔍 웹 검색 실행 중: `{tool_call['name']}`"
                                                )

                                # 최종 응답
                                if last_message.content:
                                    full_response = last_message.content
                                    response_container.markdown(full_response)

                    # 대화 기록에 추가
                    st.session_state.messages.append(
                        {"role": "assistant", "content": full_response}
                    )

                except Exception as e:
                    st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                    st.exception(e)


# 하단 정보
st.divider()
with st.expander("ℹ️ 사용 방법"):
    st.markdown("""
    ### 사용 방법

    1. **설정 적용**: 사이드바에서 원하는 설정을 선택하고 '✅ 설정 적용' 버튼을 클릭하세요.
    2. **질문 입력**: 하단 입력창에 질문을 입력하세요.
    3. **응답 확인**: AI가 웹에서 정보를 검색하여 출처와 함께 답변을 제공합니다.

    ### 주요 기능

    - **웹 검색**: Tavily API를 사용하여 실시간 웹 검색
    - **출처 표시**: 답변에 사용된 모든 출처를 번호와 함께 표시
    - **멀티턴 대화**: 이전 대화 내용을 기억하고 연속적인 질문 지원
    - **도메인 필터링**: 특정 도메인만 포함하거나 제외할 수 있음

    ### 예시 질문

    - "2024년 AI 트렌드는 무엇인가요?"
    - "LangGraph와 LangChain의 차이점은?"
    - "최근 OpenAI의 새로운 모델 소식은?"
    """)

with st.expander("🔧 현재 설정"):
    st.json(st.session_state.graph_config)
