---
title: Building Consistent Workflows with Codex CLI & Agents SDK | OpenAI Cookbook
source: https://cookbook.openai.com/examples/codex/codex_mcp_agents_sdk/building_consistent_workflows_codex_cli_agents_sdk?utm_source=codenewsletter.ai&utm_medium=newsletter&utm_campaign=google-and-aws-race-to-unify-enterprise-ai-developers-finally-get-distribution&_bhlid=505ff46a0f3cbbfe22934e0a1cdc1d5ea80c52e3
author:
published: 2025-10-01
created: 2025-10-25 00:00:00
description: 개발자들은 모든 작업에서 일관성을 추구합니다. Codex CLI와 에이전트 SDK를 통해 이제 그 일관성이 그 어느 때보다 확장될 수 있습니다.
tags: []
summary:
updated: 2025-10-25 10:41:07
---
### 반복 가능하고 추적 가능하며 확장 가능한 에이전트 개발 보장

## 소개

개발자는 모든 작업에서 일관성을 유지하기 위해 노력합니다. Codex CLI와 Agents SDK를 사용하면 이러한 일관성을 이전과는 비교할 수 없을 정도로 확장할 수 있습니다. 대규모 코드베이스를 리팩토링하거나, 새로운 기능을 출시하거나, 새로운 테스트 프레임워크를 도입하는 경우, Codex는 CLI, IDE 및 클라우드 워크플로에 완벽하게 통합되어 반복 가능한 개발 패턴을 자동화하고 적용합니다.

이 트랙에서는 Agents SDK를 사용하여 단일 및 다중 에이전트 시스템을 구축하고, Codex CLI를 MCP 서버로 노출합니다. 이를 통해 다음과 같은 기능을 구현할 수 있습니다.

- 각 에이전트에게 범위가 정해진 맥락을 제공함으로써 **일관성과 반복성을 확보합니다.**
- 단일 및 다중 에이전트 시스템을 조정하기 위한 **확장 가능한 오케스트레이션.**
- 전체 에이전트 스택 추적을 검토하여 **관찰성과 감사성을 확보합니다.**

## 우리가 다룰 내용

- Codex CLI를 MCP 서버로 초기화: Codex를 장기 실행 MCP 프로세스로 실행하는 방법.
- 단일 에이전트 시스템 구축: 범위가 지정된 작업에 Codex MCP 사용.
- 다중 에이전트 워크플로우 조율: 여러 전문 에이전트를 조정합니다.
- 에이전트 행동 추적: 가시성과 평가를 위해 에이전트 추적을 활용합니다.

## 필수 구성 요소 및 설정

이 트랙을 시작하기 전에 다음 사항이 있는지 확인하세요.

- 기본 코딩 지식: Python과 JavaScript에 익숙해야 합니다.
- 개발자 환경: VS Code나 Cursor와 같은 IDE가 필요합니다.
- OpenAI API 키: OpenAI 대시보드에서 API 키를 만들거나 찾으세요.

## 환경 설정

1. `.env` 디렉토리에 폴더를 만들고 `OPENAI_API_KEY` 키를 추가하세요
2. 종속성 설치

```
%pip install openai-agents openai ## install dependencies
```

## MCP 서버로 Codex CLI 초기화

Agents SDK 내에서 Codex CLI를 MCP 서버로 실행합니다. 의 초기화 매개변수를 제공합니다 `codex mcp`. 이 명령은 Codex CLI를 MCP 서버로 시작하고 MCP 서버에서 사용 가능한 두 가지 Codex 도구( `codex()` 와 ) 를 노출합니다 `codex-reply()`. 이 도구들은 Agents SDK가 Codex를 호출할 때 호출하는 기본 도구입니다.

- `codex()` 대화를 만드는 데 사용됩니다.
- `codex-reply()` 대화를 계속하기 위한 것입니다.

```python
import asyncio

from agents import Agent, Runner

from agents.mcp import MCPServerStdio

 

async def main() -> None:

    async with MCPServerStdio(

        name="Codex CLI",

        params={

            "command": "npx",

            "args": ["-y", "codex", "mcp"],

        },

        client_session_timeout_seconds=360000,

    ) as codex_mcp_server:

        print("Codex MCP server started.")

        # We will add more code here in the next section

        return
```

또한 Codex CLI가 주어진 작업을 실행하고 완료할 수 있도록 충분한 시간을 제공하기 위해 MCP 서버 시간 제한을 연장하고 있습니다.

---

## 단일 에이전트 시스템 구축

Codex MCP 서버를 사용하는 간단한 예제부터 시작해 보겠습니다. 두 개의 에이전트를 정의합니다.

1. **디자이너 에이전트** – 게임에 대한 간단한 브리핑을 하고 아이디어를 냅니다.
2. **개발자 에이전트** – 디자이너의 사양에 따라 간단한 게임을 구현합니다.

```python
developer_agent = Agent(

    name="Game Developer",

    instructions=(

        "You are an expert in building simple games using basic html + css + javascript with no dependencies. "

        "Save your work in a file called index.html in the current directory."

        "Always call codex with \"approval-policy\": \"never\" and \"sandbox\": \"workspace-write\""

    ),

    mcp_servers=[codex_mcp_server],

)

 

designer_agent = Agent(

    name="Game Designer",

    instructions=(

        "You are an indie game connoisseur. Come up with an idea for a single page html + css + javascript game that a developer could build in about 50 lines of code. "

        "Format your request as a 3 sentence design brief for a game developer and call the Game Developer coder with your idea."

    ),

    model="gpt-5",

    handoffs=[developer_agent],

)

 

result = await Runner.run(designer_agent, "Implement a fun new game!")
```

개발자 에이전트가 사용자에게 권한을 묻지 않고도 프로젝트 디렉토리에 파일을 쓸 수 있는 기능을 제공한다는 점에 유의하세요.

이제 코드를 실행하면 `index.html` 파일이 생성된 것을 볼 수 있습니다. 파일을 열고 게임을 시작해 보세요!

Here’s a few screenshots of the game my agentic system created. Yours will be different!

| Example gameplay | Game Over Score |
| --- | --- |
| ![게임플레이 예시](https://cookbook.openai.com/images/game_example_1.png) | ![게임 오버 점수](https://cookbook.openai.com/images/game_example_2.png) |

Here's the full executable code. Note that it might take a few minutes to run. It will have run successfully if you see an index.html file produced. You might also see some MCP events warnings about format. You can ignore these events.

```
import os

from dotenv import load_dotenv

import asyncio

from agents import Agent, Runner, set_default_openai_api

from agents.mcp import MCPServerStdio

load_dotenv(override=True) # load the API key from the .env file. We set override to True here to ensure the notebook is loading any changes

set_default_openai_api(os.getenv("OPENAI_API_KEY"))

async def main() -> None:

    async with MCPServerStdio(

        name="Codex CLI",

        params={

            "command": "npx",

            "args": ["-y", "codex", "mcp"],

        },

        client_session_timeout_seconds=360000,

    ) as codex_mcp_server:

        developer_agent = Agent(

            name="Game Developer",

            instructions=(

                "You are an expert in building simple games using basic html + css + javascript with no dependencies. "

                "Save your work in a file called index.html in the current directory."

                "Always call codex with \"approval-policy\": \"never\" and \"sandbox\": \"workspace-write\""

            ),

            mcp_servers=[codex_mcp_server],

        )

        designer_agent = Agent(

            name="Game Designer",

            instructions=(

                "You are an indie game connoisseur. Come up with an idea for a single page html + css + javascript game that a developer could build in about 50 lines of code. "

                "Format your request as a 3 sentence design brief for a game developer and call the Game Developer coder with your idea."

            ),

            model="gpt-5",

            handoffs=[developer_agent],

        )

        result = await Runner.run(designer_agent, "Implement a fun new game!")

        # print(result.final_output)

if __name__ == "__main__":

    # Jupyter/IPython already runs an event loop, so calling asyncio.run() here

    # raises "asyncio.run() cannot be called from a running event loop".

    # Workaround: if a loop is running (notebook), use top-level \`await\`; otherwise use asyncio.run().

    try:

        asyncio.get_running_loop()

        await main()

    except RuntimeError:

        asyncio.run(main())
```

---

## Orchestrating Multi-Agent Workflows

For larger workflows, we introduce a team of agents:

- **Project Manager**: Breaks down task list, creates requirements, and coordinates work.
- **Designer**: Produces UI/UX specifications.
- **Frontend Developer**: Implements UI/UX.
- **Backend Developer**: Implements APIs and logic.
- **Tester**: Validates outputs against acceptance criteria.

In this example, we intentionally have the Project Manager agent enforce gating logic between each of the specialized downstream agents. This ensures that artifacts exist before handoffs are made. This mirrors real world enterprise workflows such as JIRA task orchestration, long-chained rollouts, and QA sign-offs.

![Codex MCP를 사용한 다중 에이전트 Codex 워크플로](https://cookbook.openai.com/images/multi_agent_codex_workflow.png)  
*Multi-agent orchestration with Codex MCP and gated handoffs producing artifacts.*

In this structure, each of our agents serve a specialized purpose. The Project Manager is overall responsible for coordinating across all other agents and ensuring the overall task is complete.

## Define the Codex CLI MCP Server

We set up our MCP Server to initialize Codex CLI just as we did in the single agent example.

```python
async def main() -> None:

    async with MCPServerStdio(

        name="Codex CLI",

        params={

            "command": "npx",

            "args": ["-y", "codex", "mcp"],

        },

        client_session_timeout_seconds=360000,

    ) as codex_mcp_server:

        print("Codex MCP server started.")

        # We will add more code here in the next section

        return
```

## Define each specialized agent

Below we define each of our specialized agents and provide access to our Codex MCP server. Notice that we are also passing the `RECOMMMENDED_PROMPT_PREFIX` to each agent that helps the system optimize for handoffs between agents.

```python
# Downstream agents are defined first for clarity, then PM references them in handoffs.

designer_agent = Agent(

    name="Designer",

    instructions=(

        f"""{RECOMMENDED_PROMPT_PREFIX}"""

        "You are the Designer.\n"

        "Your only source of truth is AGENT_TASKS.md and REQUIREMENTS.md from the Project Manager.\n"

        "Do not assume anything that is not written there.\n\n"

        "You may use the internet for additional guidance or research."

        "Deliverables (write to /design):\n"

        "- design_spec.md – a single page describing the UI/UX layout, main screens, and key visual notes as requested in AGENT_TASKS.md.\n"

        "- wireframe.md – a simple text or ASCII wireframe if specified.\n\n"

        "Keep the output short and implementation-friendly.\n"

        "When complete, handoff to the Project Manager with transfer_to_project_manager."

        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

    ),

    model="gpt-5",

    tools=[WebSearchTool()],

    mcp_servers=[codex_mcp_server],

    handoffs=[],

)

 

frontend_developer_agent = Agent(

    name="Frontend Developer",

    instructions=(

        f"""{RECOMMENDED_PROMPT_PREFIX}"""

        "You are the Frontend Developer.\n"

        "Read AGENT_TASKS.md and design_spec.md. Implement exactly what is described there.\n\n"

        "Deliverables (write to /frontend):\n"

        "- index.html – main page structure\n"

        "- styles.css or inline styles if specified\n"

        "- main.js or game.js if specified\n\n"

        "Follow the Designer’s DOM structure and any integration points given by the Project Manager.\n"

        "Do not add features or branding beyond the provided documents.\n\n"

        "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."

        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

    ),

    model="gpt-5",

    mcp_servers=[codex_mcp_server],

    handoffs=[],

)

 

backend_developer_agent = Agent(

    name="Backend Developer",

    instructions=(

        f"""{RECOMMENDED_PROMPT_PREFIX}"""

        "You are the Backend Developer.\n"

        "Read AGENT_TASKS.md and REQUIREMENTS.md. Implement the backend endpoints described there.\n\n"

        "Deliverables (write to /backend):\n"

        "- package.json – include a start script if requested\n"

        "- server.js – implement the API endpoints and logic exactly as specified\n\n"

        "Keep the code as simple and readable as possible. No external database.\n\n"

        "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."

        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

    ),

    model="gpt-5",

    mcp_servers=[codex_mcp_server],

    handoffs=[],

)

 

tester_agent = Agent(

    name="Tester",

    instructions=(

        f"""{RECOMMENDED_PROMPT_PREFIX}"""

        "You are the Tester.\n"

        "Read AGENT_TASKS.md and TEST.md. Verify that the outputs of the other roles meet the acceptance criteria.\n\n"

        "Deliverables (write to /tests):\n"

        "- TEST_PLAN.md – bullet list of manual checks or automated steps as requested\n"

        "- test.sh or a simple automated script if specified\n\n"

        "Keep it minimal and easy to run.\n\n"

        "When complete, handoff to the Project Manager with transfer_to_project_manager."

        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

    ),

    model="gpt-5",

    mcp_servers=[codex_mcp_server],

    handoffs=[],

)
```

After each role completes its assignment, it will call `transfer_to_project_manager_agent`, and let the Project Manager confirm that the required files exist (or request fixes) before unblocking the next team.

## Define Project Manager Agent

The Project Manager is the only agent that receives the initial prompt, creates the planning documents in the project directory, and enforces the gatekeeping logic before every transfer.

```python
project_manager_agent = Agent(

name="Project Manager",

instructions=(

    f"""{RECOMMENDED_PROMPT_PREFIX}"""

    """

    You are the Project Manager.

 

    Objective:

    Convert the input task list into three project-root files the team will execute against.

 

    Deliverables (write in project root):

    - REQUIREMENTS.md: concise summary of product goals, target users, key features, and constraints.

    - TEST.md: tasks with [Owner] tags (Designer, Frontend, Backend, Tester) and clear acceptance criteria.

    - AGENT_TASKS.md: one section per role containing:

        - Project name

        - Required deliverables (exact file names and purpose)

        - Key technical notes and constraints

 

    Process:

    - Resolve ambiguities with minimal, reasonable assumptions. Be specific so each role can act without guessing.

    - Create files using Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"}.

    - Do not create folders. Only create REQUIREMENTS.md, TEST.md, AGENT_TASKS.md.

 

    Handoffs (gated by required files):

    1) After the three files above are created, hand off to the Designer with transfer_to_designer_agent and include REQUIREMENTS.md, and AGENT_TASKS.md.

    2) Wait for the Designer to produce /design/design_spec.md. Verify that file exists before proceeding.

    3) When design_spec.md exists, hand off in parallel to both:

        - Frontend Developer with transfer_to_frontend_developer_agent (provide design_spec.md, REQUIREMENTS.md, AGENT_TASKS.md).

        - Backend Developer with transfer_to_backend_developer_agent (provide REQUIREMENTS.md, AGENT_TASKS.md).

    4) Wait for Frontend to produce /frontend/index.html and Backend to produce /backend/server.js. Verify both files exist.

    5) When both exist, hand off to the Tester with transfer_to_tester_agent and provide all prior artifacts and outputs.

    6) Do not advance to the next handoff until the required files for that step are present. If something is missing, request the owning agent to supply it and re-check.

 

    PM Responsibilities:

    - Coordinate all roles, track file completion, and enforce the above gating checks.

    - Do NOT respond with status updates. Just handoff to the next agent until the project is complete.

    """

),

model="gpt-5",

model_settings=ModelSettings(

    reasoning=Reasoning(effort="medium")

),

handoffs=[designer_agent, frontend_developer_agent, backend_developer_agent, tester_agent],

mcp_servers=[codex_mcp_server],

)
```

After constructing the Project Manager, the script sets every specialist's handoffs back to the Project Manager. This ensures deliverables return for validation before moving on.

```python
designer_agent.handoffs = [project_manager_agent]

frontend_developer_agent.handoffs = [project_manager_agent]

backend_developer_agent.handoffs = [project_manager_agent]

tester_agent.handoffs = [project_manager_agent]
```

## Add in your task list

This is the task that the Project Manager will refine into specific requirements and tasks for the entire system.

```python
task_list = """

Goal: Build a tiny browser game to showcase a multi-agent workflow.

 

High-level requirements:

- Single-screen game called "Bug Busters".

- Player clicks a moving bug to earn points.

- Game ends after 20 seconds and shows final score.

- Optional: submit score to a simple backend and display a top-10 leaderboard.

 

Roles:

- Designer: create a one-page UI/UX spec and basic wireframe.

- Frontend Developer: implement the page and game logic.

- Backend Developer: implement a minimal API (GET /health, GET/POST /scores).

- Tester: write a quick test plan and a simple script to verify core routes.

 

Constraints:

- No external database—memory storage is fine.

- Keep everything readable for beginners; no frameworks required.

- All outputs should be small files saved in clearly named folders.

"""
```

Next, run your system, sit back, and you’ll see the agents go to work and create a game in a few minutes! We've included the fully executable code below. Once it's finished, you'll notice the creation of the following files directory. Note that this multi-agent orchestration usually took about 11 mintues to fully complete.

```markdown
root_directory/

├── AGENT_TASKS.md

├── REQUIREMENTS.md

├── backend

│   ├── package.json

│   └── server.js

├── design

│   ├── design_spec.md

│   └── wireframe.md

├── frontend

│   ├── game.js

│   ├── index.html

│   └── styles.css

└── TEST.md
```

Start your backend server with `node server.js` and open your `index.html` file to play your game.

```
import os

from dotenv import load_dotenv

import asyncio

from agents import Agent, Runner, WebSearchTool, ModelSettings, set_default_openai_api

from agents.mcp import MCPServerStdio

from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from openai.types.shared import Reasoning

load_dotenv(override=True) # load the API key from the .env file. We set override to True here to ensure the notebook is loading any changes

set_default_openai_api(os.getenv("OPENAI_API_KEY"))

async def main() -> None:

    async with MCPServerStdio(

        name="Codex CLI",

        params={"command": "npx", "args": ["-y", "codex", "mcp"]},

        client_session_timeout_seconds=360000,

    ) as codex_mcp_server:

        # Downstream agents are defined first for clarity, then PM references them in handoffs.

        designer_agent = Agent(

            name="Designer",

            instructions=(

                f"""{RECOMMENDED_PROMPT_PREFIX}"""

                "You are the Designer.\n"

                "Your only source of truth is AGENT_TASKS.md and REQUIREMENTS.md from the Project Manager.\n"

                "Do not assume anything that is not written there.\n\n"

                "You may use the internet for additional guidance or research."

                "Deliverables (write to /design):\n"

                "- design_spec.md – a single page describing the UI/UX layout, main screens, and key visual notes as requested in AGENT_TASKS.md.\n"

                "- wireframe.md – a simple text or ASCII wireframe if specified.\n\n"

                "Keep the output short and implementation-friendly.\n"

                "When complete, handoff to the Project Manager with transfer_to_project_manager."

                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

            ),

            model="gpt-5",

            tools=[WebSearchTool()],

            mcp_servers=[codex_mcp_server],

            handoffs=[],

        )

        frontend_developer_agent = Agent(

            name="Frontend Developer",

            instructions=(

                f"""{RECOMMENDED_PROMPT_PREFIX}"""

                "You are the Frontend Developer.\n"

                "Read AGENT_TASKS.md and design_spec.md. Implement exactly what is described there.\n\n"

                "Deliverables (write to /frontend):\n"

                "- index.html – main page structure\n"

                "- styles.css or inline styles if specified\n"

                "- main.js or game.js if specified\n\n"

                "Follow the Designer’s DOM structure and any integration points given by the Project Manager.\n"

                "Do not add features or branding beyond the provided documents.\n\n"

                "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."

                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

            ),

            model="gpt-5",

            mcp_servers=[codex_mcp_server],

            handoffs=[],

        )

        backend_developer_agent = Agent(

            name="Backend Developer",

            instructions=(

                f"""{RECOMMENDED_PROMPT_PREFIX}"""

                "You are the Backend Developer.\n"

                "Read AGENT_TASKS.md and REQUIREMENTS.md. Implement the backend endpoints described there.\n\n"

                "Deliverables (write to /backend):\n"

                "- package.json – include a start script if requested\n"

                "- server.js – implement the API endpoints and logic exactly as specified\n\n"

                "Keep the code as simple and readable as possible. No external database.\n\n"

                "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."

                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

            ),

            model="gpt-5",

            mcp_servers=[codex_mcp_server],

            handoffs=[],

        )

        tester_agent = Agent(

            name="Tester",

            instructions=(

                f"""{RECOMMENDED_PROMPT_PREFIX}"""

                "You are the Tester.\n"

                "Read AGENT_TASKS.md and TEST.md. Verify that the outputs of the other roles meet the acceptance criteria.\n\n"

                "Deliverables (write to /tests):\n"

                "- TEST_PLAN.md – bullet list of manual checks or automated steps as requested\n"

                "- test.sh or a simple automated script if specified\n\n"

                "Keep it minimal and easy to run.\n\n"

                "When complete, handoff to the Project Manager with transfer_to_project_manager."

                "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."

            ),

            model="gpt-5",

            mcp_servers=[codex_mcp_server],

            handoffs=[],

        )

        project_manager_agent = Agent(

            name="Project Manager",

            instructions=(

                f"""{RECOMMENDED_PROMPT_PREFIX}"""

                """

                You are the Project Manager.

                Objective:

                Convert the input task list into three project-root files the team will execute against.

                Deliverables (write in project root):

                - REQUIREMENTS.md: concise summary of product goals, target users, key features, and constraints.

                - TEST.md: tasks with [Owner] tags (Designer, Frontend, Backend, Tester) and clear acceptance criteria.

                - AGENT_TASKS.md: one section per role containing:

                  - Project name

                  - Required deliverables (exact file names and purpose)

                  - Key technical notes and constraints

                Process:

                - Resolve ambiguities with minimal, reasonable assumptions. Be specific so each role can act without guessing.

                - Create files using Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"}.

                - Do not create folders. Only create REQUIREMENTS.md, TEST.md, AGENT_TASKS.md.

                Handoffs (gated by required files):

                1) After the three files above are created, hand off to the Designer with transfer_to_designer_agent and include REQUIREMENTS.md, and AGENT_TASKS.md.

                2) Wait for the Designer to produce /design/design_spec.md. Verify that file exists before proceeding.

                3) When design_spec.md exists, hand off in parallel to both:

                   - Frontend Developer with transfer_to_frontend_developer_agent (provide design_spec.md, REQUIREMENTS.md, AGENT_TASKS.md).

                   - Backend Developer with transfer_to_backend_developer_agent (provide REQUIREMENTS.md, AGENT_TASKS.md).

                4) Wait for Frontend to produce /frontend/index.html and Backend to produce /backend/server.js. Verify both files exist.

                5) When both exist, hand off to the Tester with transfer_to_tester_agent and provide all prior artifacts and outputs.

                6) Do not advance to the next handoff until the required files for that step are present. If something is missing, request the owning agent to supply it and re-check.

                PM Responsibilities:

                - Coordinate all roles, track file completion, and enforce the above gating checks.

                - Do NOT respond with status updates. Just handoff to the next agent until the project is complete.

                """

            ),

            model="gpt-5",

            model_settings=ModelSettings(

                reasoning=Reasoning(effort="medium")

            ),

            handoffs=[designer_agent, frontend_developer_agent, backend_developer_agent, tester_agent],

            mcp_servers=[codex_mcp_server],

        )

        designer_agent.handoffs = [project_manager_agent]

        frontend_developer_agent.handoffs = [project_manager_agent]

        backend_developer_agent.handoffs = [project_manager_agent]

        tester_agent.handoffs = [project_manager_agent]

        # Example task list input for the Project Manager

        task_list = """

Goal: Build a tiny browser game to showcase a multi-agent workflow.

High-level requirements:

- Single-screen game called "Bug Busters".

- Player clicks a moving bug to earn points.

- Game ends after 20 seconds and shows final score.

- Optional: submit score to a simple backend and display a top-10 leaderboard.

Roles:

- Designer: create a one-page UI/UX spec and basic wireframe.

- Frontend Developer: implement the page and game logic.

- Backend Developer: implement a minimal API (GET /health, GET/POST /scores).

- Tester: write a quick test plan and a simple script to verify core routes.

Constraints:

- No external database—memory storage is fine.

- Keep everything readable for beginners; no frameworks required.

- All outputs should be small files saved in clearly named folders.

"""

        # Only the Project Manager receives the task list directly

        result = await Runner.run(project_manager_agent, task_list, max_turns=30)

        print(result.final_output)

if __name__ == "__main__":

    # Jupyter/IPython already runs an event loop, so calling asyncio.run() here

    # raises "asyncio.run() cannot be called from a running event loop".

    # Workaround: if a loop is running (notebook), use top-level \`await\`; otherwise use asyncio.run().

    try:

        asyncio.get_running_loop()

        await main()

    except RuntimeError:

        asyncio.run(main())
```

---

## Tracing the agentic behavior using Traces

에이전트 시스템이 복잡해질수록 이러한 에이전트들이 어떻게 상호작용하는지 파악하는 것이 중요합니다. 이를 위해 다음을 기록하는 추적 대시보드를 활용할 수 있습니다.

- 에이전트 간의 프롬프트, 도구 호출 및 인계.
- MCP 서버 호출, Codex CLI 호출, 실행 시간 및 파일 쓰기.
- 오류 및 경고.

위의 에이전트 팀에 대한 에이전트 추적을 살펴보겠습니다.

![Codex MCP를 사용한 다중 에이전트 Codex 워크플로](https://cookbook.openai.com/images/multi_agent_trace.png)

이 추적을 통해 모든 에이전트 핸드오프가 프로젝트 관리자 에이전트의 감독 하에 다음 에이전트에게 핸드오프되기 전에 특정 아티팩트가 존재하는지 확인하는 것을 확인할 수 있습니다. 또한, Codex MCP 서버의 특정 혁신 사항을 확인하고 Responses API를 호출하여 각 출력을 생성할 수 있습니다. 타임라인 막대는 실행 기간을 강조 표시하여 장시간 실행되는 단계를 쉽게 파악하고 에이전트 간 제어 전달 방식을 파악할 수 있도록 합니다.

각 추적을 클릭하면 프롬프트, 도구 호출 및 기타 메타데이터의 구체적인 세부 정보를 확인할 수 있습니다. 시간이 지남에 따라 이 정보를 확인하여 에이전트 시스템 성능을 더욱 세부적으로 조정, 최적화 및 추적할 수 있습니다.

![다중 에이전트 추적 세부 정보](https://cookbook.openai.com/images/multi_agent_trace_details.png)

---

## 이 가이드에서 우리가 한 일의 요약

이 가이드에서는 Codex CLI와 Agents SDK를 사용하여 일관되고 확장 가능한 워크플로를 구축하는 과정을 살펴보았습니다. 구체적으로 다음 내용을 다루었습니다.

- **Codex MCP 서버 설정** – Codex CLI를 MCP 서버로 초기화하고 에이전트 상호작용을 위한 도구로 사용할 수 있도록 하는 방법.
- **단일 에이전트 예시** – 디자이너 에이전트와 개발자 에이전트가 있는 간단한 워크플로에서 Codex는 범위가 지정된 작업을 결정적으로 실행하여 플레이 가능한 게임을 제작했습니다.
- **다중 에이전트 오케스트레이션** – 프로젝트 관리자, 디자이너, 프런트엔드 개발자, 백엔드 개발자, 테스터를 통해 더 큰 워크플로로 확장하여 복잡한 작업 오케스트레이션 및 승인 프로세스를 미러링합니다.
- **추적 및 관찰성** – 내장된 추적 기능을 사용하여 프롬프트, 도구 호출, 핸드오프, 실행 시간 및 아티팩트를 캡처하여 디버깅, 평가 및 향후 최적화를 위한 에이전트 동작에 대한 완전한 가시성을 제공합니다.

---

## 앞으로 나아가기: 이러한 교훈을 적용하기

이제 Codex MCP와 Agents SDK가 실제로 어떻게 활용되는지 살펴보았으니, 실제 프로젝트에 개념을 적용하여 가치를 추출하는 방법을 알아보겠습니다.

### 1\. 실제 롤아웃으로 확장

- 대규모 코드 리팩토링(예: 500개 이상의 파일, 프레임워크 마이그레이션)에 동일한 다중 에이전트 오케스트레이션을 적용합니다.
- 추적 가능한 진행 상황을 갖춘 장기적이고 감사 가능한 롤아웃을 위해 Codex MCP의 결정론적 실행을 활용하세요.

### 2\. 통제력을 잃지 않고 배달을 가속화하세요

- 아티팩트 검증을 위한 게이팅 논리를 유지하면서 개발을 병렬화하기 위해 전문 에이전트 팀을 구성합니다.
- 새로운 기능, 테스트 또는 코드베이스 현대화에 걸리는 처리 시간을 줄입니다.

### 3\. 개발 워크플로 확장 및 연결

- 웹후크를 통해 MCP 기반 에이전트를 Jira, GitHub 또는 CI/CD 파이프라인과 연결하여 자동화되고 반복 가능한 개발 주기를 구현합니다.
- 다중 에이전트 서비스 오케스트레이션에서 Codex MCP를 활용하세요. 코드 생성뿐만 아니라 문서화, QA, 배포에도 활용하세요.