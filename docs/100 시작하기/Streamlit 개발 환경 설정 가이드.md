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
