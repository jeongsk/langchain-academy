# 2. 환경 설정

## 사전 요구 사항

- Python 3.10 이상.
- 터미널 또는 명령 프롬프트에 접근 가능해야 합니다.
- 저장소 복제를 위한 Git.
- 코드 편집기 (예: Visual Studio Code) 사용을 권장합니다.

## 저장소 복제

아직 복제하지 않았다면, A2A 샘플 저장소를 복제합니다:

```bash
git clone https://github.com/google-a2a/a2a-samples.git -b main --depth 1
cd a2a-samples
```

## Python 환경 및 SDK 설치

Python 프로젝트에는 가상 환경 사용을 권장합니다. A2A Python SDK는 의존성 관리를 위해 `uv`를 사용하지만, `venv`와 함께 `pip`를 사용할 수도 있습니다.

1.  **가상 환경 생성 및 활성화:**

    `venv` (표준 라이브러리) 사용:

    === "Mac/Linux"

        ```sh
        python -m venv .venv
        source .venv/bin/activate
        ```

    === "Windows"

        ```powershell
        python -m venv .venv
        .venv\Scripts\activate
        ```

2.  **A2A SDK 및 해당 의존성과 함께 필요한 Python 의존성 설치:**

    ```bash
    pip install -r samples/python/requirements.txt
    ```

## 설치 확인

설치 후, Python 인터프리터에서 `a2a` 패키지를 가져올 수 있어야 합니다:

```bash
python -c "import a2a; print('A2A SDK를 성공적으로 가져왔습니다')"
```

이 명령이 오류 없이 실행되고 성공 메시지를 출력하면, 환경이 올바르게 설정된 것입니다.
