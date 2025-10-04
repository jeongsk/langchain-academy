---
hide:
  - navigation
---

# 에이전트간(A2A) 프로토콜 명세

**버전:** `{{ a2a_version }}`

## 10. 부록

### 10.1. MCP(모델 컨텍스트 프로토콜)와의 관계

A2A와 MCP는 에이전트 시스템의 다양한 측면을 위해 설계된 보완적인 프로토콜입니다.

- **[모델 컨텍스트 프로토콜(MCP)](https://modelcontextprotocol.io/):** AI 모델과 에이전트가 **도구, API, 데이터 소스 및 기타 외부 리소스**에 연결하고 상호 작용하는 방법을 표준화하는 데 중점을 둡니다. 도구 기능(LLM의 함수 호출과 같은)을 설명하고, 입력을 전달하고, 구조화된 출력을 수신하는 구조화된 방법을 정의합니다. MCP를 에이전트가 특정 기능을 _사용_하거나 리소스에 액세스하는 방법에 대한 "방법"으로 생각하십시오.
- **에이전트간 프로토콜(A2A):** 독립적이고 종종 불투명한 **AI 에이전트가 동료로서 서로 통신하고 협업하는 방법**을 표준화하는 데 중점을 둡니다. A2A는 에이전트가 서로를 발견하고, 상호 작용 양식을 협상하고, 공유 작업을 관리하고, 대화 컨텍스트 또는 복잡한 결과를 교환하기 위한 애플리케이션 수준 프로토콜을 제공합니다. 에이전트가 작업을 _파트너_하거나 _위임_하는 방법에 관한 것입니다.

**함께 작동하는 방식:**
A2A 클라이언트 에이전트는 A2A 서버 에이전트에게 복잡한 작업을 수행하도록 요청할 수 있습니다. 그러면 서버 에이전트는 MCP를 사용하여 여러 기본 도구, API 또는 데이터 소스와 상호 작용하여 A2A 작업을 수행하는 데 필요한 정보를 수집하거나 작업을 수행할 수 있습니다.

자세한 비교는 [A2A 및 MCP 가이드](./topics/a2a-and-mcp.md)를 참조하십시오.

### 10.2. 보안 고려 사항 요약

보안은 A2A에서 가장 중요한 관심사입니다. 주요 고려 사항은 다음과 같습니다.

- **전송 보안:** 프로덕션 환경에서는 항상 강력한 TLS 구성과 함께 HTTPS를 사용하십시오.
- **인증:**
    - 표준 HTTP 메커니즘(예: Bearer 토큰, API 키가 있는 `Authorization` 헤더)을 통해 처리됩니다.
    - 요구 사항은 `AgentCard`에 선언됩니다.
    - 자격 증명은 클라이언트가 대역 외에서 **반드시** 얻어야 합니다.
    - A2A 서버는 모든 요청을 **반드시** 인증해야 합니다.
- **권한 부여:**
    - 인증된 ID를 기반으로 한 서버 측 책임입니다.
    - 최소 권한 원칙을 구현합니다.
    - 기술, 작업 또는 데이터를 기반으로 세분화될 수 있습니다.
- **푸시 알림 보안:**
    - SSRF를 방지하려면 웹훅 URL 유효성 검사(알림을 보내는 A2A 서버에 의해)가 중요합니다.
    - 클라이언트의 웹훅에 대한 A2A 서버의 인증이 필수적입니다.
    - 클라이언트의 웹훅 수신기에 의한 알림 인증(합법적인 A2A 서버에서 왔으며 관련성이 있는지 확인)이 중요합니다.
    - 자세한 푸시 알림 보안은 [스트리밍 및 비동기 작업 가이드](./topics/streaming-and-async.md#security-considerations-for-push-notifications)를 참조하십시오.
- **입력 유효성 검사:** 서버는 주입 공격이나 처리 오류를 방지하기 위해 모든 RPC 매개변수와 `Message` 및 `Artifact` 부분의 데이터 내용/구조를 엄격하게 유효성 검사해야 합니다.
- **리소스 관리:** 에이전트를 남용이나 과부하로부터 보호하기 위해 속도 제한, 동시성 제어 및 리소스 제한을 구현합니다.
- **데이터 개인 정보 보호:** `Message` 및 `Artifact` 부분에서 교환되는 데이터에 대해 적용 가능한 모든 개인 정보 보호 규정을 준수합니다. 민감한 데이터 전송을 최소화합니다.

포괄적인 논의는 [엔터프라이즈 준비 기능 가이드](./topics/enterprise-ready.md)를 참조하십시오.

## 1. 소개

에이전트간(A2A) 프로토콜은 독립적이고 잠재적으로 불투명한 AI 에이전트 시스템 간의 통신과 상호 운용성을 촉진하기 위해 설계된 개방형 표준입니다. 에이전트가 서로 다른 프레임워크, 언어 또는 다른 공급업체에 의해 구축될 수 있는 생태계에서 A2A는 공통 언어와 상호 작용 모델을 제공합니다.

이 문서는 A2A 프로토콜에 대한 상세한 기술 명세를 제공합니다. 주요 목표는 에이전트가 다음을 수행할 수 있도록 하는 것입니다:

- 서로의 기능 발견하기.
- 상호 작용 방식(텍스트, 파일, 구조화된 데이터) 협상하기.
- 협업 작업 관리하기.
- 서로의 내부 상태, 메모리 또는 도구에 접근할 필요 없이 **사용자 목표를 달성하기 위해 안전하게 정보를 교환하기.**

### 1.1. A2A의 핵심 목표

- **상호 운용성:** 서로 다른 에이전트 시스템 간의 통신 격차 해소.
- **협업:** 에이전트가 작업을 위임하고, 컨텍스트를 교환하며, 복잡한 사용자 요청에 대해 협력할 수 있도록 지원.
- **발견:** 에이전트가 다른 에이전트의 기능을 동적으로 찾고 이해할 수 있도록 허용.
- **유연성:** 동기식 요청/응답, 실시간 업데이트를 위한 스트리밍, 장기 실행 작업을 위한 비동기 푸시 알림 등 다양한 상호 작용 모드 지원.
- **보안:** 표준 웹 보안 관행에 의존하여 엔터프라이즈 환경에 적합한 보안 통신 패턴 촉진.
- **비동기성:** 장기 실행 작업 및 인간 참여 시나리오를 포함할 수 있는 상호 작용을 기본적으로 지원.

### 1.2. 기본 원칙

- **단순성:** 기존의 잘 알려진 표준(HTTP, JSON-RPC 2.0, 서버 전송 이벤트) 재사용.
- **엔터프라이즈 준비성:** 기존 엔터프라이즈 관행에 맞춰 인증, 권한 부여, 보안, 개인 정보 보호, 추적 및 모니터링 해결.
- **비동기 우선:** (잠재적으로 매우) 긴 실행 작업 및 인간 참여 상호 작용을 위해 설계.
- **양식 불가지성:** 텍스트, 오디오/비디오(파일 참조를 통해), 구조화된 데이터/양식, 그리고 잠재적으로 포함된 UI 구성 요소(예: 부분에서 참조된 iframe)를 포함한 다양한 콘텐츠 유형 교환 지원.
- **불투명한 실행:** 에이전트는 내부 생각, 계획 또는 도구 구현을 공유할 필요 없이 선언된 기능과 교환된 정보를 기반으로 협력.

A2A의 목적과 이점에 대한 더 넓은 이해를 원하시면 [A2A란 무엇인가?](./topics/what-is-a2a.md)를 참조하십시오.

## 2. 핵심 개념 요약

A2A는 몇 가지 핵심 개념을 중심으로 전개됩니다. 자세한 설명은 [핵심 개념 가이드](./topics/key-concepts.md)를 참조하십시오.

- **A2A 클라이언트:** 사용자 또는 다른 시스템을 대신하여 A2A 서버에 요청을 시작하는 애플리케이션 또는 에이전트.
- **A2A 서버(원격 에이전트):** A2A 호환 HTTP 엔드포인트를 노출하고 작업을 처리하며 응답을 제공하는 에이전트 또는 에이전트 시스템.
- **에이전트 카드:** A2A 서버에서 게시하는 JSON 메타데이터 문서로, ID, 기능, 기술, 서비스 엔드포인트 및 인증 요구 사항을 설명합니다.
- **메시지:** 클라이언트와 원격 에이전트 간의 통신 차례로, `role`("user" 또는 "agent")을 가지며 하나 이상의 `Part`를 포함합니다.
- **작업:** A2A에서 관리하는 기본 작업 단위로, 고유 ID로 식별됩니다. 작업은 상태를 가지며 정의된 수명 주기를 통해 진행됩니다.
- **부분:** 메시지 또는 아티팩트 내의 가장 작은 콘텐츠 단위입니다(예: `TextPart`, `FilePart`, `DataPart`).
- **아티팩트:** 작업 결과로 에이전트가 생성한 출력물(예: 문서, 이미지, 구조화된 데이터)로, `Part`로 구성됩니다.
- **스트리밍(SSE):** 서버 전송 이벤트를 통해 전달되는 작업(상태 변경, 아티팩트 청크)에 대한 실시간 증분 업데이트.
- **푸시 알림:** 장기 실행 또는 연결이 끊긴 시나리오를 위해 클라이언트가 제공한 웹훅 URL에 서버가 시작한 HTTP POST 요청을 통해 전달되는 비동기 작업 업데이트.
- **컨텍스트:** 관련 작업을 논리적으로 그룹화하기 위한 선택적 서버 생성 식별자.
- **확장:** 에이전트가 핵심 A2A 사양을 넘어 추가 기능이나 데이터를 제공하기 위한 메커니즘.

## 3. 전송 및 형식

### 3.1. 전송 프로토콜

- A2A 통신은 **반드시** **HTTP(S)**를 통해 이루어져야 합니다.
- A2A 서버는 `AgentCard`에 정의된 URL에서 서비스를 노출합니다.

### 3.2. 데이터 형식

A2A는 모든 요청 및 응답(SSE 스트림 래퍼 제외)의 페이로드 형식으로 **[JSON-RPC 2.0](https://www.jsonrpc.org/specification)**을 사용합니다.

- 클라이언트 요청 및 서버 응답은 **반드시** JSON-RPC 2.0 사양을 준수해야 합니다.
- JSON-RPC 페이로드를 포함하는 HTTP 요청 및 응답의 `Content-Type` 헤더는 **반드시** `application/json`이어야 합니다.

### 3.3. 스트리밍 전송(서버 전송 이벤트)

`message/stream` 또는 `tasks/resubscribe`와 같은 메서드에 스트리밍이 사용되는 경우:

- 서버는 HTTP `200 OK` 상태와 `text/event-stream`의 `Content-Type` 헤더로 응답합니다.
- 이 HTTP 응답의 본문에는 W3C에서 정의한 **[서버 전송 이벤트(SSE)](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events)** 스트림이 포함됩니다.
- 각 SSE `data` 필드에는 완전한 JSON-RPC 2.0 응답 객체(특히, [`SendStreamingMessageResponse`](#721-sendstreamingmessageresponse-object))가 포함됩니다.

## 4. 인증 및 권한 부여

A2A는 에이전트를 표준 엔터프라이즈 애플리케이션으로 취급하며, 기존 웹 보안 관행에 의존합니다. ID 정보는 A2A JSON-RPC 페이로드 내에서 전송되지 **않으며**, HTTP 전송 계층에서 처리됩니다.

엔터프라이즈 보안 측면에 대한 포괄적인 가이드는 [엔터프라이즈 준비 기능](./topics/enterprise-ready.md)을 참조하십시오.

### 4.1. 전송 보안

3.1절에 명시된 바와 같이, 프로덕션 배포는 **반드시** HTTPS를 사용해야 합니다. 구현은 강력한 암호화 스위트와 함께 최신 [TLS](https://datatracker.ietf.org/doc/html/rfc8446) 구성(TLS 1.2+ 권장)을 **사용해야 합니다**.

### 4.2. 서버 ID 확인

A2A 클라이언트는 TLS 핸드셰이크 중에 신뢰할 수 있는 인증 기관(CA)에 대해 TLS 인증서를 검증하여 A2A 서버의 ID를 **확인해야 합니다**.

### 4.3. 클라이언트/사용자 ID 및 인증 프로세스

1. **요구 사항 발견:** 클라이언트는 [`AgentCard`](#55-agentcard-object-structure)의 `authentication` 필드를 통해 서버의 필수 인증 체계를 발견합니다. 체계 이름은 종종 [OpenAPI 인증 방법](https://swagger.io/docs/specification/authentication/)과 일치합니다(예: OAuth 2.0 토큰의 경우 "Bearer", 기본 인증의 경우 "Basic", API 키의 경우 "ApiKey").
2. **자격 증명 획득(대역 외):** 클라이언트는 필수 인증 체계 및 ID 공급자에 특정한 **대역 외 프로세스**를 통해 필요한 자격 증명(예: API 키, OAuth 토큰, JWT)을 얻습니다. 이 프로세스는 A2A 프로토콜 자체의 범위를 벗어납니다.
3. **자격 증명 전송:** 클라이언트는 서버로 전송되는 모든 A2A 요청의 적절한 [HTTP 헤더](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)(예: `Authorization: Bearer <token>`, `X-API-Key: <value>`)에 이러한 자격 증명을 포함합니다.

### 4.4. 인증에 대한 서버 책임

A2A 서버:

- **반드시** 제공된 HTTP 자격 증명과 에이전트 카드에서 선언된 인증 요구 사항을 기반으로 모든 들어오는 요청을 인증해야 합니다.
- 인증 문제 또는 거부에 대해 [`401 Unauthorized`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401) 또는 [`403 Forbidden`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403)과 같은 표준 HTTP 상태 코드를 **사용해야 합니다**.
- 클라이언트를 안내하기 위해 필요한 인증 체계를 나타내기 위해 `401 Unauthorized` 응답과 함께 관련 HTTP 헤더(예: [`WWW-Authenticate`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate))를 **포함해야 합니다**.

### 4.5. 작업 내 인증(보조 자격 증명)

에이전트가 작업 실행 중에 _다른_ 시스템 또는 리소스에 대한 _추가_ 자격 증명이 필요한 경우(예: 자체 인증이 필요한 특정 도구에 사용자 대신 액세스하기 위해):

1. A2A 작업을 `auth-required` 상태로 **전환해야 합니다**([`TaskState`](#63-taskstate-enum) 참조).
2. 함께 제공되는 `TaskStatus.message`(종종 [`DataPart`](#653-datapart-object))는 필요한 보조 인증에 대한 세부 정보를 **제공해야 하며**, 필요성을 설명하기 위해 잠재적으로 [`PushNotificationAuthenticationInfo`](#69-pushnotificationauthenticationinfo-object)와 유사한 구조를 사용합니다.
3. 그런 다음 A2A 클라이언트는 이러한 새 자격 증명을 대역 외로 얻어 후속 [`message/send`](#71-messagesend) 또는 [`message/stream`](#72-messagestream) 요청에서 제공합니다. 이러한 자격 증명이 사용되는 방식(예: 에이전트가 프록시하는 경우 A2A 메시지 내에서 데이터로 전달되거나 클라이언트가 보조 시스템과 직접 상호 작용하는 데 사용됨)은 특정 시나리오에 따라 다릅니다.

### 4.6. 권한 부여

클라이언트가 인증되면 A2A 서버는 인증된 클라이언트/사용자 ID와 자체 정책을 기반으로 요청을 승인할 책임이 있습니다. 권한 부여 논리는 구현에 따라 다르며 다음에 따라 적용될 **수 있습니다**.

- 요청된 특정 기술(예: 에이전트 카드의 `AgentSkill.id`로 식별됨).
- 작업 내에서 시도된 작업.
- 에이전트가 관리하는 리소스와 관련된 데이터 액세스 정책.
- 해당하는 경우 제시된 토큰과 관련된 OAuth 범위.

서버는 최소 권한 원칙을 구현해야 합니다.

## 5. 에이전트 발견: 에이전트 카드

### 5.1. 목적

A2A 서버는 **반드시** 에이전트 카드를 사용할 수 있도록 해야 합니다. 에이전트 카드는 서버의 ID, 기능, 기술, 서비스 엔드포인트 URL 및 클라이언트가 인증하고 상호 작용하는 방법을 설명하는 JSON 문서입니다. 클라이언트는 이 정보를 사용하여 적합한 에이전트를 찾고 상호 작용을 구성합니다.

발견 전략에 대한 자세한 내용은 [에이전트 발견 가이드](./topics/agent-discovery.md)를 참조하십시오.

### 5.2. 발견 메커니즘

클라이언트는 다음을 포함하되 이에 국한되지 않는 다양한 방법을 통해 에이전트 카드를 찾을 수 있습니다.

- **잘 알려진 URI:** 에이전트 도메인의 미리 정의된 경로에 액세스합니다([섹션 5.3](#53-recommended-location) 참조).
- **레지스트리/카탈로그:** 큐레이션된 에이전트 카탈로그 또는 레지스트리(엔터프라이즈별, 공개 또는 도메인별일 수 있음)를 쿼리합니다.
- **직접 구성:** 클라이언트는 에이전트 카드 URL 또는 카드 콘텐츠 자체로 미리 구성될 수 있습니다.

### 5.3. 권장 위치

잘 알려진 URI 전략을 사용하는 경우 에이전트의 에이전트 카드에 권장되는 위치는 다음과 같습니다.
`https://{server_domain}/.well-known/agent.json`
이는 잘 알려진 URI에 대한 [RFC 8615](https://datatracker.ietf.org/doc/html/rfc8615)의 원칙을 따릅니다.

### 5.4. 에이전트 카드 보안

에이전트 카드 자체에 민감한 것으로 간주되는 정보가 포함될 수 있습니다.

- 에이전트 카드에 민감한 정보가 포함된 경우 카드를 제공하는 엔드포인트는 **반드시** 적절한 액세스 제어(예: mTLS, 네트워크 제한, 카드 가져오기에 필요한 인증)로 보호되어야 합니다.
- 일반적으로 에이전트 카드에 일반 텍스트 비밀(예: 정적 API 키)을 직접 포함하는 것은 **권장되지 않습니다**. 클라이언트가 대역 외에서 동적 자격 증명을 얻는 인증 체계를 선호합니다.

### 5.5. `AgentCard` 객체 구조

```ts { .no-copy }
--8<-- "types/src/types.ts:AgentCard"
```

| 필드 이름                         | 유형                                                               | 필수     | 설명                                                                                                                                        |
| :---------------------------------- | :----------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`                              | `string`                                                           | 예       | 에이전트의 사람이 읽을 수 있는 이름입니다.                                                                                                  |
| `description`                       | `string`                                                           | 예       | 사람이 읽을 수 있는 설명입니다. [CommonMark](https://commonmark.org/)를 사용할 수 있습니다.                                                     |
| `url`                               | `string`                                                           | 예       | 에이전트의 A2A 서비스에 대한 기본 URL입니다. 절대적이어야 합니다. 프로덕션용 HTTPS.                                                              |
| `provider`                          | [`AgentProvider`](#551-agentprovider-object)                       | 아니요   | 에이전트 공급자에 대한 정보입니다.                                                                                                            |
| `iconUrl`                           | `string`                                                           | 아니요   | 에이전트 아이콘의 URL입니다.                                                                                                                |
| `version`                           | `string`                                                           | 예       | 에이전트 또는 A2A 구현 버전 문자열입니다.                                                                                                   |
| `documentationUrl`                  | `string`                                                           | 아니요   | 에이전트에 대한 사람이 읽을 수 있는 설명서의 URL입니다.                                                                                     |
| `capabilities`                      | [`AgentCapabilities`](#552-agentcapabilities-object)               | 예       | 지원되는 선택적 A2A 프로토콜 기능(예: 스트리밍, 푸시 알림)을 지정합니다.                                                                    |
| `securitySchemes`                   | { [scheme: string]: [SecurityScheme](#553-securityscheme-object) } | 아니요   | 이 에이전트로 인증하는 데 사용되는 보안 체계 세부 정보입니다. undefined는 A2A 광고 인증이 없음을 의미합니다(프로덕션에는 권장되지 않음).        |
| `security`                          | `{ [scheme: string]: string[]; }[]`                                | 아니요   | 에이전트 연락을 위한 보안 요구 사항입니다.                                                                                                  |
| `defaultInputModes`                 | `string[]`                                                         | 예       | 에이전트에서 허용하는 입력 미디어 유형입니다.                                                                                               |
| `defaultOutputModes`                | `string[]`                                                         | 예       | 에이전트에서 생성하는 출력 미디어 유형입니다.                                                                                               |
| `skills`                            | [`AgentSkill[]`](#554-agentskill-object)                           | 예       | 기술 배열입니다. 에이전트가 작업을 수행하는 경우 하나 이상 있어야 합니다.                                                                    |
| `supportsAuthenticatedExtendedCard` | `boolean`                                                          | 아니요   | 인증된 엔드포인트를 통해 더 자세한 에이전트 카드를 검색하는 지원 여부를 나타냅니다.                                                          |

#### 5.5.1. `AgentProvider` Object

Information about the organization or entity providing the agent.

```ts { .no-copy }
--8<-- "types/src/types.ts:AgentProvider"
```

| Field Name     | Type     | Required | Description                             |
| :------------- | :------- | :------- | :-------------------------------------- |
| `organization` | `string` | Yes      | Name of the organization/entity.        |
| `url`          | `string` | Yes      | URL for the provider's website/contact. |

#### 5.5.2. `AgentCapabilities` Object

Specifies optional A2A protocol features supported by the agent.

```ts { .no-copy }
--8<-- "types/src/types.ts:AgentCapabilities"
```

| Field Name               | Type             | Required | Default | Description                                                                          |
| :----------------------- | :--------------- | :------- | :------ | :----------------------------------------------------------------------------------- |
| `streaming`              | `boolean`        | No       | `false` | Indicates support for SSE streaming methods (`message/stream`, `tasks/resubscribe`). |
| `pushNotifications`      | `boolean`        | No       | `false` | Indicates support for push notification methods (`tasks/pushNotificationConfig/*`).  |
| `stateTransitionHistory` | `boolean`        | No       | `false` | Placeholder for future feature: exposing detailed task status change history.        |
| `extensions`             | [`AgentExtension`[]](#5521-agentextension-object) | No       | `[]`    | A list of extensions supported by this agent.                                        |

#### 5.5.2.1. `AgentExtension` Object

Specifies an extension to the A2A protocol supported by the agent.

```ts { .no-copy }
--8<-- "types/src/types.ts:AgentExtension"
```

| Field Name    | Type      | Required | Description                                                                                 |
| :-------------| :-------- | :------- | :------------------------------------------------------------------------------------------ |
| `uri`         | `string`  | Yes      | The URI for the supported extension.                                                        |
| `required`    | `boolean` | No       | Whether the agent requires clients to follow some protocol logic specific to the extension. Clients should expect failures when attempting to interact with a server that requires an extension the client does not support. |
| `description` | `string`  | No       | A description of how the extension is used by the agent.                                    |
| `params`      | `object`  | No       | Configuration parameters specific to the extension                                          |

#### 5.5.3. `SecurityScheme` Object

Describes the authentication requirements for accessing the agent's `url` endpoint. Refer [Sample Agent Card](#56-sample-agent-card) for an example.

```ts { .no-copy }
--8<-- "types/src/types.ts:SecurityScheme"
```

#### 5.5.4. `AgentSkill` Object

Describes a specific capability, function, or area of expertise the agent can perform or address.

```ts { .no-copy }
--8<-- "types/src/types.ts:AgentSkill"
```

| Field Name    | Type       | Required | Description                                                                    |
| :------------ | :--------- | :------- | :----------------------------------------------------------------------------- |
| `id`          | `string`   | Yes      | Unique skill identifier within this agent.                                     |
| `name`        | `string`   | Yes      | Human-readable skill name.                                                     |
| `description` | `string`   | Yes      | Detailed skill description. [CommonMark](https://commonmark.org/) MAY be used. |
| `tags`        | `string[]` | Yes      | Keywords/categories for discoverability.                                       |
| `examples`    | `string[]` | No       | Example prompts or use cases demonstrating skill usage.                        |
| `inputModes`  | `string[]` | No       | Overrides `defaultInputModes` for this specific skill. Accepted Media Types.    |
| `outputModes` | `string[]` | No       | Overrides `defaultOutputModes` for this specific skill. Produced Media Types.   |

### 5.6. Sample Agent Card

```json
{
  "name": "GeoSpatial Route Planner Agent",
  "description": "Provides advanced route planning, traffic analysis, and custom map generation services. This agent can calculate optimal routes, estimate travel times considering real-time traffic, and create personalized maps with points of interest.",
  "url": "https://georoute-agent.example.com/a2a/v1",
  "provider": {
    "organization": "Example Geo Services Inc.",
    "url": "https://www.examplegeoservices.com"
  },
  "iconUrl": "https://georoute-agent.example.com/icon.png",
  "version": "1.2.0",
  "documentationUrl": "https://docs.examplegeoservices.com/georoute-agent/api",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": false
  },
  "securitySchemes": {
    "google": {
      "type": "openIdConnect",
      "openIdConnectUrl": "https://accounts.google.com/.well-known/openid-configuration"
    }
  },
  "security": [{ "google": ["openid", "profile", "email"] }],
  "defaultInputModes": ["application/json", "text/plain"],
  "defaultOutputModes": ["application/json", "image/png"],
  "skills": [
    {
      "id": "route-optimizer-traffic",
      "name": "Traffic-Aware Route Optimizer",
      "description": "Calculates the optimal driving route between two or more locations, taking into account real-time traffic conditions, road closures, and user preferences (e.g., avoid tolls, prefer highways).",
      "tags": ["maps", "routing", "navigation", "directions", "traffic"],
      "examples": [
        "Plan a route from '1600 Amphitheatre Parkway, Mountain View, CA' to 'San Francisco International Airport' avoiding tolls.",
        "{\"origin\": {\"lat\": 37.422, \"lng\": -122.084}, \"destination\": {\"lat\": 37.7749, \"lng\": -122.4194}, \"preferences\": [\"avoid_ferries\"]}"
      ],
      "inputModes": ["application/json", "text/plain"],
      "outputModes": [
        "application/json",
        "application/vnd.geo+json",
        "text/html"
      ]
    },
    {
      "id": "custom-map-generator",
      "name": "Personalized Map Generator",
      "description": "Creates custom map images or interactive map views based on user-defined points of interest, routes, and style preferences. Can overlay data layers.",
      "tags": ["maps", "customization", "visualization", "cartography"],
      "examples": [
        "Generate a map of my upcoming road trip with all planned stops highlighted.",
        "Show me a map visualizing all coffee shops within a 1-mile radius of my current location."
      ],
      "inputModes": ["application/json"],
      "outputModes": [
        "image/png",
        "image/jpeg",
        "application/json",
        "text/html"
      ]
    }
  ],
  "supportsAuthenticatedExtendedCard": true
}
```

## 6. 프로토콜 데이터 객체

이러한 객체는 A2A 프로토콜의 JSON-RPC 메서드 내에서 교환되는 데이터의 구조를 정의합니다.

### 6.1. `Task` 객체

A2A 클라이언트를 위해 A2A 서버에서 처리 중인 상태 저장 작업 단위를 나타냅니다. 작업은 특정 목표 또는 요청과 관련된 전체 상호 작용을 캡슐화합니다.

```ts { .no-copy }
--8<-- "types/src/types.ts:Task"
```

| 필드 이름 | 유형                                  | 필수     | 설명                                                                          |
|:------------|:--------------------------------------| :------- | :---------------------------------------------------------------------------- |
| `id`        | `string`                              | 예       | 서버에서 생성한 고유 작업 식별자(예: UUID)                                    |
| `contextId` | `string`                              | 예       | 상호 작용 전반에 걸친 컨텍스트 정렬을 위해 서버에서 생성한 ID                 |
| `status`    | [`TaskStatus`](#62-taskstatus-object) | 예       | 작업의 현재 상태(상태, 메시지, 타임스탬프).                                   |
| `artifacts` | [`Artifact[]`](#67-artifact-object)   | 아니요   | 이 작업에 대해 에이전트가 생성한 출력 배열.                                   |
| `history`   | [`Message[]`](#64-message-object)     | 아니요   | `historyLength`로 요청된 경우 교환된 최근 메시지의 선택적 배열.               |
| `metadata`  | `Record<string, any>`                 | 아니요   | 작업과 관련된 임의의 키-값 메타데이터.                                       |
| `kind`      | `"task"`                              | 예       | 유형 판별자, 리터럴 값                                                        |

### 6.2. `TaskStatus` Object

Represents the current state and associated context (e.g., a message from the agent) of a `Task`.

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskStatus"
```

| Field Name  | Type                              | Required | Description                                                |
| :---------- | :-------------------------------- | :------- | :--------------------------------------------------------- |
| `state`     | [`TaskState`](#63-taskstate-enum) | Yes      | Current lifecycle state of the task.                       |
| `message`   | [`Message`](#64-message-object)   | No       | Optional message providing context for the current status. |
| `timestamp` | `string` (ISO 8601)               | No       | Timestamp (UTC recommended) when this status was recorded. |

### 6.3. `TaskState` Enum

Defines the possible lifecycle states of a `Task`.

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskState"
```

| Value            | Description                                                                                               | Terminal?  |
| :--------------- | :-------------------------------------------------------------------------------------------------------- | :--------- |
| `submitted`      | Task received by the server and acknowledged, but processing has not yet actively started.                | No         |
| `working`        | Task is actively being processed by the agent. Client may expect further updates or a terminal state.     | No         |
| `input-required` | Agent requires additional input from the client/user to proceed. The task is effectively paused.          | No (Pause) |
| `completed`      | Task finished successfully. Results are typically available in `Task.artifacts` or `TaskStatus.message`.  | Yes        |
| `canceled`       | Task was canceled (e.g., by a `tasks/cancel` request or server-side policy).                              | Yes        |
| `failed`         | Task terminated due to an error during processing. `TaskStatus.message` may contain error details.        | Yes        |
| `rejected`       | Task terminated due to rejection by remote agent. `TaskStatus.message` may contain error details.         | Yes        |
| `auth-required`  | Agent requires additional authentication from the client/user to proceed. The task is effectively paused. | No (Pause) |
| `unknown`        | The state of the task cannot be determined (e.g., task ID is invalid, unknown, or has expired).           | Yes        |

### 6.4. `Message` Object

Represents a single communication turn or a piece of contextual information between a client and an agent. Messages are used for instructions, prompts, replies, and status updates.

```ts { .no-copy }
--8<-- "types/src/types.ts:Message"
```

| Field Name         | Type                            | Required | Description                                                                      |
| :----------------- | :------------------------------ | :------- | :------------------------------------------------------------------------------- |
| `role`             | `"user"` \| `"agent"`           | Yes      | Indicates the sender: `"user"` (from A2A Client) or `"agent"` (from A2A Server). |
| `parts`            | [`Part[]`](#65-part-union-type) | Yes      | Array of content parts. Must contain at least one part.                          |
| `metadata`         | `Record<string, any>`           | No       | Arbitrary key-value metadata associated with this message.                       |
| `extensions`       | `string[]`                      | No       | A list of extension URIs that contributed to this message.                       |
| `referenceTaskIds` | `string[]`                      | No       | List of tasks referenced as contextual hint by this message.                     |
| `messageId`        | `string`                        | Yes      | Message identifier generated by the message sender                               |
| `taskId`           | `string`                        | No       | Task identifier the current message is related to                                |
| `contextId`        | `string`                        | No       | Context identifier the message is associated with                                |
| `kind`             | `"message"`                     | Yes      | Type discriminator, literal value                                                |

### 6.5. `Part` Union Type

Represents a distinct piece of content within a `Message` or `Artifact`. A `Part` is a union type representing exportable content as either `TextPart`, `FilePart`, or `DataPart`. All `Part` types also include an optional `metadata` field (`Record<string, any>`) for part-specific metadata.

```ts { .no-copy }
--8<-- "types/src/types.ts:Part"
```

It **MUST** be one of the following:

#### 6.5.1. `TextPart` Object

For conveying plain textual content.

```ts { .no-copy }
--8<-- "types/src/types.ts:TextPart"
```

| Field Name | Type                  | Required | Description                                   |
| :--------- | :-------------------- | :------- | :-------------------------------------------- |
| `kind`     | `"text"` (literal)    | Yes      | Identifies this part as textual content.      |
| `text`     | `string`              | Yes      | The textual content of the part.              |
| `metadata` | `Record<string, any>` | No       | Optional metadata specific to this text part. |

#### 6.5.2. `FilePart` Object

For conveying file-based content.

```ts { .no-copy }
--8<-- "types/src/types.ts:FilePart"
```

| Field Name | Type                  | Required    | Description                                   |
| :--------- | :-------------------- | :---------- | :-------------------------------------------- |
| `kind`     | `"file"` (literal)    | Yes         | Identifies this part as file content.         |
| `file`     | `FileWithBytes` \| `FileWithUri` | Yes  | Contains the file details and data/reference. |
| `metadata` | `Record<string, any>` | No          | Optional metadata specific to this file part. |

#### 6.5.3. `DataPart` Object

For conveying structured JSON data. Useful for forms, parameters, or any machine-readable information.

```ts { .no-copy }
--8<-- "types/src/types.ts:DataPart"
```

| Field Name | Type                  | Required | Description                                                                 |
| :--------- | :-------------------- | :------- | :-------------------------------------------------------------------------- |
| `kind`     | `"data"` (literal)    | Yes      | Identifies this part as structured data.                                    |
| `data`     | `Record<string, any>` | Yes      | The structured JSON data payload (an object or an array).                   |
| `metadata` | `Record<string, any>` | No       | Optional metadata specific to this data part (e.g., reference to a schema). |

### 6.6.1 `FileWithBytes` Object

Represents the data for a file, used within a `FilePart`.

```ts { .no-copy }
--8<-- "types/src/types.ts:FileWithBytes"
```

| Field Name | Type     | Required | Description                                                                                                                         |
| :--------- | :------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `name`     | `string` | No       | Original filename (e.g., "report.pdf").                                                                                             |
| `mimeType` | `string` | No       | [Media Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) (e.g., `image/png`). Strongly recommended. |
| `bytes`    | `string` | Yes      | Base64 encoded file content.                                                                                                        |

### 6.6.2 `FileWithUri` Object

Represents the URI for a file, used within a `FilePart`.

```ts { .no-copy }
--8<-- "types/src/types.ts:FileWithUri"
```

| Field Name | Type     | Required | Description                                                                                                                         |
| :--------- | :------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `name`     | `string` | No       | Original filename (e.g., "report.pdf").                                                                                             |
| `mimeType` | `string` | No       | [Media Type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) (e.g., `image/png`). Strongly recommended. |
| `uri`      | `string` | Yes      | URI (absolute URL strongly recommended) to file content. Accessibility is context-dependent.                                        |

### 6.7. `Artifact` Object

Represents a tangible output generated by the agent during a task. Artifacts are the results or products of the agent's work.

```ts { .no-copy }
--8<-- "types/src/types.ts:Artifact"
```

| Field Name    | Type                            | Required | Description                                                                     |
| :------------ | :------------------------------ | :------- | ------------------------------------------------------------------------------- |
| `artifactId`  | `string`                        | Yes      | Identifier for the artifact generated by the agent.                             |
| `name`        | `string`                        | No       | Descriptive name for the artifact.                                              |
| `description` | `string`                        | No       | Human-readable description of the artifact.                                     |
| `parts`       | [`Part[]`](#65-part-union-type) | Yes      | Content of the artifact, as one or more `Part` objects. Must have at least one. |
| `metadata`    | `Record<string, any>`           | No       | Arbitrary key-value metadata associated with the artifact.                      |
| `extensions`  | `string[]`                 | No       | A list of extension URIs that contributed to this artifact.                         |

### 6.8. `PushNotificationConfig` Object

Configuration provided by the client to the server for sending asynchronous push notifications about task updates.

```ts { .no-copy }
--8<-- "types/src/types.ts:PushNotificationConfig"
```

| Field Name       | Type                                                                  | Required | Description                                                                                                                                                               |
| :--------------- | :-------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `url`            | `string`                                                              | Yes      | Absolute HTTPS webhook URL for the A2A Server to POST task updates to.                                                                                                    |
| `token`          | `string`                                                              | No       | Optional client-generated opaque token for the client's webhook receiver to validate the notification (e.g., server includes it in an `X-A2A-Notification-Token` header). |
| `authentication` | [`PushNotificationAuthenticationInfo`](#69-pushnotificationauthenticationinfo-object) | No       | Authentication details the A2A Server must use when calling the `url`. The client's webhook (receiver) defines these requirements.                                        |

### 6.9. `PushNotificationAuthenticationInfo` Object

A generic structure for specifying authentication requirements, typically used within `PushNotificationConfig` to describe how the A2A Server should authenticate to the client's webhook.

```ts { .no-copy }
--8<-- "types/src/types.ts:PushNotificationAuthenticationInfo"
```

| Field Name    | Type       | Required | Description                                                                                                                                                                                |
| :------------ | :--------- | :------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schemes`     | `string[]` | Yes      | Array of auth scheme names the A2A Server must use when calling the client's webhook (e.g., "Bearer", "ApiKey").                                                                           |
| `credentials` | `string`   | No       | Optional static credentials or scheme-specific configuration info. **Handle with EXTREME CAUTION if secrets are involved.** Prefer server-side dynamic credential fetching where possible. |

### 6.10. `TaskPushNotificationConfig` Object

Used as the `params` object for the [`tasks/pushNotificationConfig/set`](#75-taskspushnotificationconfigset) method and as the `result` object for the [`tasks/pushNotificationConfig/get`](#76-taskspushnotificationconfigget) method.

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskPushNotificationConfig"
```

| Field Name               | Type                                                          | Required | Description                                                                                                                           |
| :----------------------- | :------------------------------------------------------------ | :------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `taskId`                 | `string`                                                      | Yes      | The ID of the task to configure push notifications for, or retrieve configuration from.                                               |
| `pushNotificationConfig` | [`PushNotificationConfig`](#68-pushnotificationconfig-object) | Yes      | The push notification configuration. For `set`, the desired config. For `get`, the current config (secrets MAY be omitted by server). |

### 6.11. JSON-RPC Structures

A2A adheres to the standard [JSON-RPC 2.0](https://www.jsonrpc.org/specification) structures for requests and responses.

#### 6.11.1. `JSONRPCRequest` Object

All A2A method calls are encapsulated in a JSON-RPC Request object.

- `jsonrpc`: A String specifying the version of the JSON-RPC protocol. **MUST** be exactly `"2.0"`.
- `method`: A String containing the name of the method to be invoked (e.g., `"message/send"`, `"tasks/get"`).
- `params`: A Structured value that holds the parameter values to be used during the invocation of the method. This member **MAY** be omitted if the method expects no parameters. A2A methods typically use an `object` for `params`.
- `id`: An identifier established by the Client that **MUST** contain a String, Number, or `NULL` value if included. If it is not included it is assumed to be a notification. The value **SHOULD NOT** be `NULL` for requests expecting a response, and Numbers **SHOULD NOT** contain fractional parts. The Server **MUST** reply with the same value in the Response object if included. This member is used to correlate the context between the two objects. A2A methods typically expect a response or stream, so `id` will usually be present and non-null.

#### 6.11.2. `JSONRPCResponse` Object

Responses from the A2A Server are encapsulated in a JSON-RPC Response object.

- `jsonrpc`: A String specifying the version of the JSON-RPC protocol. **MUST** be exactly `"2.0"`.
- `id`: This member is **REQUIRED**. It **MUST** be the same as the value of the `id` member in the Request Object. If there was an error in detecting the `id` in the Request object (e.g. Parse error/Invalid Request), it **MUST** be `null`.
- **EITHER** `result`: This member is **REQUIRED** on success. This member **MUST NOT** exist if there was an error invoking the method. The value of this member is determined by the method invoked on the Server.
- **OR** `error`: This member is **REQUIRED** on failure. This member **MUST NOT** exist if there was no error triggered during invocation. The value of this member **MUST** be an [`JSONRPCError`](#612-jsonrpcerror-object) object.
- The members `result` and `error` are mutually exclusive: one **MUST** be present, and the other **MUST NOT**.

### 6.12. `JSONRPCError` Object

When a JSON-RPC call encounters an error, the Response Object will contain an `error` member with a value of this structure.

```ts { .no-copy }
--8<-- "types/src/types.ts:JSONRPCError"
```

| Field Name | Type      | Required | Description                                                                                                  |
| :--------- | :-------- | :------- | :----------------------------------------------------------------------------------------------------------- |
| `code`     | `integer` | Yes      | Integer error code. See [Section 8 (Error Handling)](#8-error-handling) for standard and A2A-specific codes. |
| `message`  | `string`  | Yes      | Short, human-readable summary of the error.                                                                  |
| `data`     | `any`     | No       | Optional additional structured information about the error.                                                  |

## 7. 프로토콜 RPC 메서드

모든 A2A RPC 메서드는 A2A 클라이언트가 A2A 서버의 `url`(`AgentCard`에 지정된 대로)에 HTTP POST 요청을 보내 호출합니다. HTTP POST 요청의 본문은 **반드시** `JSONRPCRequest` 객체여야 하며, `Content-Type` 헤더는 **반드시** `application/json`이어야 합니다.

A2A 서버의 HTTP 응답 본문은 **반드시** `JSONRPCResponse` 객체여야 합니다(또는 스트리밍 메서드의 경우 각 이벤트의 데이터가 `JSONRPCResponse`인 SSE 스트림). JSON-RPC 응답의 `Content-Type`은 `application/json`입니다. SSE 스트림의 경우 `text/event-stream`입니다.

### 7.1. `message/send`

새로운 상호 작용을 시작하거나 기존 상호 작용을 계속하기 위해 에이전트에 메시지를 보냅니다. 이 메서드는 동기식 요청/응답 상호 작용 또는 클라이언트 측 폴링(`tasks/get` 사용)이 장기 실행 작업을 모니터링하는 데 허용되는 경우에 적합합니다.

- **요청 `params` 유형**: [`MessageSendParams`](#711-messagesendparams-object)
- **응답 `result` 유형(성공 시)**: [`Task` | `Message`](#61-task-object) (메시지 객체 또는 메시지 처리 후 작업의 현재 또는 최종 상태).
- **응답 `error` 유형(실패 시)**: [`JSONRPCError`](#612-jsonrpcerror-object).

#### 7.1.1. `MessageSendParams` Object

```ts { .no-copy }
--8<-- "types/src/types.ts:MessageSendParams"

--8<-- "types/src/types.ts:MessageSendConfiguration"
```

| Field Name      | Type                                                            | Required | Description                                                        |
| :-------------- | :-------------------------------------------------------------- | :------- | :----------------------------------------------------------------- |
| `message`       | [`Message`](#64-message-object)                                 | Yes      | The message content to send. `Message.role` is typically `"user"`. |
| `configuration` | [`MessageSendConfiguration`](#711-messagesendparams-object) | No       | Optional: additional message configuration                         |
| `metadata`      | `Record<string, any>`                                           | No       | Request-specific metadata.                                         |

### 7.2. `message/stream`

Sends a message to an agent to initiate/continue a task AND subscribes the client to real-time updates for that task via Server-Sent Events (SSE). This method requires the server to have `AgentCard.capabilities.streaming: true`.

- **요청 `params` 유형**: [`MessageSendParams`](#711-messagesendparams-object) (same as `message/send`).
- **Response (on successful subscription)**:
    - HTTP Status: `200 OK`.
    - HTTP `Content-Type`: `text/event-stream`.
    - HTTP Body: A stream of Server-Sent Events. Each SSE `data` field contains a [`SendStreamingMessageResponse`](#721-sendstreamingmessageresponse-object) JSON object.
- **Response (on initial subscription failure)**:
    - Standard HTTP error code (e.g., 4xx, 5xx).
    - The HTTP body MAY contain a standard `JSONRPCResponse` with an `error` object detailing the failure.

#### 7.2.1. `SendStreamingMessageResponse` Object

This is the structure of the JSON object found in the `data` field of each Server-Sent Event sent by the server for a `message/stream` request or `tasks/resubscribe` request.

```ts { .no-copy }
--8<-- "types/src/types.ts:SendStreamingMessageResponse"

--8<-- "types/src/types.ts:SendStreamingMessageSuccessResponse"
```

| Field Name | Type                                                                                                                                                                                          | Required | Description                                                                            |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------- |
| `jsonrpc`  | `"2.0"` (literal)                                                                                                                                                                             | Yes      | JSON-RPC version string.                                                               |
| `id`       | `string` \| `number`                                                                                                                                                                          | Yes      | Matches the `id` from the originating `message/stream` or `tasks/resubscribe` request. |
| `result`   | **Either** `Message` <br> **OR** `Task` <br> **OR** [`TaskStatusUpdateEvent`](#722-taskstatusupdateevent-object) <br> **OR** [`TaskArtifactUpdateEvent`](#723-taskartifactupdateevent-object) | Yes      | The event payload                                                                      |

#### 7.2.2. `TaskStatusUpdateEvent` Object

Carries information about a change in the task's status during streaming. This is one of the possible `result` types in a `SendStreamingMessageSuccessResponse`.

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskStatusUpdateEvent"
```

| Field Name  | Type                                  | Required | Default         | Description                                                                                                                                      |
| :---------- | :------------------------------------ | :------- | :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| `taskId`    | `string`                              | Yes      |                 | Task ID being updated                                                                                                                            |
| `contextId` | `string`                              | Yes      |                 | Context ID the task is associated with                                                                                                           |
| `kind`      | `string`, literal                     | Yes      | `status-update` | Type discriminator, literal value                                                                                                                |
| `status`    | [`TaskStatus`](#62-taskstatus-object) | Yes      |                 | The new `TaskStatus` object.                                                                                                                     |
| `final`     | `boolean`                             | No       | `false`         | If `true`, indicates this is the terminal status update for the current stream cycle. The server typically closes the SSE connection after this. |
| `metadata`  | `Record<string, any>`                 | No       | `undefined`     | Event-specific metadata.                                                                                                                         |

#### 7.2.3. `TaskArtifactUpdateEvent` Object

Carries a new or updated artifact (or a chunk of an artifact) generated by the task during streaming. This is one of the possible `result` types in a `SendTaskStreamingResponse`.

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskArtifactUpdateEvent"
```

| Field Name  | Type                              | Required | Default           | Description                                                                |
| :---------- | :-------------------------------- | :------- | :---------------- | :------------------------------------------------------------------------- |
| `taskId`    | `string`                          | Yes      |                   | Task ID associated with the generated artifact part                        |
| `contextId` | `string`                          | Yes      |                   | Context ID the task is associated with                                     |
| `kind`      | `string`, literal                 | Yes      | `artifact-update` | Type discriminator, literal value                                          |
| `artifact`  | [`Artifact`](#67-artifact-object) | Yes      |                   | The `Artifact` data. Could be a complete artifact or an incremental chunk. |
| `append`    | `boolean`                         | No       | `false`           | `true` means append parts to artifact; `false` (default) means replace.    |
| `lastChunk` | `boolean`                         | No       | `false`           | `true` indicates this is the final update for the artifact.                |
| `metadata`  | `Record<string, any>`             | No       | `undefined`       | Event-specific metadata.                                                   |

### 7.3. `tasks/get`

Retrieves the current state (including status, artifacts, and optionally history) of a previously initiated task. This is typically used for polling the status of a task initiated with `message/send`, or for fetching the final state of a task after being notified via a push notification or after an SSE stream has ended.

- **Request `params` type**: [`TaskQueryParams`](#731-taskqueryparams-object)
- **Response `result` type (on success)**: [`Task`](#61-task-object) (A snapshot of the task's current state).
- **Response `error` type (on failure)**: [`JSONRPCError`](#612-jsonrpcerror-object) (e.g., if the task ID is not found, see [`TaskNotFoundError`](#82-a2a-specific-errors)).

#### 7.3.1. `TaskQueryParams` Object

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskQueryParams"
```

| Field Name      | Type                  | Required | Description                                                                              |
| :-------------- | :-------------------- | :------- | :--------------------------------------------------------------------------------------- |
| `id`            | `string`              | Yes      | The ID of the task whose current state is to be retrieved.                               |
| `historyLength` | `integer`             | No       | If positive, requests the server to include up to `N` recent messages in `Task.history`. |
| `metadata`      | `Record<string, any>` | No       | Request-specific metadata.                                                               |

### 7.4. `tasks/cancel`

Requests the cancellation of an ongoing task. The server will attempt to cancel the task, but success is not guaranteed (e.g., the task might have already completed or failed, or cancellation might not be supported at its current stage).

- **Request `params` type**: [`TaskIdParams`](#741-taskidparams-object-for-taskscancel-and-taskspushnotificationconfigget)
- **Response `result` type (on success)**: [`Task`](#61-task-object) (The state of the task after the cancellation attempt. Ideally, `Task.status.state` will be `"canceled"` if successful).
- **Response `error` type (on failure)**: [`JSONRPCError`](#612-jsonrpcerror-object) (e.g., [`TaskNotFoundError`](#82-a2a-specific-errors), [`TaskNotCancelableError`](#82-a2a-specific-errors)).

#### 7.4.1. `TaskIdParams` Object (for `tasks/cancel` and `tasks/pushNotificationConfig/get`)

A simple object containing just the task ID and optional metadata.

```ts { .no-copy }
--8<-- "types/src/types.ts:TaskIdParams"
```

| Field Name | Type                  | Required | Description                |
| :--------- | :-------------------- | :------- | :------------------------- |
| `id`       | `string`              | Yes      | The ID of the task.        |
| `metadata` | `Record<string, any>` | No       | Request-specific metadata. |

### 7.5. `tasks/pushNotificationConfig/set`

Sets or updates the push notification configuration for a specified task. This allows the client to tell the server where and how to send asynchronous updates for the task. Requires the server to have `AgentCard.capabilities.pushNotifications: true`.

- **Request `params` type**: [`TaskPushNotificationConfig`](#610-taskpushnotificationconfig-object)
- **Response `result` type (on success)**: [`TaskPushNotificationConfig`](#610-taskpushnotificationconfig-object) (Confirms the configuration that was set. The server MAY omit or mask any sensitive details like secrets from the `authentication.credentials` field in the response).
- **Response `error` type (on failure)**: [`JSONRPCError`](#612-jsonrpcerror-object) (e.g., [`PushNotificationNotSupportedError`](#82-a2a-specific-errors), [`TaskNotFoundError`](#82-a2a-specific-errors), errors related to invalid `PushNotificationConfig`).

### 7.6. `tasks/pushNotificationConfig/get`

Retrieves the current push notification configuration for a specified task. Requires the server to have `AgentCard.capabilities.pushNotifications: true`.

- **Request `params` type**: [`GetTaskPushNotificationConfigParams`](#761-gettaskpushnotificationconfigparams-object-taskspushnotificationconfigget) | [`TaskIdParams`](#741-taskidparams-object-for-taskscancel-and-taskspushnotificationconfigget)
_(Note: TaskIdParams type is deprecated for this method. Use GetTaskPushNotificationConfigParams instead.)_
- **Response `result` type (on success)**: [`TaskPushNotificationConfig`](#610-taskpushnotificationconfig-object) (The current push notification configuration for the task. Server may return an error if no push notification configuration is associated with the task).
- **Response `error` type (on failure)**: [`JSONRPCError`](#612-jsonrpcerror-object) (e.g., [`PushNotificationNotSupportedError`](#82-a2a-specific-errors), [`TaskNotFoundError`](#82-a2a-specific-errors)).

#### 7.6.1. `GetTaskPushNotificationConfigParams` Object (`tasks/pushNotificationConfig/get`)

A object for fetching the push notification configuration for a task.

```ts { .no-copy }
--8<-- "types/src/types.ts:GetTaskPushNotificationConfigParams"
```

| Field Name | Type                  | Required | Description                |
| :--------- | :-------------------- | :------- | :------------------------- |
| `id`       | `string`              | Yes      | The ID of the task.        |
| `pushNotificationConfigId`       | `string` | No      | Push notification configuration id. Server will return one of the associated configurations if config id is not specified |
| `metadata` | `Record<string, any>` | No       | Request-specific metadata. |

### 7.7. `tasks/pushNotificationConfig/list`

Retrieves the associated push notification configurations for a specified task. Requires the server to have `AgentCard.capabilities.pushNotifications: true`.

- **Request `params` type**: [`ListTaskPushNotificationConfigParams`](#771-listtaskpushnotificationconfigparams-object-taskspushnotificationconfiglist)
- **Response `result` type (on success)**: [`TaskPushNotificationConfig[]`](#610-taskpushnotificationconfig-object) (The push notification configurations associated with the task.).
- **Response `error` type (on failure)**: [`JSONRPCError`](#612-jsonrpcerror-object) (e.g., [`PushNotificationNotSupportedError`](#82-a2a-specific-errors), [`TaskNotFoundError`](#82-a2a-specific-errors)).

#### 7.7.1. `ListTaskPushNotificationConfigParams` Object (`tasks/pushNotificationConfig/list`)

A object for fetching the push notification configurations for a task.

```ts { .no-copy }
--8<-- "types/src/types.ts:ListTaskPushNotificationConfigRequest"
```

| Field Name | Type                  | Required | Description                |
| :--------- | :-------------------- | :------- | :------------------------- |
| `id`       | `string`              | Yes      | The ID of the task.        |
| `metadata` | `Record<string, any>` | No       | Request-specific metadata. |

### 7.8. `tasks/pushNotificationConfig/delete`

Deletes an associated push notification configuration for a task. Requires the server to have `AgentCard.capabilities.pushNotifications: true`.

- **Request `params` type**: [`DeleteTaskPushNotificationConfigParams`](#781-deletetaskpushnotificationconfigparams-object-taskspushnotificationconfigdelete)
- **Response `result` type (on success)**: [`null`]
- **Response `error` type (on failure)**: [`JSONRPCError`](#612-jsonrpcerror-object) (e.g., [`PushNotificationNotSupportedError`](#82-a2a-specific-errors), [`TaskNotFoundError`](#82-a2a-specific-errors)).

#### 7.8.1. `DeleteTaskPushNotificationConfigParams` Object (`tasks/pushNotificationConfig/delete`)

A object for deleting an associated push notification configuration for a task.

```ts { .no-copy }
--8<-- "types/src/types.ts:DeleteTaskPushNotificationConfigParams"
```

| Field Name | Type                  | Required | Description                |
| :--------- | :-------------------- | :------- | :------------------------- |
| `id`       | `string`              | Yes      | The ID of the task.        |
| `pushNotificationConfigId` | `string`   | Yes | Push notification configuration id |
| `metadata` | `Record<string, any>` | No       | Request-specific metadata. |

### 7.9. `tasks/resubscribe`

Allows a client to reconnect to an SSE stream for an ongoing task after a previous connection (from `message/stream` or an earlier `tasks/resubscribe`) was interrupted. Requires the server to have `AgentCard.capabilities.streaming: true`.

The purpose is to resume receiving _subsequent_ updates. The server's behavior regarding events missed during the disconnection period (e.g., whether it attempts to backfill some missed events or only sends new ones from the point of resubscription) is implementation-dependent and not strictly defined by this specification.

- **Request `params` type**: [`TaskIdParams`](#731-taskqueryparams-object)
- **Response (on successful resubscription)**:
    - HTTP Status: `200 OK`.
    - HTTP `Content-Type`: `text/event-stream`.
    - HTTP Body: A stream of Server-Sent Events, identical in format to `message/stream`, carrying _subsequent_ [`SendStreamingMessageResponse`](#721-sendstreamingmessageresponse-object) events for the task.
- **Response (on resubscription failure)**:
    - Standard HTTP error code (e.g., 4xx, 5xx).
    - The HTTP body MAY contain a standard `JSONRPCResponse` with an `error` object. Failures can occur if the task is no longer active, doesn't exist, or streaming is not supported/enabled for it.

### 7.10. `agent/authenticatedExtendedCard`

Retrieves a potentially more detailed version of the Agent Card after the client has authenticated. This endpoint is available only if `AgentCard.supportsAuthenticatedExtendedCard` is `true`. This is an HTTP GET endpoint, not a JSON-RPC method.

- **Endpoint URL**: `{AgentCard.url}/../agent/authenticatedExtendedCard` (relative to the base URL specified in the public Agent Card).
- **HTTP Method**: `GET`
- **Authentication**: The client **MUST** authenticate the request using one of the schemes declared in the public `AgentCard.securitySchemes` and `AgentCard.security` fields.
- **Request `params`**: None (HTTP GET request).
- **Response `result` type (on success)**: `AgentCard` (A complete Agent Card object, which may contain additional details or skills not present in the public card).
- **Response `error` type (on failure)**: Standard HTTP error codes.
    - `401 Unauthorized`: Authentication failed (missing or invalid credentials). The server **SHOULD** include a `WWW-Authenticate` header.
    - `403 Forbidden`: Authentication succeeded, but the client/user is not authorized to access the extended card.
    - `404 Not Found`: The `supportsAuthenticatedExtendedCard` capability is declared, but the server has not implemented this endpoint at the specified path.
    - `5xx Server Error`: An internal server error occurred.

Clients retrieving this authenticated card **SHOULD** replace their cached public Agent Card with the content received from this endpoint for the duration of their authenticated session or until the card's version changes.

#### 7.10.1. `AuthenticatedExtendedCardParams` Object

This endpoint does not use JSON-RPC `params`. Any parameters would be included as HTTP query parameters if needed (though none are defined by the standard).

#### 7.10.2. `AuthenticatedExtendedCardResponse` Object

The successful response body is a JSON object conforming to the `AgentCard` interface.

```ts { .no-copy }
--8<-- "types/src/types.ts:AuthenticatedExtendedCardResponse"
```

## 8. 오류 처리

A2A는 오류 보고를 위해 표준 [JSON-RPC 2.0 오류 코드 및 구조](https://www.jsonrpc.org/specification#error_object)를 사용합니다. 오류는 `JSONRPCErrorResponse` 객체의 `error` 멤버로 반환됩니다. [`JSONRPCError` 객체 정의](#612-jsonrpcerror-object)를 참조하십시오.

### 8.1. 표준 JSON-RPC 오류

이것들은 JSON-RPC 2.0 사양에 의해 정의된 표준 코드입니다.

| 코드                 | JSON-RPC 사양 의미    | 일반적인 A2A `message`    | 설명                                                                                         |
| :------------------- | :-------------------- | :------------------------ | :------------------------------------------------------------------------------------------- |
| `-32700`             | 구문 분석 오류        | 잘못된 JSON 페이로드      | 서버가 잘못된 형식의 JSON을 수신했습니다.                                                    |
| `-32600`             | 잘못된 요청           | 잘못된 JSON-RPC 요청      | JSON 페이로드는 유효한 JSON이었지만 유효한 JSON-RPC 요청 객체가 아닙니다.                      |
| `-32601`             | 메서드를 찾을 수 없음 | 메서드를 찾을 수 없음     | 요청된 A2A RPC `method`(예: `"tasks/foo"`)가 존재하지 않거나 지원되지 않습니다.            |
| `-32602`             | 잘못된 매개변수       | 잘못된 메서드 매개변수    | 메서드에 제공된 `params`가 잘못되었습니다(예: 잘못된 유형, 필수 필드 누락).                  |
| `-32603`             | 내부 오류             | 내부 서버 오류            | 처리 중 서버에서 예기치 않은 오류가 발생했습니다.                                            |
| `-32000` ~ `-32099`  | 서버 오류             | _(서버 정의)_             | 구현 정의 서버 오류를 위해 예약되었습니다. A2A 관련 오류는 이 범위를 사용합니다.            |

### 8.2. A2A 관련 오류

이것들은 A2A 관련 문제에 대한 보다 구체적인 피드백을 제공하기 위해 JSON-RPC 서버 오류 범위(`-32000` ~ `-32099`) 내에 정의된 사용자 지정 오류 코드입니다. 서버는 해당되는 경우 이러한 코드를 **사용해야 합니다**.

| 코드     | 오류 이름(개념)                     | 일반적인 `message` 문자열          | 설명                                                                                                                                                                                                                         |
| :------- | :---------------------------------- | :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-32001` | `TaskNotFoundError`                 | 작업을 찾을 수 없음                | 지정된 작업 `id`가 기존 또는 활성 작업에 해당하지 않습니다. 유효하지 않거나, 만료되었거나, 이미 완료되어 제거되었을 수 있습니다.                                                                                             |
| `-32002` | `TaskNotCancelableError`            | 작업을 취소할 수 없음              | 취소할 수 없는 상태의 작업을 취소하려고 시도했습니다(예: 이미 `completed`, `failed` 또는 `canceled`와 같은 최종 상태에 도달함).                                                                                                  |
| `-32003` | `PushNotificationNotSupportedError` | 푸시 알림이 지원되지 않음          | 클라이언트가 푸시 알림 기능(예: `tasks/pushNotificationConfig/set`)을 사용하려고 시도했지만 서버 에이전트가 지원하지 않습니다(즉, `AgentCard.capabilities.pushNotifications`가 `false`임).                                         |
| `-32004` | `UnsupportedOperationError`         | 이 작업은 지원되지 않음            | 요청된 작업 또는 특정 측면(아마도 매개변수에 의해 암시됨)이 이 서버 에이전트 구현에서 지원되지 않습니다. 메서드를 찾을 수 없음보다 더 광범위합니다.                                                                            |
| `-32005` | `ContentTypeNotSupportedError`      | 호환되지 않는 콘텐츠 유형          | 요청의 `message.parts`에 제공된 [미디어 유형](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)(또는 아티팩트에 대해 암시됨)이 에이전트 또는 호출되는 특정 기술에서 지원되지 않습니다.                      |
| `-32006` | `InvalidAgentResponseError`         | 잘못된 에이전트 응답 유형          | 에이전트가 요청된 메서드에 대해 잘못된 응답을 생성했습니다.                                                                                                                                                                  |

서버는 위에 설명되지 않은 보다 구체적인 시나리오에 대해 `-32000` ~ `-32099` 범위 내에서 추가 오류 코드를 정의할 **수 있지만**, 이를 명확하게 문서화해야 **합니다**. `JSONRPCError` 객체의 `data` 필드를 사용하여 모든 오류에 대한 보다 구조화된 세부 정보를 제공할 수 있습니다.

## 9. 일반적인 워크플로우 및 예제

이 섹션에서는 일반적인 A2A 상호 작용의 예시적인 JSON 예제를 제공합니다. 타임스탬프, 컨텍스트 ID 및 요청/응답 ID는 데모용입니다. 간결성을 위해 예제의 핵심이 아닌 일부 선택적 필드는 생략될 수 있습니다.

### 9.1. 인증된 확장 에이전트 카드 가져오기

**시나리오:** 클라이언트가 인증된 확장 카드를 지원함을 나타내는 공개 에이전트 카드를 발견하고 전체 세부 정보를 검색하려고 합니다.

1. **클라이언트가 공개 에이전트 카드를 가져옵니다:**

   ```none
   GET https://example.com/.well-known/agent.json
   ```

   _서버는 공개 에이전트 카드(섹션 5.6의 예제와 같이)로 응답하며, `supportsAuthenticatedExtendedCard: true`(루트 수준) 및 `securitySchemes`를 포함합니다._

2. **클라이언트가 공개 카드에서 필요한 인증을 식별합니다.**

3. **클라이언트가 대역 외에서 필요한 자격 증명을 얻습니다(예: Google로 OAuth 2.0 흐름을 수행하여 액세스 토큰을 얻음).**

4. **클라이언트가 인증된 확장 에이전트 카드를 가져옵니다:**

   ```none
   GET https://example.com/a2a/agent/authenticatedExtendedCard
   Authorization: Bearer <obtained_access_token>
   ```

5. **서버가 요청을 인증하고 권한을 부여합니다.**

6. **서버가 전체 에이전트 카드로 응답합니다:**

### 9.2. Basic Execution (Synchronous / Polling Style)

**Scenario:** Client asks a simple question, and the agent responds quickly with a task

1. **Client sends a message using `message/send`:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "tell me a joke"
           }
         ],
         "messageId": "9229e770-767c-417b-a0b0-f0741243c589"
       },
       "metadata": {}
     }
   }
   ```

2. **Server processes the request, creates a task and responds (task completes quickly)**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "id": "363422be-b0f9-4692-a24d-278670e7c7f1",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "status": {
         "state": "completed"
       },
       "artifacts": [
         {
           "artifactId": "9b6934dd-37e3-4eb1-8766-962efaab63a1",
           "name": "joke",
           "parts": [
             {
               "kind": "text",
               "text": "Why did the chicken cross the road? To get to the other side!"
             }
           ]
         }
       ],
       "history": [
         {
           "role": "user",
           "parts": [
             {
               "kind": "text",
               "text": "tell me a joke"
             }
           ],
           "messageId": "9229e770-767c-417b-a0b0-f0741243c589",
           "taskId": "363422be-b0f9-4692-a24d-278670e7c7f1",
           "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4"
         }
       ],
       "kind": "task",
       "metadata": {}
     }
   }
   ```

**Scenario:** Client asks a simple question, and the agent responds quickly without a task

1. **Client sends a message using `message/send`:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "tell me a joke"
           }
         ],
         "messageId": "9229e770-767c-417b-a0b0-f0741243c589"
       },
       "metadata": {}
     }
   }
   ```

2. **Server processes the request, responds quickly without a task**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "messageId": "363422be-b0f9-4692-a24d-278670e7c7f1",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "parts": [
         {
           "kind": "text",
           "text": "Why did the chicken cross the road? To get to the other side!"
         }
       ],
       "kind": "message",
       "metadata": {}
     }
   }
   ```

_If the task were longer-running, the server might initially respond with `status.state: "working"`. The client would then periodically call `tasks/get` with `params: {"id": "363422be-b0f9-4692-a24d-278670e7c7f1"}` until the task reaches a terminal state._

### 9.3. Streaming Task Execution (SSE)

**Scenario:** Client asks the agent to write a long paper describing an attached picture.

1. **Client sends a message and subscribes using `message/stream`:**

   ```json
   {
     "method": "message/stream",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "write a long paper describing the attached pictures"
           },
           {
             "kind": "file",
             "file": {
               "mimeType": "image/png",
               "data": "<base64-encoded-content>"
             }
           }
         ],
         "messageId": "bbb7dee1-cf5c-4683-8a6f-4114529da5eb"
       },
       "metadata": {}
     }
   }
   ```

2. **Server responds with HTTP 200 OK, `Content-Type: text/event-stream`, and starts sending SSE events:**

   _Event 1: Task status update - working_

   ```json
   data: {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "id": "225d6247-06ba-4cda-a08b-33ae35c8dcfa",
       "contextId": "05217e44-7e9f-473e-ab4f-2c2dde50a2b1",
       "status": {
         "state": "submitted",
         "timestamp":"2025-04-02T16:59:25.331844"
       },
       "history": [
         {
           "role": "user",
           "parts": [
             {
               "kind": "text",
               "text": "write a long paper describing the attached pictures"
             },
             {
               "kind": "file",
               "file": {
                 "mimeType": "image/png",
                 "data": "<base64-encoded-content>"
               }
             }
           ],
           "messageId": "bbb7dee1-cf5c-4683-8a6f-4114529da5eb",
           "taskId": "225d6247-06ba-4cda-a08b-33ae35c8dcfa",
           "contextId": "05217e44-7e9f-473e-ab4f-2c2dde50a2b1"
         }
       ],
       "kind": "task",
       "metadata": {}
     }
   }

   data: {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "taskId": "225d6247-06ba-4cda-a08b-33ae35c8dcfa",
       "contextId": "05217e44-7e9f-473e-ab4f-2c2dde50a2b1",
       "artifact": {
         "artifactId": "9b6934dd-37e3-4eb1-8766-962efaab63a1",
         "parts": [
           {"type":"text", "text": "<section 1...>"}
         ]
       },
       "append": false,
       "lastChunk": false,
       "kind":"artifact-update"
     }
   }

   data: {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "taskId": "225d6247-06ba-4cda-a08b-33ae35c8dcfa",
       "contextId": "05217e44-7e9f-473e-ab4f-2c2dde50a2b1",
       "artifact": {
         "artifactId": "9b6934dd-37e3-4eb1-8766-962efaab63a1",
         "parts": [
           {"type":"text", "text": "<section 2...>"}
         ],
       },
       "append": true,
       "lastChunk": false,
       "kind":"artifact-update"
     }
   }


   data: {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "taskId": "225d6247-06ba-4cda-a08b-33ae35c8dcfa",
       "contextId": "05217e44-7e9f-473e-ab4f-2c2dde50a2b1",
       "artifact": {
         "artifactId": "9b6934dd-37e3-4eb1-8766-962efaab63a1",
         "parts": [
           {"type":"text", "text": "<section 3...>"}
         ]
       },
       "append": true,
       "lastChunk": true,
       "kind":"artifact-update"
     }
   }

   data: {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "taskId": "225d6247-06ba-4cda-a08b-33ae35c8dcfa",
       "contextId": "05217e44-7e9f-473e-ab4f-2c2dde50a2b1",
       "status": {
         "state": "completed",
         "timestamp":"2025-04-02T16:59:35.331844"
       },
       "final": true,
       "kind":"status-update"
     }
   }
   ```

   _(Server closes the SSE connection after the `final:true` event)._

### 9.4. Multi-Turn Interaction (Input Required)

**Scenario:** Client wants to book a flight, and the agent needs more information.

1. **Client sends a message using `message/send`:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-003",
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [{ "kind": "text", "text": "I'd like to book a flight." }]
       },
       "messageId": "c53ba666-3f97-433c-a87b-6084276babe2"
     }
   }
   ```

2. **Server responds, task state is `input-required`:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-003",
     "result": {
       "id": "3f36680c-7f37-4a5f-945e-d78981fafd36",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "status": {
         "state": "input-required",
         "message": {
           "role": "agent",
           "parts": [
             {
               "kind": "text",
               "text": "Sure, I can help with that! Where would you like to fly to, and from where? Also, what are your preferred travel dates?"
             }
           ],
           "messageId": "c2e1b2dd-f200-4b04-bc22-1b0c65a1aad2",
           "taskId": "3f36680c-7f37-4a5f-945e-d78981fafd36",
           "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4"
         },
         "timestamp": "2024-03-15T10:10:00Z"
       },
       "history": [
         {
           "role": "user",
           "parts": [
             {
               "kind": "text",
               "text": "I'd like to book a flight."
             }
           ],
           "messageId": "c53ba666-3f97-433c-a87b-6084276babe2",
           "taskId": "3f36680c-7f37-4a5f-945e-d78981fafd36",
           "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4"
         }
       ],
       "kind": "task"
     }
   }
   ```

3. **Client `message/send` (providing the requested input, using the _same_ task ID):**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-004",
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "I want to fly from New York (JFK) to London (LHR) around October 10th, returning October 17th."
           }
         ],
         "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
         "taskId": "3f36680c-7f37-4a5f-945e-d78981fafd36",
         "messageId": "0db1d6c4-3976-40ed-b9b8-0043ea7a03d3"
       },
       "configuration": {
         "blocking": true
       }
     }
   }
   ```

4. **Server processes the new input and responds (e.g., task completed or more input needed):**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-004",
     "result": {
       "id": "3f36680c-7f37-4a5f-945e-d78981fafd36",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "status": {
         "state": "completed",
         "message": {
           "role": "agent",
           "parts": [
             {
               "kind": "text",
               "text": "Okay, I've found a flight for you. Confirmation XYZ123. Details are in the artifact."
             }
           ]
         }
       },
       "artifacts": [
         {
           "artifactId": "9b6934dd-37e3-4eb1-8766-962efaab63a1",
           "name": "FlightItinerary.json",
           "parts": [
             {
               "kind": "data",
               "data": {
                 "confirmationId": "XYZ123",
                 "from": "JFK",
                 "to": "LHR",
                 "departure": "2024-10-10T18:00:00Z",
                 "arrival": "2024-10-11T06:00:00Z",
                 "returnDeparture": "..."
               }
             }
           ]
         }
       ],
       "history": [
         {
           "role": "user",
           "parts": [
             {
               "kind": "text",
               "text": "I'd like to book a flight."
             }
           ],
           "messageId": "c53ba666-3f97-433c-a87b-6084276babe2",
           "taskId": "3f36680c-7f37-4a5f-945e-d78981fafd36",
           "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4"
         },
         {
           "role": "agent",
           "parts": [
             {
               "kind": "text",
               "text": "Sure, I can help with that! Where would you like to fly to, and from where? Also, what are your preferred travel dates?"
             }
           ],
           "messageId": "c2e1b2dd-f200-4b04-bc22-1b0c65a1aad2",
           "taskId": "3f36680c-7f37-4a5f-945e-d78981fafd36",
           "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4"
         },
         {
           "role": "user",
           "parts": [
             {
               "kind": "text",
               "text": "I want to fly from New York (JFK) to London (LHR) around October 10th, returning October 17th."
             }
           ],
           "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
           "taskId": "3f36680c-7f37-4a5f-945e-d78981fafd36",
           "messageId": "0db1d6c4-3976-40ed-b9b8-0043ea7a03d3"
         }
       ],
       "kind": "task",
       "metadata": {}
     }
   }
   ```

### 9.5. Push Notification Setup and Usage

**Scenario:** Client requests a long-running report generation and wants to be notified via webhook when it's done.

1. **Client `message/send` with `pushNotification` config:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-005",
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "Generate the Q1 sales report. This usually takes a while. Notify me when it's ready."
           }
         ],
         "messageId": "6dbc13b5-bd57-4c2b-b503-24e381b6c8d6"
       },
       "configuration": {
         "pushNotificationConfig": {
           "url": "https://client.example.com/webhook/a2a-notifications",
           "token": "secure-client-token-for-task-aaa",
           "authentication": {
             "schemes": ["Bearer"]
             // Assuming server knows how to get a Bearer token for this webhook audience,
             // or this implies the webhook is public/uses the 'token' for auth.
             // 'credentials' could provide more specifics if needed by the server.
           }
         }
       }
     }
   }
   ```

2. **Server acknowledges the task (e.g., status `submitted` or `working`):**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-005",
     "result": {
       "id": "43667960-d455-4453-b0cf-1bae4955270d",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "status": { "state": "submitted", "timestamp": "2024-03-15T11:00:00Z" }
       // ... other fields ...
     }
   }
   ```

3. **(Later) A2A Server completes the task and POSTs a notification to `https://client.example.com/webhook/a2a-notifications`:**

   - **HTTP Headers might include:**
     - `Authorization: Bearer <server_jwt_for_webhook_audience>` (if server authenticates to webhook)
     - `Content-Type: application/json`
     - `X-A2A-Notification-Token: secure-client-token-for-task-aaa`
   - **HTTP Body (Task object is sent as JSON payload):**

   ```json
   {
     "id": "43667960-d455-4453-b0cf-1bae4955270d",
     "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
     "status": { "state": "completed", "timestamp": "2024-03-15T18:30:00Z" },
     "kind": "task"
     // ... other fields ...
   }
   ```

4. **Client's Webhook Service:**

   - Receives the POST.
   - Validates the `Authorization` header (if applicable).
   - Validates the `X-A2A-Notification-Token`.
   - Internally processes the notification (e.g., updates application state, notifies end user).

### 9.6. File Exchange (Upload and Download)

**Scenario:** Client sends an image for analysis, and the agent returns a modified image.

1. **Client `message/send` with a `FilePart` (uploading image bytes):**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-007",
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "Analyze this image and highlight any faces."
           },
           {
             "kind": "file",
             "file": {
               "name": "input_image.png",
               "mimeType": "image/png",
               "bytes": "iVBORw0KGgoAAAANSUhEUgAAAAUA..." // Base64 encoded image data
             }
           }
         ],
         "messageId": "6dbc13b5-bd57-4c2b-b503-24e381b6c8d6"
       }
     }
   }
   ```

2. **Server processes the image and responds with a `FilePart` in an artifact (e.g., providing a URI to the modified image):**

   ```json
   {
     "jsonrpc": "2.0",
     "id": "req-007",
     "result": {
       "id": "43667960-d455-4453-b0cf-1bae4955270d",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "status": { "state": "completed", "timestamp": "2024-03-15T12:05:00Z" },
       "artifacts": [
         {
           "artifactId": "9b6934dd-37e3-4eb1-8766-962efaab63a1",
           "name": "processed_image_with_faces.png",
           "parts": [
             {
               "kind": "file",
               "file": {
                 "name": "output.png",
                 "mimeType": "image/png",
                 // Server might provide a URI to a temporary storage location
                 "uri": "https://storage.example.com/processed/task-bbb/output.png?token=xyz"
                 // Or, alternatively, it could return bytes directly:
                 // "bytes": "ASEDGhw0KGgoAAAANSUhEUgAA..."
               }
             }
           ]
         }
       ],
       "kind": "task"
     }
   }
   ```

### 9.7. Structured Data Exchange (Requesting and Providing JSON)

**Scenario:** Client asks for a list of open support tickets in a specific JSON format.

1. **Client `message/send`, `Part.metadata` hints at desired output schema/Media Type:**
   _(Note: A2A doesn't formally standardize schema negotiation in v0.2.0, but `metadata` can be used for such hints by convention between client/server)._

   ```json
   {
     "jsonrpc": "2.0",
     "id": 9,
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [
           {
             "kind": "text",
             "text": "Show me a list of my open IT tickets",
             "metadata": {
               "mimeType": "application/json",
               "schema": {
                 "type": "array",
                 "items": {
                   "type": "object",
                   "properties": {
                     "ticketNumber": { "type": "string" },
                     "description": { "type": "string" }
                   }
                 }
               }
             }
           }
         ],
         "messageId": "85b26db5-ffbb-4278-a5da-a7b09dea1b47"
       },
       "metadata": {}
     }
   }
   ```

2. **Server responds with structured JSON data:**

   ```json
   {
     "jsonrpc": "2.0",
     "id": 9,
     "result": {
       "id": "d8c6243f-5f7a-4f6f-821d-957ce51e856c",
       "contextId": "c295ea44-7543-4f78-b524-7a38915ad6e4",
       "status": {
         "state": "completed",
         "timestamp": "2025-04-17T17:47:09.680794"
       },
       "artifacts": [
         {
           "artifactId": "c5e0382f-b57f-4da7-87d8-b85171fad17c",
           "parts": [
             {
               "kind": "text",
               "text": "[{\"ticketNumber\":\"REQ12312\",\"description\":\"request for VPN access\"},{\"ticketNumber\":\"REQ23422\",\"description\":\"Add to DL - team-gcp-onboarding\"}]"
             }
           ]
         }
       ],
       "kind": "task"
     }
   }
   ```

These examples illustrate the flexibility of A2A in handling various interaction patterns and data types. Implementers should refer to the detailed object definitions for all fields and constraints.

## 10. Appendices

### 10.1. Relationship to MCP (Model Context Protocol)

A2A and MCP are complementary protocols designed for different aspects of agentic systems:

- **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/):** Focuses on standardizing how AI models and agents connect to and interact with **tools, APIs, data sources, and other external resources.** It defines structured ways to describe tool capabilities (like function calling in LLMs), pass inputs, and receive structured outputs. Think of MCP as the "how-to" for an agent to _use_ a specific capability or access a resource.
- **Agent2Agent Protocol (A2A):** Focuses on standardizing how independent, often opaque, **AI agents communicate and collaborate with each other as peers.** A2A provides an application-level protocol for agents to discover each other, negotiate interaction modalities, manage shared tasks, and exchange conversational context or complex results. It's about how agents _partner_ or _delegate_ work.

**How they work together:**
An A2A Client agent might request an A2A Server agent to perform a complex task. The Server agent, in turn, might use MCP to interact with several underlying tools, APIs, or data sources to gather information or perform actions necessary to fulfill the A2A task.

For a more detailed comparison, see the [A2A and MCP guide](./topics/a2a-and-mcp.md).

### 10.2. Security Considerations Summary

Security is a paramount concern in A2A. Key considerations include:

- **Transport Security:** Always use HTTPS with strong TLS configurations in production environments.
- **Authentication:**
    - Handled via standard HTTP mechanisms (e.g., `Authorization` header with Bearer tokens, API keys).
    - Requirements are declared in the `AgentCard`.
    - Credentials MUST be obtained out-of-band by the client.
    - A2A Servers MUST authenticate every request.
- **Authorization:**
    - A server-side responsibility based on the authenticated identity.
    - Implement the principle of least privilege.
    - Can be granular, based on skills, actions, or data.
- **Push Notification Security:**
    - Webhook URL validation (by the A2A Server sending notifications) is crucial to prevent SSRF.
    - Authentication of the A2A Server to the client's webhook is essential.
    - Authentication of the notification by the client's webhook receiver (verifying it came from the legitimate A2A Server and is relevant) is critical.
    - See the [Streaming & Asynchronous Operations guide](./topics/streaming-and-async.md#security-considerations-for-push-notifications) for detailed push notification security.
- **Input Validation:** Servers MUST rigorously validate all RPC parameters and the content/structure of data in `Message` and `Artifact` parts to prevent injection attacks or processing errors.
- **Resource Management:** Implement rate limiting, concurrency controls, and resource limits to protect agents from abuse or overload.
- **Data Privacy:** Adhere to all applicable privacy regulations for data exchanged in `Message` and `Artifact` parts. Minimize sensitive data transfer.

For a comprehensive discussion, refer to the [Enterprise-Ready Features guide](./topics/enterprise-ready.md).
