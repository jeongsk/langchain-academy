This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where security check has been disabled.

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Security check has been disabled - content may contain sensitive information
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.streamlit/
  config.toml
modules/
  agent.py
  base.py
  handler.py
  tools.py
.env_sample
.gitignore
main.py
pyproject.toml
README.md
```

# Files

## File: .streamlit/config.toml
````toml
[theme]

# 사용자 정의 테마가 상속받을 Streamlit 기본 테마입니다.
# "light" 또는 "dark" 중 하나를 선택할 수 있습니다.
base = "light"

# 대화형 요소에 사용되는 기본 강조 색상입니다.
primaryColor = "#027373"

# 메인 콘텐츠 영역의 배경색입니다.
backgroundColor = "#F2E7DC"

# 사이드바와 대부분의 대화형 위젯에 사용되는 배경색입니다.
secondaryBackgroundColor = "#A9D9D0"

# 대부분의 텍스트에 사용되는 색상입니다.
textColor = "#0D0D0D"

# 코드 블록을 제외한 앱의 모든 텍스트에 사용되는 글꼴 패밀리입니다.
# "sans serif", "serif", 또는 "monospace" 중 하나를 선택할 수 있습니다.
font = "monospace"
````

## File: modules/agent.py
````python
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


def create_agent_executor(model_name="gpt-4o", tools=[]):
    # 메모리 설정
    memory = MemorySaver()

    # 모델 설정
    model = ChatOpenAI(model_name=model_name)

    # 시스템 프롬프트 설정
    system_prompt = """You are an helpful AI Assitant like Perplexity. Your mission is to answer the user's question.

Here are the tools you can use:
{tools}

If you need further information to answer the question, use the tools to get the information.

###

Please follow these instructions:

1. For your answer:
- Use numbered sources in your report (e.g., [1], [2]) based on information from source documents
- Use markdown format
- Write your response as the same language as the user's question


2. You must include sources in your answer if you use the tools. 

For sources:
- Include all sources used in your report
- Provide full links to relevant websites or specific document paths
- Separate each source by a newline. Use two spaces at the end of each line to create a newline in Markdown.
- It will look like:

**출처**

[1] Link or Document name
[2] Link or Document name

3.Be sure to combine sources. For example this is not correct:

[3] https://ai.meta.com/blog/meta-llama-3-1/
[4] https://ai.meta.com/blog/meta-llama-3-1/

There should be no redundant sources. It should simply be:

[3] https://ai.meta.com/blog/meta-llama-3-1/
        
4. Final review:
- Ensure the answer follows the required structure
- Check that all guidelines have been followed"""

    agent_executor = create_react_agent(
        model, tools=tools, checkpointer=memory, state_modifier=system_prompt
    )

    return agent_executor
````

## File: modules/base.py
````python
from typing import Any, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")  # 제네릭 타입 변수 정의


class BaseTool(ABC, Generic[T]):
    """도구들의 기본 클래스"""

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """도구 초기화를 위한 추상 메서드"""
        pass

    @abstractmethod
    def _create_tool(self) -> T:
        """실제 도구 객체를 생성하는 추상 메서드"""
        pass

    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> T:
        """도구 객체를 생성하고 바로 반환하는 팩토리 메서드"""
        instance = cls(*args, **kwargs)
        tool = instance._create_tool()
        return tool

    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """도구를 실행하는 추상 메서드"""
        pass
````

## File: modules/handler.py
````python
import streamlit as st


def get_current_tool_message(tool_args, tool_call_id):
    """
    Get the tool message corresponding to the given tool call ID.

    Args:
        tool_args (list): List of tool arguments
        tool_call_id (str): ID of the tool call to find

    Returns:
        dict: Tool message if found, None otherwise
    """
    if tool_call_id:
        for tool_arg in tool_args:
            if tool_arg["tool_call_id"] == tool_call_id:
                return tool_arg
        return None
    else:
        return None


def format_search_result(results):
    """
    Format search results into a markdown string.

    Args:
        results (str): JSON string containing search results

    Returns:
        str: Formatted markdown string with search results
    """
    import json

    results = json.loads(results)

    answer = ""
    for result in results:
        answer += f'**[{result["title"]}]({result["url"]})**\n\n'
        answer += f'{result["content"]}\n\n'
        answer += f'신뢰도: {result["score"]}\n\n'
        answer += "\n-----\n"
    return answer


def stream_handler(streamlit_container, agent_executor, inputs, config):
    """
    Handle streaming of agent execution results in a Streamlit container.

    Args:
        streamlit_container (streamlit.container): Streamlit container to display results
        agent_executor: Agent executor instance
        inputs: Input data for the agent
        config: Configuration settings

    Returns:
        tuple: (container, tool_args, agent_answer)
            - container: Streamlit container with displayed results
            - tool_args: List of tool arguments used
            - agent_answer: Final answer from the agent
    """
    # Initialize result storage
    tool_args = []
    agent_answer = ""
    agent_message = None  # Pre-declare agent_message variable

    container = streamlit_container.container()
    with container:
        for chunk_msg, metadata in agent_executor.stream(
            inputs, config, stream_mode="messages"
        ):
            if hasattr(chunk_msg, "tool_calls") and chunk_msg.tool_calls:
                # Initialize tool call result
                tool_arg = {
                    "tool_name": "",
                    "tool_result": "",
                    "tool_call_id": chunk_msg.tool_calls[0]["id"],
                }
                # Save tool name
                tool_arg["tool_name"] = chunk_msg.tool_calls[0]["name"]
                if tool_arg["tool_name"]:
                    tool_args.append(tool_arg)

            if hasattr(chunk_msg, "tool_call_chunks") and chunk_msg.tool_call_chunks:
                if len(chunk_msg.tool_call_chunks) > 0:  # Add None check
                    # Accumulate tool call arguments
                    chunk_msg.tool_call_chunks[0]["args"]

            if metadata["langgraph_node"] == "tools":
                # Save tool execution results
                current_tool_message = get_current_tool_message(
                    tool_args, chunk_msg.tool_call_id
                )
                if current_tool_message:
                    current_tool_message["tool_result"] = chunk_msg.content
                    with st.status(f'✅ {current_tool_message["tool_name"]}'):
                        if current_tool_message["tool_name"] == "web_search":
                            st.markdown(
                                format_search_result(
                                    current_tool_message["tool_result"]
                                )
                            )

            if metadata["langgraph_node"] == "agent":
                if chunk_msg.content:
                    if agent_message is None:
                        agent_message = st.empty()
                    # Accumulate agent message
                    agent_answer += chunk_msg.content
                    agent_message.markdown(agent_answer)

        return container, tool_args, agent_answer
````

## File: modules/tools.py
````python
from typing import Any, List
from langchain_teddynote.tools.tavily import TavilySearch
from .base import BaseTool


class WebSearchTool(BaseTool[TavilySearch]):
    """웹 검색을 수행하는 도구 클래스"""

    def __init__(
        self,
        topic: str = "general",
        max_results: int = 3,
        include_answer: bool = False,
        include_raw_content: bool = False,
        include_images: bool = False,
        format_output: bool = False,
        include_domains: List[str] = [],
        exclude_domains: List[str] = [],
    ):
        """WebSearchTool 초기화 메서드"""
        super().__init__()
        self.topic = topic
        self.max_results = max_results
        self.include_answer = include_answer
        self.include_raw_content = include_raw_content
        self.include_images = include_images
        self.format_output = format_output
        self.include_domains = include_domains
        self.exclude_domains = exclude_domains

    def _create_tool(self) -> TavilySearch:
        """TavilySearch 객체를 생성하고 설정하는 내부 메서드"""
        search = TavilySearch(
            topic=self.topic,
            max_results=self.max_results,
            include_answer=self.include_answer,
            include_raw_content=self.include_raw_content,
            include_images=self.include_images,
            format_output=self.format_output,
            include_domains=self.include_domains,
            exclude_domains=self.exclude_domains,
        )
        search.name = "web_search"
        search.description = "Use this tool to search on the web"
        return search

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """도구를 실행하는 메서드"""
        tool = self._create_tool()
        return tool(*args, **kwargs)
````

## File: .env_sample
````
OPENAI_API_KEY=sk-5K9kI4dia...
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=ls__69f274d55...
LANGCHAIN_PROJECT=FASTCAMPUS-PERPLEXITY-CLONE
TAVILY_API_KEY=tvly-mGxBGvzbH...
````

## File: .gitignore
````
# Created by https://www.toptal.com/developers/gitignore/api/jupyternotebooks,python
# Edit at https://www.toptal.com/developers/gitignore?templates=jupyternotebooks,python

### JupyterNotebooks ###
# gitignore template for Jupyter Notebooks
# website: http://jupyter.org/

.ipynb_checkpoints
*/.ipynb_checkpoints/*

.env
.devcontainer/

# IPython
profile_default/
ipython_config.py

# Remove previous ipynb_checkpoints
#   git rm -r .ipynb_checkpoints/

### Python ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook

# IPython

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/#use-with-ide
.pdm.toml

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

### Python Patch ###
# Poetry local configuration file - https://python-poetry.org/docs/configuration/#local-configuration
poetry.toml

# ruff
.ruff_cache/

# LSP config files
pyrightconfig.json

# End of https://www.toptal.com/developers/gitignore/api/jupyternotebooks,python
````

## File: main.py
````python
from attr import dataclass
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_teddynote import logging
from langchain_teddynote.messages import random_uuid
from modules.agent import create_agent_executor
from dotenv import load_dotenv
from modules.handler import stream_handler, format_search_result
from modules.tools import WebSearchTool

# API KEY 정보로드
load_dotenv()

# 프로젝트 이름
logging.langsmith("Perplexity")

st.title("Perplexity 💬")
st.markdown(
    "LLM에 **웹검색 기능** 을 추가한 [Perplexity](https://www.perplexity.ai/) 클론 입니다. _멀티턴_ 대화를 지원합니다."
)

# 대화기록을 저장하기 위한 용도로 생성
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ReAct Agent 초기화
if "react_agent" not in st.session_state:
    st.session_state["react_agent"] = None

# include_domains 초기화
if "include_domains" not in st.session_state:
    st.session_state["include_domains"] = []

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

    st.markdown("made by [@teddynote](https://youtube.com/c/teddynote)")

    # 모델 선택 메뉴
    selected_model = st.selectbox("LLM 선택", ["gpt-4o", "gpt-4o-mini"], index=0)

    # 검색 결과 개수 설정
    search_result_count = st.slider("검색 결과", min_value=1, max_value=10, value=3)

    # include_domains 설정
    st.subheader("검색 도메인 설정")
    search_topic = st.selectbox("검색 주제", ["general", "news"], index=0)
    new_domain = st.text_input("추가할 도메인 입력")
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("도메인 추가", key="add_domain"):
            if new_domain and new_domain not in st.session_state["include_domains"]:
                st.session_state["include_domains"].append(new_domain)

    # 현재 등록된 도메인 목록 표시
    st.write("등록된 도메인 목록:")
    for idx, domain in enumerate(st.session_state["include_domains"]):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(domain)
        with col2:
            if st.button("삭제", key=f"del_{idx}"):
                st.session_state["include_domains"].pop(idx)
                st.rerun()

    # 설정 버튼
    apply_btn = st.button("설정 완료", type="primary")


@dataclass
class ChatMessageWithType:
    chat_message: ChatMessage
    msg_type: str
    tool_name: str


# 이전 대화를 출력
def print_messages():
    for message in st.session_state["messages"]:
        if message.msg_type == "text":
            st.chat_message(message.chat_message.role).write(
                message.chat_message.content
            )
        elif message.msg_type == "tool_result":
            with st.expander(f"✅ {message.tool_name}"):
                st.markdown(message.chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message, msg_type="text", tool_name=""):
    if msg_type == "text":
        st.session_state["messages"].append(
            ChatMessageWithType(
                chat_message=ChatMessage(role=role, content=message),
                msg_type="text",
                tool_name=tool_name,
            )
        )
    elif msg_type == "tool_result":
        st.session_state["messages"].append(
            ChatMessageWithType(
                chat_message=ChatMessage(
                    role="assistant", content=format_search_result(message)
                ),
                msg_type="tool_result",
                tool_name=tool_name,
            )
        )


# 초기화 버튼이 눌리면...
if clear_btn:
    st.session_state["messages"] = []
    st.session_state["thread_id"] = random_uuid()
# 이전 대화 기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 경고 메시지를 띄우기 위한 빈 영역
warning_msg = st.empty()

# 설정 버튼이 눌리면...
if apply_btn:
    tool = WebSearchTool().create()
    tool.max_results = search_result_count
    tool.include_domains = st.session_state["include_domains"]
    tool.topic = search_topic
    st.session_state["react_agent"] = create_agent_executor(
        model_name=selected_model,
        tools=[tool],
    )
    st.session_state["thread_id"] = random_uuid()

# 만약에 사용자 입력이 들어오면...
if user_input:
    agent = st.session_state["react_agent"]
    # Config 설정

    if agent is not None:
        config = {"configurable": {"thread_id": st.session_state["thread_id"]}}
        # 사용자의 입력
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            # 빈 공간(컨테이너)을 만들어서, 여기에 토큰을 스트리밍 출력한다.
            container = st.empty()

            ai_answer = ""
            container_messages, tool_args, agent_answer = stream_handler(
                container,
                agent,
                {
                    "messages": [
                        ("human", user_input),
                    ]
                },
                config,
            )

            # 대화기록을 저장한다.
            add_message("user", user_input)
            for tool_arg in tool_args:
                add_message(
                    "assistant",
                    tool_arg["tool_result"],
                    "tool_result",
                    tool_arg["tool_name"],
                )
            add_message("assistant", agent_answer)
    else:
        warning_msg.warning("사이드바에서 설정을 완료해주세요.")
````

## File: pyproject.toml
````toml
[tool.poetry]
name = "fastcampus-perplexity-clone"
version = "0.1.0"
description = ""
authors = ["teddy <teddylee777@gmail.com>"]
license = "Apache 2.0"
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
python = ">=3.11,<=3.13"
langchain = "^0.3.13"
langgraph = "^0.2.60"
langchain-openai = "^0.2.14"
jupyter = "^1.1.1"
notebook = "^7.3.1"
streamlit = "^1.41.1"
langchain-teddynote = "^0.3.40"
python-dotenv = "^1.0.1"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
````

## File: README.md
````markdown
# 프로젝트 소개

본 프로젝트는 Fastcampus 강의 중 제공되는 프로젝트 입니다.

- 강의: [RAG 비법노트](https://fastcampus.co.kr/data_online_teddy)
- 프로젝트 링크: https://link.teddynote.com/PERPLEX


## 설치

다음의 명령어로 가상환경을 활성화 합니다.

```bash
poetry shell
```

패키지를 설치합니다.

```bash
poetry install
```

## 실행

```bash
poetry run streamlit run main.py
```

## 스트림릿에 배포

1. 다음의 [링크](https://share.streamlit.io/)로 접속합니다.
2. 계정을 생성 합니다.
3. 우측 상단의 "Create app" 버튼을 클릭합니다.
4. "Deploy a public app from GitHub" 버튼을 클릭합니다.
5. 본인의 "Repository" 를 입력합니다. 링크를 입력합니다.
6. Main file path 는 "main.py" 입니다.
7. "Advanced settings" 를 클릭합니다.
    - `Python version` 은 3.11 을 선택합니다.
    - `Secrets` 에 API KEY 를 입력합니다.
    - "Save" 버튼을 클릭합니다.
8. "Deploy" 버튼을 클릭합니다.
````
