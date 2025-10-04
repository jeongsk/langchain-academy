# A2A 문서

## 게시된 A2A 문서

[`https://google-a2a.github.io/A2A`](https://google-a2a.github.io/A2A)

## A2A 문서 개발 방법

1. 이 저장소를 복제(clone)하고 저장소 디렉터리로 `cd` 명령을 사용하여 이동합니다.
2. `pip install -r requirements-docs.txt` 명령을 실행합니다.
3. `mkdocs serve` 명령을 실행하고, `.md` 파일을 편집하며 실시간 미리보기를 확인합니다.
4. 일반적인 방법으로 문서 변경 사항에 기여합니다.

## 작동 방식

- A2A 문서는 [mkdocs](https://www.mkdocs.org/)와 [mkdocs-material 테마](https://squidfunk.github.io/mkdocs-material/)를 사용합니다.
- A2A 문서와 관련된 모든 원본 문서 및 마크다운 파일은 A2A 저장소의 `docs/` 디렉터리에 있습니다.
- 저장소 루트의 `mkdocs.yml` 파일에는 사이트 탐색 및 구성을 포함한 모든 문서 설정이 들어 있습니다.
- `.github/workflows/docs.yml` 경로에는 GitHub Action이 있으며, 이 Action은 문서를 빌드하고 게시하며, `mkdocs gh-deploy --force` 명령을 사용하여 빌드된 결과물을 이 저장소의 `gh-pages` 브랜치로 푸시합니다. 이 과정은 `main` 브랜치에 대한 모든 커밋 및 병합 시 자동으로 수행됩니다.
- A2A 문서는 GitHub Pages에서 호스팅되며, 이에 대한 설정은 GitHub 내 A2A 저장소 설정에 있습니다.
