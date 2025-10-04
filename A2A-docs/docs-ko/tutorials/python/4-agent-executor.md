# 4. 에이전트 실행기 (Agent Executor)

A2A 에이전트가 요청을 처리하고 응답/이벤트를 생성하는 핵심 로직은 **에이전트 실행기(Agent Executor)**에 의해 처리됩니다. A2A Python SDK는 여러분이 구현해야 하는 추상 기본 클래스 `a2a.server.agent_execution.AgentExecutor`를 제공합니다.

## `AgentExecutor` 인터페이스

`AgentExecutor` 클래스는 두 가지 주요 메서드를 정의합니다:

- `async def execute(self, context: RequestContext, event_queue: EventQueue)`: 응답 또는 이벤트 스트림을 예상하는 들어오는 요청을 처리합니다. `context`를 통해 사용 가능한 사용자 입력을 처리하고, `event_queue`를 사용하여 `Message`, `Task`, `TaskStatusUpdateEvent`, 또는 `TaskArtifactUpdateEvent` 객체를 다시 보냅니다.
- `async def cancel(self, context: RequestContext, event_queue: EventQueue)`: 진행 중인 작업을 취소하라는 요청을 처리합니다.

`RequestContext`는 사용자의 메시지 및 기존 작업 세부 정보와 같이 들어오는 요청에 대한 정보를 제공합니다. `EventQueue`는 실행기가 클라이언트에 이벤트를 다시 보내는 데 사용됩니다.

## Helloworld 에이전트 실행기

`agent_executor.py` 파일을 살펴보겠습니다. 이 파일은 `HelloWorldAgentExecutor`를 정의합니다.

1.  **에이전트 (`HelloWorldAgent`)**:
    실제 "비즈니스 로직"을 캡슐화하는 간단한 헬퍼 클래스입니다.

    ```python { .no-copy }
    --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/agent_executor.py:HelloWorldAgent"
    ```

    "Hello World" 문자열을 반환하는 간단한 `invoke` 메서드를 가지고 있습니다.

2.  **실행기 (`HelloWorldAgentExecutor`)**:
    이 클래스는 `AgentExecutor` 인터페이스를 구현합니다.

    - **`__init__`**:

        ```python { .no-copy }
        --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/agent_executor.py:HelloWorldAgentExecutor_init"
        ```

        `HelloWorldAgent`를 인스턴스화합니다.

    - **`execute`**:

        ```python { .no-copy }
        --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/agent_executor.py:HelloWorldAgentExecutor_execute"
        ```

        `message/send` 또는 `message/stream` 요청이 들어오면 (이 단순화된 실행기에서는 둘 다 `execute`에 의해 처리됨):

        1.  `self.agent.invoke()`를 호출하여 "Hello World" 문자열을 가져옵니다.
        2.  `new_agent_text_message` 유틸리티 함수를 사용하여 A2A `Message` 객체를 생성합니다.
        3.  이 메시지를 `event_queue`에 추가합니다. 그러면 기본 `DefaultRequestHandler`가 이 큐를 처리하여 클라이언트에 응답을 보냅니다. 이와 같은 단일 메시지의 경우, 스트림이 닫히기 전에 `message/send`에 대한 단일 응답 또는 `message/stream`에 대한 단일 이벤트가 발생합니다.

    - **`cancel`**:
        Helloworld 예제의 `cancel` 메서드는 단순히 예외를 발생시켜 이 기본 에이전트에 대해서는 취소가 지원되지 않음을 나타냅니다.

        ```python { .no-copy }
        --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/agent_executor.py:HelloWorldAgentExecutor_cancel"
        ```

`AgentExecutor`는 A2A 프로토콜(요청 핸들러 및 서버 애플리케이션에 의해 관리됨)과 에이전트의 특정 로직 사이의 다리 역할을 합니다. 요청에 대한 컨텍스트를 수신하고 이벤트 큐를 사용하여 결과 또는 업데이트를 다시 전달합니다.
