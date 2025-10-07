# 환경 설정

본 강좌를 시작하기 위한 권장 설정입니다. [여기](https://github.com/jeongsk/langchain-academy)에 위치한 노트북 세트를 사용할 예정입니다.

## Python 버전

!!! warning "중요"
    본 강좌를 최대한 활용하시려면 **Python 3.12** 을 사용 중인지 확인해 주세요. 이 버전은 LangGraph와의 최적 호환성을 위해 필수입니다.

현재 Python 버전을 확인하려면:

```bash
python3 --version
```

## 저장소 복제

GitHub에서 프로젝트를 복제합니다:

```bash
git clone https://github.com/jeongsk/langchain-academy.git
cd langchain-academy
```

## 환경 생성 및 종속성 설치

### uv 사용 (권장)

uv를 사용하여 환경을 생성하고 종속성을 설치합니다:

```bash
# uv가 설치되어 있지 않다면 먼저 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 가상환경 생성 및 종속성 설치
uv sync

# 가상환경 활성화 (필요한 경우)
source .venv/bin/activate
```

uv를 사용하여 직접 명령을 실행할 수도 있습니다:

```bash
uv run jupyter notebook
```

### 기존 pip 사용

기존 pip를 사용하여 설치하려면:

```bash
# 가상환경 생성
python3 -m venv .venv
source .venv/bin/activate

# 종속성 설치
pip install -r requirements.txt
```

## Jupyter 노트북 실행

Jupyter가 설치되어 있지 않다면, [여기](https://jupyter.org/install)의 설치 안내를 따르세요.

```bash
jupyter notebook
```

## API 키 설정

### LangSmith 설정

[LangSmith](https://smith.langchain.com/)에서 가입하고 API 키를 발급받으세요. LangSmith 문서는 [여기](https://docs.smith.langchain.com/)에서 참조할 수 있습니다.

환경 변수를 설정하세요:

```bash
export LANGSMITH_API_KEY="your-key"
export LANGSMITH_TRACING_V2=true
export LANGSMITH_PROJECT="langchain-academy"
```

또는 `.env` 파일에 추가하세요:

```env
LANGSMITH_API_KEY="your-key"
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT="langchain-academy"
```

### OpenAI API 키 설정

OpenAI API 키가 없다면 [여기](https://openai.com/index/openai-api/)에서 가입할 수 있습니다.

환경 변수를 설정하세요:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Tavily 웹 검색용 API 키

Tavily Search API는 대규모 언어 모델(LLM)과 RAG(Retrieval-Augmented Generation)에 최적화된 검색 엔진입니다. API 키는 [여기](https://tavily.com/)에서 신청할 수 있습니다.

환경 변수를 설정하세요:

```bash
export TAVILY_API_KEY="your-tavily-api-key"
```

## LangGraph Studio 설정

!!! info "LangGraph Studio 소개"
    LangGraph Studio는 에이전트를 확인하고 테스트하기 위한 맞춤형 통합 개발 환경(IDE)입니다.

### 설치 및 실행

Studio는 로컬에서 실행할 수 있으며 Mac, Windows, Linux에서 브라우저로 열 수 있습니다.

각 모듈의 `/studio` 디렉터리에서 터미널에 다음 명령을 실행하세요:

```bash
langgraph dev
```

다음과 같은 출력이 표시되어야 합니다:

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

브라우저를 열고 Studio UI로 이동하세요: `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`

### 환경 파일 생성

Studio를 사용하려면 관련 API 키가 포함된 `.env` 파일을 생성해야 합니다.

모듈 1부터 6까지의 파일을 생성하려면 다음을 실행하세요:

```bash
for i in {1..6}; do
  cp module-$i/studio/.env.example module-$i/studio/.env
  echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > module-$i/studio/.env
done
echo "TAVILY_API_KEY=\"$TAVILY_API_KEY\"" >> module-4/studio/.env
```

## 문제 해결

### 일반적인 문제들

#### Python 버전 문제
- Python 3.12 이상을 사용하고 있는지 확인하세요
- `pyenv` 또는 `conda`를 사용하여 올바른 Python 버전을 설치하세요

#### 패키지 설치 문제
- 가상환경이 활성화되어 있는지 확인하세요
- pip를 최신 버전으로 업그레이드하세요: `pip install --upgrade pip`

#### Jupyter 커널 문제
- 가상환경을 Jupyter 커널로 추가하세요:
  ```bash
  python -m ipykernel install --user --name=langchain-academy
  ```

!!! tip "도움이 필요한가요?"
    문제가 발생하면 [GitHub Issues](https://github.com/jeongsk/langchain-academy/issues)에 문의하세요.