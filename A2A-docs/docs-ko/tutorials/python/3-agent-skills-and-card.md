# 3. 에이전트 기술 및 에이전트 카드

A2A 에이전트가 어떤 작업을 수행하기 전에, 자신이 무엇을 할 수 있는지(기술)와 다른 에이전트나 클라이언트가 이러한 기능에 대해 어떻게 알 수 있는지(에이전트 카드)를 정의해야 합니다.

[`a2a-samples/samples/python/agents/helloworld/`](https://github.com/google-a2a/a2a-samples/tree/main/samples/python/agents/helloworld)에 있는 `helloworld` 예제를 사용하겠습니다.

## 에이전트 기술

**에이전트 기술(Agent Skill)**은 에이전트가 수행할 수 있는 특정 기능이나 함수를 설명합니다. 이는 클라이언트에게 에이전트가 어떤 종류의 작업에 적합한지 알려주는 구성 요소입니다.

`AgentSkill`의 주요 속성 (`a2a.types`에 정의됨):

- `id`: 기술에 대한 고유 식별자입니다.
- `name`: 사람이 읽을 수 있는 이름입니다.
- `description`: 기술이 수행하는 작업에 대한 더 자세한 설명입니다.
- `tags`: 분류 및 검색을 위한 키워드입니다.
- `examples`: 샘플 프롬프트 또는 사용 사례입니다.
- `inputModes` / `outputModes`: 입력 및 출력에 지원되는 미디어 유형입니다 (예: "text/plain", "application/json").

`__main__.py`에서 Helloworld 에이전트에 대한 기술이 어떻게 정의되는지 확인할 수 있습니다:

```python { .no-copy }
--8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/__main__.py:AgentSkill"
```

이 기술은 매우 간단합니다: "Returns hello world"라는 이름이며 주로 텍스트를 다룹니다.

## 에이전트 카드

**에이전트 카드(Agent Card)**는 A2A 서버가 일반적으로 `.well-known/agent.json` 엔드포인트에서 제공하는 JSON 문서입니다. 이는 에이전트의 디지털 명함과 같습니다.

`AgentCard`의 주요 속성 (`a2a.types`에 정의됨):

- `name`, `description`, `version`: 기본 ID 정보입니다.
- `url`: A2A 서비스에 도달할 수 있는 엔드포인트입니다.
- `capabilities`: `streaming` 또는 `pushNotifications`와 같이 지원되는 A2A 기능을 지정합니다.
- `defaultInputModes` / `defaultOutputModes`: 에이전트의 기본 미디어 유형입니다.
- `skills`: 에이전트가 제공하는 `AgentSkill` 객체 목록입니다.

`helloworld` 예제는 다음과 같이 에이전트 카드를 정의합니다:

```python { .no-copy }
--8<-- "https://raw.githubusercontent.com/google-a2a/a2a-samples/refs/heads/main/samples/python/agents/helloworld/__main__.py:AgentCard"
```

이 카드는 에이전트 이름이 "Hello World Agent"이고, `http://localhost:9999/`에서 실행되며, 텍스트 상호 작용을 지원하고, `hello_world` 기술을 가지고 있음을 알려줍니다. 또한 특정 자격 증명이 필요하지 않음을 의미하는 공개 인증을 나타냅니다.

에이전트 카드를 이해하는 것은 클라이언트가 에이전트를 발견하고 상호 작용하는 방법을 배우는 방법이므로 매우 중요합니다.
