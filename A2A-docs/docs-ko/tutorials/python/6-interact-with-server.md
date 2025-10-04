# 6. 서버와 상호 작용하기

Helloworld A2A 서버가 실행 중이므로, 이제 몇 가지 요청을 보내보겠습니다. SDK에는 이러한 상호 작용을 단순화하는 클라이언트(`A2AClient`)가 포함되어 있습니다.

## Helloworld 테스트 클라이언트

`test_client.py` 스크립트는 다음 방법을 보여줍니다:

1.  서버에서 에이전트 카드를 가져옵니다.
2.  `A2AClient` 인스턴스를 생성합니다.
3.  비스트리밍(`message/send`) 및 스트리밍(`message/stream`) 요청을 모두 보냅니다.

**새 터미널 창**을 열고, 가상 환경을 활성화한 후, `a2a-samples` 디렉토리로 이동합니다.

가상 환경 활성화 (가상 환경을 생성한 동일한 디렉토리에서 이 작업을 수행해야 합니다):

=== "Mac/Linux"

    ```sh
    source .venv/bin/activate
    ```

=== "Windows"

    ```powershell
    .venv\Scripts\activate
    ```

테스트 클라이언트를 실행합니다:

```bash
# a2a-samples 디렉토리에서
python samples/python/agents/helloworld/test_client.py
```

## 클라이언트 코드 이해하기

`test_client.py`의 주요 부분을 살펴보겠습니다:

1.  **에이전트 카드 가져오기 및 클라이언트 초기화**:

    ```python { .no-copy }
    --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/test_client.py:A2ACardResolver"
    ```

    `A2ACardResolver` 클래스는 편의를 위한 것입니다. 먼저 (제공된 기본 URL을 기반으로) 서버의 `/.well-known/agent.json` 엔드포인트에서 `AgentCard`를 가져온 다음, 이를 사용하여 클라이언트를 초기화합니다.

2.  **비스트리밍 메시지 보내기 (`send_message`)**:

    ```python { .no-copy }
    --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/test_client.py:send_message"
    ```

    - `send_message_payload`는 `MessageSendParams`를 위한 데이터를 구성합니다.
    - 이것은 `SendMessageRequest`로 래핑됩니다.
    - `role`이 "user"로 설정되고 `parts`에 내용이 포함된 `message` 객체를 포함합니다.
    - Helloworld 에이전트의 `execute` 메서드는 단일 "Hello World" 메시지를 큐에 넣습니다. `DefaultRequestHandler`는 이를 검색하여 응답으로 보냅니다.
    - `response`는 `SendMessageResponse` 객체가 되며, 여기에는 `SendMessageSuccessResponse`(에이전트의 `Message`가 결과로 포함됨) 또는 `JSONRPCErrorResponse`가 포함됩니다.

3.  **작업 ID 처리 (Helloworld를 위한 설명 참고)**:

    Helloworld 클라이언트 (`test_client.py`)는 `get_task` 또는 `cancel_task`를 직접 시도하지 않습니다. 왜냐하면 단순한 Helloworld 에이전트의 `execute` 메서드가 `message/send`를 통해 호출될 때, `DefaultRequestHandler`가 `Task` 객체 대신 직접적인 `Message` 응답을 반환하기 때문입니다. (LangGraph 예제와 같이) 명시적으로 작업을 관리하는 더 복잡한 에이전트는 `message/send`로부터 `Task` 객체를 반환하며, 이 객체의 `id`는 `get_task` 또는 `cancel_task`에 사용될 수 있습니다.

4.  **스트리밍 메시지 보내기 (`send_message_streaming`)**:

    ```python { .no-copy }
    --8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/test_client.py:send_message_streaming"
    ```

    - 이 메서드는 에이전트의 `message/stream` 엔드포인트를 호출합니다. `DefaultRequestHandler`는 `HelloWorldAgentExecutor.execute` 메서드를 호출합니다.
    - `execute` 메서드는 "Hello World" 메시지 하나를 큐에 넣고, 그 후 이벤트 큐가 닫힙니다.
    - 클라이언트는 이 단일 메시지를 하나의 `SendStreamingMessageResponse` 이벤트로 수신한 다음 스트림이 종료됩니다.
    - `stream_response`는 `AsyncGenerator`입니다.

## 예상 출력

`test_client.py`를 실행하면 다음에 대한 JSON 출력을 볼 수 있습니다:

-   비스트리밍 응답 (단일 "Hello World" 메시지).
-   스트리밍 응답 (하나의 청크로 된 단일 "Hello World" 메시지, 그 후 스트림 종료).

출력의 `id` 필드는 실행할 때마다 달라집니다.

```console { .no-copy }
// 비스트리밍 응답
{"jsonrpc":"2.0","id":"xxxxxxxx","result":{"type":"message","role":"agent","parts":[{"type":"text","text":"Hello World"}],"messageId":"yyyyyyyy"}}
// 스트리밍 응답 (하나의 청크)
{"jsonrpc":"2.0","id":"zzzzzzzz","result":{"type":"message","role":"agent","parts":[{"type":"text","text":"Hello World"}],"messageId":"wwwwwwww","final":true}}
```

_(실제 ID `xxxxxxxx`, `yyyyyyyy`, `zzzzzzzz`, `wwwwwwww` 등은 다른 UUID/요청 ID가 됩니다)_

이는 여러분의 서버가 업데이트된 SDK 구조로 기본적인 A2A 상호 작용을 올바르게 처리하고 있음을 확인시켜 줍니다!

이제 `__main__.py`가 실행 중인 터미널 창에서 Ctrl+C를 입력하여 서버를 종료할 수 있습니다.
