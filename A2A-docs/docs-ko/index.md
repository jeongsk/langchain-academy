---
hide:
  - navigation
  - toc
---

# Agent2Agent (A2A) 프로토콜

![A2A 배너](assets/a2a-banner.png){width="70%"}
{style="text-align: center; margin-bottom:1em; margin-top:1em;"}

## 협업 에이전트 시나리오 활성화

**Agent2Agent (A2A) 프로토콜**은 AI 에이전트 간의 원활한 통신과 협업을 가능하게 하도록 설계된 개방형 표준입니다. 다양한 프레임워크를 사용하고 여러 공급업체에서 구축한 에이전트가 존재하는 세상에서, A2A는 공통 언어를 제공하여 사일로를 허물고 상호 운용성을 증진합니다.

- [블로그 게시물: Agent2Agent 프로토콜(A2A) 발표](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [A2A 데모 비디오 시청](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/A2A_demo_v4.mp4)

### A2A 소개 비디오

<iframe src="https://www.linkedin.com/embed/feed/update/urn:li:ugcPost:7336822404003807232?compact=1" height="399" width="504" frameborder="0" allowfullscreen="" title="A2A 프로토콜 소개 비디오"></iframe>

---

### A2A가 중요한 이유

![A2A 메인 그래픽](assets/a2a-main.png){width="50%"}
{style="text-align: center; margin-bottom:1em; margin-top:2em;"}

<div class="grid cards" markdown>

- :material-account-group-outline:{ .lg .middle } **상호 운용성**

    다양한 플랫폼(LangGraph, CrewAI, Semantic Kernel, 맞춤형 솔루션)에 구축된 에이전트를 연결하여 강력한 복합 AI 시스템을 만듭니다.

- :material-lan-connect:{ .lg .middle } **복잡한 워크플로우**

    단일 에이전트로는 해결할 수 없는 복잡한 문제를 해결하기 위해 에이전트가 하위 작업을 위임하고, 정보를 교환하며, 행동을 조정할 수 있도록 합니다.

- :material-shield-key-outline:{ .lg .middle } **보안 및 불투명성**

    에이전트는 내부 메모리, 도구 또는 독점적인 로직을 공유할 필요 없이 상호 작용하여 보안을 보장하고 지적 재산권을 보호합니다.

</div>

---

### A2A와 MCP: 상호 보완적인 프로토콜

![A2A MCP 그래픽](assets/a2a-mcp-readme.png){width="60%"}
{style="text-align: center; margin-bottom:1em; margin-top:1em;"}

A2A와 [모델 컨텍스트 프로토콜(MCP)](https://modelcontextprotocol.io/)은 강력한 에이전트 애플리케이션 구축을 위한 상호 보완적인 표준입니다.

- **MCP (모델 컨텍스트 프로토콜):** 구조화된 입력/출력으로 에이전트를 **도구, API, 리소스**에 연결합니다. 에이전트가 자신의 기능에 접근하는 방식이라고 생각할 수 있습니다.
- **A2A (Agent2Agent 프로토콜):** 서로 다른 에이전트 간의 **동적, 다중 모드 통신**을 피어(peer)로서 촉진합니다. 에이전트가 협업하고, 위임하며, 공유 작업을 관리하는 방식입니다.

[A2A와 MCP에 대해 자세히 알아보기](./topics/a2a-and-mcp.md)

---

### A2A 시작하기

<div class="grid cards" markdown>

- :material-book-open:{ .lg .middle } **소개 읽기**

    A2A의 핵심 아이디어를 이해합니다.

    [:octicons-arrow-right-24: A2A란 무엇인가?](./topics/what-is-a2a.md)

    [:octicons-arrow-right-24: 주요 개념](./topics/key-concepts.md)

- :material-file-document-outline:{ .lg .middle } **사양 자세히 살펴보기**

    A2A 프로토콜의 상세한 기술적 정의를 탐색합니다.

    [:octicons-arrow-right-24: 프로토콜 사양](./specification.md)

- :material-application-cog-outline:{ .lg .middle } **튜토리얼 따라 하기**

    단계별 Python 빠른 시작 가이드를 통해 첫 A2A 호환 에이전트를 구축합니다.

    [:octicons-arrow-right-24: Python 튜토리얼](./tutorials/python/1-introduction.md)

- :material-code-braces:{ .lg .middle } **코드 샘플 탐색하기**

    샘플 클라이언트, 서버, 에이전트 프레임워크 통합을 통해 A2A의 실제 작동을 확인합니다.

    [:fontawesome-brands-github: GitHub 샘플](https://github.com/google-a2a/a2a-samples)

</div>
