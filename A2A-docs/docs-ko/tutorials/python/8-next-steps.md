# 다음 단계

A2A Python SDK 튜토리얼을 완료하신 것을 축하합니다! 여러분은 다음을 배웠습니다:

-   A2A 개발을 위한 환경 설정 방법.
-   SDK의 타입을 사용하여 에이전트 기술(Agent Skills) 및 에이전트 카드(Agent Cards)를 정의하는 방법.
-   기본적인 HelloWorld A2A 서버 및 클라이언트 구현 방법.
-   스트리밍 기능 이해 및 구현 방법.
-   LangGraph를 사용하여 더 복잡한 에이전트를 통합하고, 작업 상태 관리 및 도구 사용을 시연하는 방법.

이제 여러분은 자신만의 A2A 호환 에이전트를 구축하고 통합하기 위한 견고한 기반을 갖추게 되었습니다.

## 다음에는 무엇을 할까요?

A2A 여정을 계속하기 위한 몇 가지 아이디어와 자료는 다음과 같습니다:

-   **다른 예제 탐색:**
    -   더 복잡한 에이전트 통합 및 기능을 보려면 [A2A GitHub 저장소](https://github.com/google-a2a/a2a-samples/tree/main/samples)의 `a2a-samples/samples/` 디렉토리에 있는 다른 예제들을 확인해 보세요.
    -   메인 A2A 저장소에는 [다른 언어 및 프레임워크를 위한 샘플](https://github.com/google-a2a/A2A/tree/main/samples)도 있습니다.
-   **프로토콜 이해 심화:**
    -   📚 포괄적인 개요를 보려면 전체 [A2A 프로토콜 문서 사이트](https://google.github.io/A2A/)를 읽어보세요.
    -   📝 모든 데이터 구조와 RPC 메서드의 미묘한 차이를 이해하려면 상세한 [A2A 프로토콜 사양](../../specification.md)을 검토하세요.
-   **주요 A2A 주제 검토:**
    -   [A2A와 MCP](../../topics/a2a-and-mcp.md): A2A가 도구 사용을 위해 모델 컨텍스트 프로토콜(MCP)을 어떻게 보완하는지 이해합니다.
    -   [엔터프라이즈급 기능](../../topics/enterprise-ready.md): 보안, 관찰 가능성 및 기타 엔터프라이즈 고려 사항에 대해 알아봅니다.
    -   [스트리밍 및 비동기 작업](../../topics/streaming-and-async.md): SSE 및 푸시 알림에 대한 자세한 내용을 확인합니다.
    -   [에이전트 발견](../../topics/agent-discovery.md): 에이전트가 서로를 찾는 다양한 방법을 탐색합니다.
-   **나만의 에이전트 구축:**
    -   선호하는 Python 에이전트 프레임워크(예: LangChain, CrewAI, AutoGen, Semantic Kernel 또는 사용자 지정 솔루션)를 사용하여 새로운 A2A 에이전트를 만들어 보세요.
    -   에이전트의 로직을 A2A 프로토콜과 연결하기 위해 `a2a.server.AgentExecutor` 인터페이스를 구현합니다.
    -   에이전트가 제공할 수 있는 고유한 기술과 에이전트 카드가 이를 어떻게 나타낼지 생각해 보세요.
-   **고급 기능 실험:**
    -   에이전트가 장기 실행 또는 다중 세션 작업을 처리하는 경우 영구 `TaskStore`로 강력한 작업 관리를 구현합니다.
    -   에이전트 작업이 매우 오래 지속되는 경우 푸시 알림 구현을 탐색합니다.
    -   더 복잡한 입력 및 출력 양식(예: 파일 업로드/다운로드 처리 또는 `DataPart`를 통한 구조화된 데이터)을 고려합니다.
-   **A2A 커뮤니티에 기여:**
    -   [A2A GitHub 토론 페이지](https://github.com/google-a2a/A2A/discussions)에서 토론에 참여하세요.
    -   [GitHub 이슈](https://github.com/google-a2a/A2A/issues)를 통해 문제를 보고하거나 개선 사항을 제안하세요.
    -   코드, 예제 또는 문서 기여를 고려해 보세요. [CONTRIBUTING.md](https://github.com/google-a2a/A2A/blob/main/CONTRIBUTING.md) 가이드를 참조하세요.

A2A 프로토콜은 상호 운용 가능한 AI 에이전트 생태계를 육성하는 것을 목표로 합니다. A2A 호환 에이전트를 구축하고 공유함으로써 이 흥미로운 개발의 일부가 될 수 있습니다!
