# 5. 서버 시작하기

이제 에이전트 카드와 에이전트 실행기가 준비되었으니, A2A 서버를 설정하고 시작할 수 있습니다.

A2A Python SDK는 A2A 호환 HTTP 서버 실행을 단순화하는 `A2AStarletteApplication` 클래스를 제공합니다. 이 클래스는 웹 프레임워크로 [Starlette](https://www.starlette.io/)을 사용하며, 일반적으로 [Uvicorn](https://www.uvicorn.org/)과 같은 ASGI 서버와 함께 실행됩니다.

## Helloworld에서의 서버 설정

서버가 어떻게 초기화되고 시작되는지 `__main__.py`를 다시 살펴보겠습니다.

```python { .no-copy }
--8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/__main__.py"
```

자세히 살펴보겠습니다:

1.  **`DefaultRequestHandler`**:

    - SDK는 `DefaultRequestHandler`를 제공합니다. 이 핸들러는 여러분의 `AgentExecutor` 구현체(여기서는 `HelloWorldAgentExecutor`)와 `TaskStore`(여기서는 `InMemoryTaskStore`)를 인자로 받습니다.
    - 들어오는 A2A RPC 호출을 실행기의 적절한 메서드(예: `execute` 또는 `cancel`)로 라우팅합니다.
    - `TaskStore`는 `DefaultRequestHandler`가 작업의 라이프사이클을 관리하는 데 사용되며, 특히 상태 저장 상호 작용, 스트리밍 및 재구독에 사용됩니다. 에이전트 실행기가 간단하더라도 핸들러에는 작업 저장소가 필요합니다.

2.  **`A2AStarletteApplication`**:

    - `A2AStarletteApplication` 클래스는 `agent_card`와 `request_handler`(생성자에서는 `http_handler`로 참조됨)로 인스턴스화됩니다.
    - 서버가 (기본적으로) `/.well-known/agent.json` 엔드포인트에서 `agent_card`를 노출하므로 이는 매우 중요합니다.
    - `request_handler`는 `AgentExecutor`와 상호 작용하여 들어오는 모든 A2A 메서드 호출을 처리할 책임이 있습니다.

3.  **`uvicorn.run(server_app_builder.build(), ...)`**:
    - `A2AStarletteApplication`에는 실제 Starlette 애플리케이션을 구성하는 `build()` 메서드가 있습니다.
    - 이 애플리케이션은 `uvicorn.run()`을 사용하여 실행되어, 여러분의 에이전트를 HTTP를 통해 접근할 수 있게 만듭니다.
    - `host='0.0.0.0'`은 사용자의 컴퓨터 모든 네트워크 인터페이스에서 서버에 접근할 수 있도록 합니다.
    - `port=9999`는 수신 대기할 포트를 지정합니다. 이는 `AgentCard`의 `url`과 일치합니다.

## Helloworld 서버 실행하기

터미널에서 `a2a-samples` 디렉토리로 이동한 후 (아직 해당 위치가 아니라면) 가상 환경이 활성화되어 있는지 확인하십시오.

Helloworld 서버를 실행하려면:

```bash
# a2a-samples 디렉토리에서
python samples/python/agents/helloworld/__main__.py
```

서버가 실행 중임을 나타내는 다음과 유사한 출력을 볼 수 있어야 합니다:

```console { .no-copy }
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9999 (Press CTRL+C to quit)
```

이제 여러분의 A2A Helloworld 에이전트가 활성화되어 요청을 기다리고 있습니다! 다음 단계에서는 이 에이전트와 상호 작용해 보겠습니다.
