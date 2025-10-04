# 7. 스트리밍 및 다중 회차(Multi-Turn) 상호작용 (LangGraph 예제)

Helloworld 예제는 A2A의 기본 메커니즘을 보여줍니다. 강력한 스트리밍, 작업 상태 관리, LLM 기반의 다중 회차 대화와 같은 고급 기능을 위해서는 [`a2a-samples/samples/python/agents/langgraph/`](https://github.com/google-a2a/a2a-samples/tree/main/samples/python/agents/langgraph)에 위치한 LangGraph 예제를 살펴보겠습니다.

이 예제는 LangChain 및 LangGraph를 통해 Gemini 모델을 사용하여 환전 질문에 답변하는 "통화 에이전트(Currency Agent)"를 특징으로 합니다.

## LangGraph 예제 설정하기

1.  아직 없다면 [Gemini API 키](https://ai.google.dev/gemini-api/docs/api-key)를 생성합니다.

2.  **환경 변수:**

    `a2a-samples/samples/python/agents/langgraph/` 디렉토리에 `.env` 파일을 생성합니다:

    ```bash
    echo "GOOGLE_API_KEY=YOUR_API_KEY_HERE" > .env
    ```

    `YOUR_API_KEY_HERE`를 실제 Gemini API 키로 교체합니다.

3.  **의존성 설치 (아직 설치되지 않은 경우):**

    `langgraph` 예제에는 `langchain-google-genai` 및 `langgraph`와 같은 의존성을 포함하는 자체 `pyproject.toml` 파일이 있습니다. `pip install -e .[dev]`를 사용하여 `a2a-samples` 루트에서 SDK를 설치했다면, `langgraph-example`을 포함한 워크스페이스 예제의 의존성도 설치되었어야 합니다. 만약 임포트 오류가 발생하면, 루트 디렉토리에서 기본 SDK 설치가 성공적으로 완료되었는지 확인하십시오.

## LangGraph 서버 실행하기

터미널에서 `a2a-samples/samples/python/agents/langgraph/app` 디렉토리로 이동한 후, (SDK 루트의) 가상 환경이 활성화되어 있는지 확인합니다.

LangGraph 에이전트 서버를 시작합니다:

```bash
python __main__.py
```

이렇게 하면 보통 `http://localhost:10000`에서 서버가 시작됩니다.

## LangGraph 에이전트와 상호작용하기

**새 터미널 창**을 열고, 가상 환경을 활성화한 후, `a2a-samples/samples/python/agents/langgraph/app`으로 이동합니다.

테스트 클라이언트를 실행합니다:

```bash
python test_client.py
```

이제 `__main__.py`가 실행 중인 터미널 창에서 Ctrl+C를 입력하여 서버를 종료할 수 있습니다.

## 시연된 주요 기능

`langgraph` 예제는 몇 가지 중요한 A2A 개념을 보여줍니다:

1.  **LLM 통합**:

    - `agent.py`는 `CurrencyAgent`를 정의합니다. 이 에이전트는 사용자 쿼리를 처리하기 위해 `ChatGoogleGenerativeAI`와 LangGraph의 `create_react_agent`를 사용합니다.
    - 이는 실제 LLM이 에이전트의 로직을 어떻게 구동할 수 있는지 보여줍니다.

2.  **작업 상태 관리**:

    - `samples/langgraph/__main__.py`는 `InMemoryTaskStore`를 사용하여 `DefaultRequestHandler`를 초기화합니다.

        ```python { .no-copy }
        --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/langgraph/app/__main__.py:DefaultRequestHandler"
        ```

    - `CurrencyAgentExecutor` (`samples/langgraph/agent_executor.py`에 있음)의 `execute` 메서드가 `DefaultRequestHandler`에 의해 호출될 때, 현재 작업(있는 경우)을 포함하는 `RequestContext`와 상호작용합니다.
    - `message/send`의 경우, `DefaultRequestHandler`는 `TaskStore`를 사용하여 상호작용 전반에 걸쳐 작업 상태를 유지하고 검색합니다. 에이전트의 실행 흐름에 여러 단계가 포함되거나 영구적인 작업으로 귀결되는 경우, `message/send`에 대한 응답은 전체 `Task` 객체가 됩니다.
    - `test_client.py`의 `run_single_turn_test`는 `Task` 객체를 다시 받고 `get_task`를 사용하여 쿼리하는 것을 보여줍니다.

3.  **`TaskStatusUpdateEvent` 및 `TaskArtifactUpdateEvent`를 이용한 스트리밍**:

    - `CurrencyAgentExecutor`의 `execute` 메서드는 `DefaultRequestHandler`에 의해 조정되는 비스트리밍 및 스트리밍 요청을 모두 처리할 책임이 있습니다.
    - LangGraph 에이전트가 요청을 처리함에 따라 (`get_exchange_rate`와 같은 도구 호출을 포함할 수 있음), `CurrencyAgentExecutor`는 다양한 유형의 이벤트를 `EventQueue`에 추가합니다:
        - `TaskStatusUpdateEvent`: 중간 업데이트용 (예: "환율 조회 중...", "환율 처리 중..."). 이러한 이벤트의 `final` 플래그는 `False`입니다.
        - `TaskArtifactUpdateEvent`: 최종 답변이 준비되면 아티팩트로 큐에 추가됩니다. `lastChunk` 플래그는 `True`입니다.
        - 스트리밍 작업의 종료를 알리기 위해 `state=TaskState.completed` 및 `final=True`인 최종 `TaskStatusUpdateEvent`가 전송됩니다.
    - `test_client.py`의 `run_streaming_test` 함수는 서버로부터 수신되는 이러한 개별 이벤트 청크를 출력합니다.

4.  **다중 회차 대화 (`TaskState.input_required`)**:

    - `CurrencyAgent`는 쿼리가 모호한 경우(예: 사용자가 "100 USD는 얼마인가요?"라고 묻는 경우) 설명을 요청할 수 있습니다.
    - 이 경우, `CurrencyAgentExecutor`는 `status.state`가 `TaskState.input_required`이고 `status.message`에 에이전트의 질문(예: "어떤 통화로 변환하시겠습니까?")이 포함된 `TaskStatusUpdateEvent`를 큐에 추가합니다. 이 이벤트는 현재 상호작용 스트림에 대해 `final=True`를 갖습니다.
    - `test_client.py`의 `run_multi_turn_test` 함수는 다음을 보여줍니다:
        - 초기 모호한 쿼리를 보냅니다.
        - 에이전트는 (큐에 추가된 이벤트를 처리하는 `DefaultRequestHandler`를 통해) 상태가 `input_required`인 `Task`로 응답합니다.
        - 그런 다음 클라이언트는 첫 번째 회차의 `Task` 응답에서 `taskId`와 `contextId`를 포함하여 두 번째 메시지를 보내 누락된 정보("GBP로")를 제공합니다. 이는 동일한 작업을 계속합니다.

## 코드 살펴보기

다음 파일들을 잠시 살펴보십시오:

-   `__main__.py`: `A2AStarletteApplication` 및 `DefaultRequestHandler`를 사용한 서버 설정. `AgentCard` 정의에 `capabilities.streaming=True`가 포함되어 있음을 주목하십시오.
-   `agent.py`: LangGraph, LLM 모델 및 도구 정의가 포함된 `CurrencyAgent`.
-   `agent_executor.py`: `execute` (및 `cancel`) 메서드를 구현하는 `CurrencyAgentExecutor`. 진행 중인 작업을 이해하기 위해 `RequestContext`를 사용하고 다양한 이벤트(`TaskStatusUpdateEvent`, `TaskArtifactUpdateEvent`, 작업이 없는 경우 첫 번째 이벤트를 통해 암시적으로 새 `Task` 객체)를 다시 보내기 위해 `EventQueue`를 사용합니다.
-   `test_client.py`: 작업 ID 검색 및 다중 회차 대화에 사용하는 것을 포함하여 다양한 상호작용 패턴을 보여줍니다.

이 예제는 A2A가 에이전트 간의 복잡하고, 상태 저장이며, 비동기적인 상호작용을 어떻게 촉진하는지 훨씬 더 풍부하게 보여줍니다.
