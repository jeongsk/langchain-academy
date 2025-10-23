# LangGraph Academy

## 소개

LangGraph Academy에 오신 것을 환영합니다! 본 아카데미는 LangGraph를 기초부터 실전 프로젝트까지 체계적으로 학습할 수 있는 종합 과정입니다.

아카데미는 세 가지 주요 트랙으로 구성되어 있습니다:

- **Foundation**: LangGraph 기초 개념부터 배포까지 단계별 학습
- **Ambient Agents**: 실전 프로젝트를 통한 심화 학습
- **Tutorial**: 다양한 패턴과 예제를 통한 확장 학습

각 과정에는 동영상 강의, 노트북, 그리고 LangGraph Studio 통합이 포함되어 있습니다.

## 목차

### 📚 [Foundation Introduction to LangGraph](./langgraph-foundation/README.md)

LangGraph의 기초부터 프로덕션 배포까지 여섯 개의 모듈로 구성된 입문 과정입니다.

- **[Module 1: LangGraph 입문](./langgraph-foundation/module-1/README.md)**: 그래프, 노드, 에지의 기초부터 에이전트 구축까지
- **[Module 2: 상태 관리와 메모리](./langgraph-foundation/module-2/README.md)**: 고급 상태 관리 기법과 메모리 시스템
- **[Module 3: Human-in-the-Loop](./langgraph-foundation/module-3/README.md)**: 사람이 개입하는 워크플로우 구현
- **[Module 4: 고급 LangGraph 기술](./langgraph-foundation/module-4/README.md)**: 병렬 처리, 서브그래프, 맵리듀스 패턴
- **[Module 5: LangGraph 메모리 심화](./langgraph-foundation/module-5/README.md)**: BaseStore와 StateSchema를 활용한 메모리 관리
- **[Module 6: LangGraph 서버 배포 및 연결](./langgraph-foundation/module-6/README.md)**: 프로덕션 배포 및 클라이언트 연결

### 🚀 [Project: Ambient Agents with LangGraph](./projects/ambient-agents/README.md)

실전 프로젝트를 통해 Ambient Agents를 구현하며 학습하는 프로젝트 중심 실습 과정입니다.

- **[Project 1](./projects/ambient-agents/project-1/README.md)**: [프로젝트 제목 - 학습 중 업데이트 예정]
- **[Project 2](./projects/ambient-agents/project-2/README.md)**: [프로젝트 제목 - 학습 중 업데이트 예정]
- **[Project 3](./projects/ambient-agents/project-3/README.md)**: [프로젝트 제목 - 학습 중 업데이트 예정]

### 💡 [Tutorial & Examples](./langgraph-tutorial/README.md)

다양한 패턴과 고급 기법을 다루는 독립적인 예제 및 참고 자료입니다.

## 설정

본 강좌를 시작하기 위한 권장 설정입니다. [여기](https://github.com/jeongsk/langchain-academy)에 위치한 노트북 세트를 사용할 예정입니다.

### Python 버전

본 강좌를 최대한 활용하시려면 **Python 3.12**을 사용 중인지 확인해 주세요. 이 버전은 LangGraph와의 최적 호환성을 위해 필수입니다. 구버전을 사용 중이라면 업그레이드하시면 모든 기능이 원활하게 실행됩니다.

```shell
python3 --version
```

### 저장소 복제

```shell
git clone https://github.com/jeongsk/langchain-academy.git
$ cd langchain-academy
```

#### 환경 생성 및 종속성 설치

uv를 사용하여 환경을 생성하고 종속성을 설치합니다:

```shell
# uv가 설치되어 있지 않다면 먼저 설치
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# 가상환경 생성 및 종속성 설치
$ uv sync

# 가상환경 활성화 (필요한 경우)
$ source .venv/bin/activate
```

또는 uv를 사용하여 직접 명령을 실행할 수도 있습니다:

```shell
uv run jupyter notebook
```

### 노트북 실행하기

Jupyter가 설치되어 있지 않다면, [여기](https://jupyter.org/install)의 설치 안내를 따르세요.

```sh
jupyter notebook
```

### LangSmith에 가입하세요

[여기](https://smith.langchain.com/)에서 가입하세요. LangSmith 문서는 [여기](https://docs.smith.langchain.com/)에서 참조할 수 있습니다.

그런 다음 환경에서 다음을 설정하십시오.

```shell
LANGSMITH_API_KEY="your-key"
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT="langchain-academy"
```

### OpenAI API 키 설정

OpenAI API 키가 없다면 [여기](https://openai.com/index/openai-api/)에서 가입할 수 있습니다.

그런 다음 환경에서 `OPENAI_API_KEY`를 설정하십시오.

### Tavily 웹 검색용

Tavily Search API는 대규모 언어 모델(LLM)과 RAG(Retrieval-Augmented Generation)에 최적화된 검색 엔진으로, 효율적이고 신속하며 지속적인 검색 결과를 목표로 합니다. API 키는 [여기](https://tavily.com/)에서 신청할 수 있습니다. 가입 절차는 간단하며 풍부한 무료 이용권을 제공합니다. 모듈 4의 일부 강의에서는 Tavily를 활용할 예정입니다.

그런 다음 환경에서 `TAVILY_API_KEY`를 설정하십시오.

#### LangGraph Studio 설정하기

- LangGraph Studio는 에이전트를 확인하고 테스트하기 위한 맞춤형 통합 개발 환경(IDE)입니다.
- Studio는 로컬에서 실행할 수 있으며 Mac, Windows, Linux에서 브라우저로 열 수 있습니다.
- 로컬 Studio 개발 서버에 대한 설명은 [여기](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/#local-development-server)와 [여기](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/)를 참조하세요.
- LangGraph Studio용 그래프는 langgraph-foundation/module-X/studio/ 및 projects/ambient-agents/project-X/studio/ 폴더에 있습니다.
- 로컬 개발 서버를 시작하려면 각 모듈의 /studio 디렉터리에서 터미널에 다음 명령을 실행하세요:

```shell
langgraph dev
```

다음과 같은 출력이 표시되어야 합니다:

- 🚀 API: <http://127.0.0.1:2024>
- 🎨 Studio UI: <https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024>
- 📚 API Docs: [http://127.0.0.1:2024/docs](http://127.0.0.1:2024/docs)

브라우저를 열고 Studio UI로 이동하세요: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

- Studio를 사용하려면 관련 API 키가 포함된 .env 파일을 생성해야 합니다
- 예를 들어 모듈 1부터 6까지의 파일을 생성하려면 명령줄에서 다음을 실행하세요:

```bash
# Foundation 모듈 .env 설정
for i in {1..6}; do
  cp langgraph-foundation/module-$i/studio/.env.example langgraph-foundation/module-$i/studio/.env
  echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > langgraph-foundation/module-$i/studio/.env
done
echo "TAVILY_API_KEY=\"$TAVILY_API_KEY\"" >> langgraph-foundation/module-4/studio/.env

# Ambient Agents 프로젝트 .env 설정 (프로젝트 생성 후)
for i in {1..6}; do
  if [ -d "projects/ambient-agents/project-$i/studio" ]; then
    cp projects/ambient-agents/project-$i/studio/.env.example projects/ambient-agents/project-$i/studio/.env
    echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > projects/ambient-agents/project-$i/studio/.env
  fi
done
```

## 리소스

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain 공식 문서](https://python.langchain.com/)
- [LangSmith](https://smith.langchain.com/)
- [GitHub 저장소](https://github.com/langchain-ai)
