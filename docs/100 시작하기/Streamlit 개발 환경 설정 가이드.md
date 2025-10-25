---
created: 2025-10-25 16:08:49
updated: 2025-10-25 16:14:20
---
## 소개

이 가이드는 Streamlit 프로젝트를 시작하는 데 필요한 Python 개발 환경을 터미널 명령어를 사용하여 설정하는 방법을 단계별로 안내합니다.

`streamlit-app`이라는 예제 프로젝트를 통해 Python 3.12 기반의 독립된 가상 환경을 만들고, 여기에 Streamlit 라이브러리를 설치하는 전체 과정을 다룹니다. 이 과정을 따라 하면 프로젝트별로 깔끔하게 분리된 개발 환경을 구성할 수 있습니다.

## 1. 프로젝트 폴더 생성

`streamlit-app`이라는 이름의 새 프로젝트 폴더를 만듭니다.

```bash
mkdir streamlit-app
cd streamlit-app
```

## 2. Python 가상 환경 생성

`pyenv`를 사용하여 이 프로젝트만을 위한 격리된 Python 가상 환경을 생성합니다. 다음 명령어는 Python 3.12 버전을 기반으로 `streamlit-app`이라는 이름의 가상 환경을 만듭니다.

```bash
pyenv virtualenv 3.12 streamlit-app
```

> **Tip:** 가상 환경은 프로젝트별 의존성 격리를 통해 시스템 전역 라이브러리와의 충돌을 방지하고, 협업 시 동일한 개발 환경을 보장하는 좋은 방법입니다.

## 3. 로컬 Python 환경 설정

현재 디렉터리(`streamlit-app` 폴더)에서 사용할 Python 환경을 방금 만든 `streamlit-app` 가상 환경으로 지정합니다.  이제 이 폴더에 진입하면 자동으로 지정된 가상 환경이 활성화됩니다.

```bash
pyenv local streamlit-app
```

## 4. Streamlit 라이브러리 설치

현재 활성화된 가상 환경에 `streamlit` 라이브러리를 설치합니다. `streamlit`은 데이터 기반의 웹 애플리케이션을 쉽게 만들 수 있도록 도와주는 인기 있는 Python 프레임워크입니다.

```bash
pip install streamlit
```


## 심화 학습: `pyenv virtualenv` vs `python -m venv`

`pyenv virtualenv`와 Python에 내장된 `venv` 모듈은 모두 가상 환경을 생성하지만, 관리 범위와 목적에 중요한 차이가 있습니다.

-   **`python -m venv`**: **패키지 격리**에 중점을 둡니다. 현재 시스템에서 활성화된 단일 Python 버전 내에서 프로젝트별 라이브러리 충돌을 방지합니다. 하지만 Python 인터프리터 버전 자체를 바꾸지는 못합니다.

-   **`pyenv virtualenv`**: **Python 버전 관리와 패키지 격리**를 모두 수행합니다. `pyenv`로 설치한 여러 Python 버전 중 특정 버전을 선택해 가상 환경을 만들 수 있어, "이 프로젝트는 반드시 Python 3.12에서 실행되어야 한다"와 같은 엄격한 요구사항을 충족시킬 수 있습니다.

이 가이드에서 `pyenv virtualenv`를 사용하는 이유는 프로젝트마다 각기 다른 Python 버전을 명확하게 지정하고 일관된 개발 환경을 보장하기 위함입니다.
