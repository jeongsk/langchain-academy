---
title: "MarkItDown: 파일을 Markdown으로 변환하는 Microsoft 오픈소스 도구"
author: Microsoft
repository: https://github.com/microsoft/markitdown
license: MIT
created: 2025-10-25
stars: 82.1k
tags:
  - Microsoft
  - 마크다운
  - 파일변환
  - LLM도구
  - PDF변환
  - 문서변환
  - MCP
  - Python
related:
  - "[[학습 자료 모음]]"
---
## 개요

**MarkItDown**은 LLM 및 관련 텍스트 분석 파이프라인에서 사용할 수 있도록 다양한 파일을 Markdown으로 변환하는 가벼운 Python 유틸리티입니다. Microsoft에서 개발한 오픈소스 프로젝트로, **82,100개 이상의 스타**를 받은 인기 있는 도구입니다.

> **저장소**: <https://github.com/microsoft/markitdown>
> **라이선스**: MIT

## 주요 특징

### 1. 광범위한 파일 형식 지원

MarkItDown은 다음과 같은 다양한 파일 형식을 Markdown으로 변환할 수 있습니다:

#### 오피스 문서

- **PDF** - 학술 논문, 보고서, 전자책
- **PowerPoint** (.pptx) - 프레젠테이션
- **Word** (.docx) - 문서
- **Excel** (.xlsx, .xls) - 스프레드시트

#### 미디어 파일

- **이미지** - EXIF 메타데이터 및 OCR
- **오디오** (.wav, .mp3) - EXIF 메타데이터 및 음성 전사

#### 웹 및 데이터

- **HTML** - 웹 페이지
- **CSV, JSON, XML** - 구조화된 데이터
- **YouTube URLs** - 동영상 전사

#### 기타

- **ZIP 파일** - 압축 파일 내용 반복 처리
- **EPub** - 전자책
- **Outlook 메시지** (.msg)

### 2. LLM 친화적 출력

- Markdown은 순수 텍스트에 가까우면서도 중요한 문서 구조 표현 가능
- 주요 LLM(예: GPT-4o)이 네이티브로 Markdown을 "말함"
- 제목, 리스트, 테이블, 링크 등 중요한 구조 보존
- 토큰 효율적인 형식

### 3. MCP(Model Context Protocol) 서버 지원

Claude Desktop과 같은 LLM 애플리케이션과의 통합을 위한 MCP 서버를 제공합니다.

> **MCP 패키지**: [markitdown-mcp](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp)

### 4. 플러그인 시스템

3rd-party 플러그인을 통한 확장 가능:

- 기본적으로 비활성화
- `--use-plugins` 플래그로 활성화
- GitHub에서 `#markitdown-plugin` 해시태그로 검색 가능

## 설치

### 기본 요구사항

- **Python 3.10 이상**
- 가상 환경 사용 권장 (의존성 충돌 방지)

### 가상 환경 생성

**표준 Python:**

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

**uv 사용:**

```bash
uv venv
source .venv/bin/activate
# uv pip install 사용 (pip install이 아님)
```

**Anaconda:**

```bash
conda create -n markitdown python=3.12
conda activate markitdown
```

### 패키지 설치

**모든 선택적 의존성 포함:**

```bash
pip install 'markitdown[all]'
```

**소스에서 설치:**

```bash
git clone https://github.com/microsoft/markitdown.git
cd markitdown/packages/markitdown
pip install -e '.[all]'
```

### 선택적 의존성

필요한 파일 형식에 맞게 개별적으로 설치 가능:

```bash
pip install 'markitdown[pdf, docx, pptx]'
```

**사용 가능한 옵션:**

- `[all]` - 모든 선택적 의존성 설치
- `[pptx]` - PowerPoint 파일
- `[docx]` - Word 파일
- `[xlsx]` - Excel 파일
- `[xls]` - 구형 Excel 파일
- `[pdf]` - PDF 파일
- `[outlook]` - Outlook 메시지
- `[az-doc-intel]` - Azure Document Intelligence
- `[audio-transcription]` - wav/mp3 오디오 전사
- `[youtube-transcription]` - YouTube 동영상 전사

## 사용법

### 1. 커맨드 라인 인터페이스(CLI)

**기본 사용:**

```bash
markitdown path-to-file.pdf
```

**출력 파일 지정:**

```bash
markitdown path-to-file.pdf -o document.md
```

**파이프 사용:**

```bash
cat path-to-file.pdf | markitdown
```

**플러그인 사용:**

```bash
# 설치된 플러그인 목록 보기
markitdown --list-plugins

# 플러그인 활성화
markitdown --use-plugins path-to-file.pdf
```

### 2. Python API

**기본 사용:**

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("test.xlsx")
print(result.text_content)
```

**플러그인 활성화:**

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True)
result = md.convert("test.xlsx")
print(result.text_content)
```

**Azure Document Intelligence 사용:**

```python
from markitdown import MarkItDown

md = MarkItDown(
    docintel_endpoint="<Azure Document Intelligence endpoint>",
    docintel_key="<Azure Document Intelligence key>"
)
result = md.convert("test.pdf")
print(result.text_content)
```

**LLM을 사용한 이미지 설명:**

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client,
    llm_model="gpt-4o",
    llm_prompt="optional custom prompt"  # 선택적
)
result = md.convert("example.jpg")
print(result.text_content)
```

### 3. Docker 사용

```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

## 실무 활용 사례

### 1. LLM 파이프라인 전처리

**사용 시나리오:**

- PDF 논문을 Markdown으로 변환하여 LLM에 입력
- PowerPoint 프레젠테이션을 텍스트로 추출하여 요약 생성
- Excel 데이터를 구조화된 텍스트로 변환

**예시 워크플로우:**

```python
from markitdown import MarkItDown
from openai import OpenAI

# 1. PDF를 Markdown으로 변환
md = MarkItDown()
result = md.convert("research_paper.pdf")

# 2. LLM으로 요약 생성
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "당신은 학술 논문을 요약하는 전문가입니다."},
        {"role": "user", "content": f"다음 논문을 요약해주세요:\n\n{result.text_content}"}
    ]
)
print(response.choices[0].message.content)
```

### 2. RAG 시스템 데이터 준비

**사용 시나리오:**

- 다양한 형식의 문서를 통일된 Markdown 형식으로 변환
- 벡터 데이터베이스에 임베딩하기 전 전처리
- 문서 구조 보존을 통한 검색 품질 향상

**예시:**

```python
from markitdown import MarkItDown
from langchain.text_splitter import MarkdownTextSplitter

md = MarkItDown()

# 여러 파일 형식 처리
files = ["doc1.pdf", "doc2.docx", "doc3.pptx"]
markdown_docs = []

for file in files:
    result = md.convert(file)
    markdown_docs.append(result.text_content)

# Markdown 구조를 보존하며 청킹
splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.create_documents(markdown_docs)

# 벡터 데이터베이스에 저장...
```

### 3. 문서 아카이빙 및 검색

**사용 시나리오:**

- 레거시 문서를 검색 가능한 Markdown으로 변환
- OCR을 통한 이미지 기반 문서 텍스트 추출
- 통일된 형식으로 문서 관리

### 4. 콘텐츠 추출 및 분석

**사용 시나리오:**

- YouTube 동영상 전사를 통한 콘텐츠 분석
- 오디오 파일의 음성 인식 및 텍스트 변환
- 웹 페이지 스크래핑 및 구조화

## 비교: MarkItDown vs. Textract

| 특징 | MarkItDown | Textract |
|------|-----------|----------|
| **주요 목적** | LLM 친화적 Markdown 변환 | 일반 텍스트 추출 |
| **문서 구조 보존** | ✅ (제목, 리스트, 테이블 등) | ⚠️ 제한적 |
| **지원 형식** | 광범위 (오피스, 미디어, 웹) | 광범위 |
| **LLM 최적화** | ✅ | ❌ |
| **플러그인 시스템** | ✅ | ❌ |
| **MCP 지원** | ✅ | ❌ |
| **Azure 통합** | ✅ (Document Intelligence) | ❌ |

## 주요 변경사항 (v0.0.1 → v0.1.0)

### Breaking Changes

1. **선택적 의존성 구성**
   - 기존: 모든 의존성 자동 설치
   - 현재: feature-groups로 분리
   - 이전 버전 호환: `pip install 'markitdown[all]'`

2. **convert_stream() 변경**
   - 바이너리 파일 객체 필요 (binary mode)
   - 텍스트 파일 객체(io.StringIO) 더 이상 지원 안 함

3. **DocumentConverter 인터페이스 변경**
   - 파일 경로 대신 파일 스트림에서 읽기
   - 임시 파일 생성하지 않음
   - 플러그인 개발자는 코드 업데이트 필요

## Azure Document Intelligence 통합

### 설정 방법

1. Azure Portal에서 Document Intelligence 리소스 생성
2. 엔드포인트와 키 획득
3. MarkItDown에서 사용:

```python
from markitdown import MarkItDown

md = MarkItDown(
    docintel_endpoint="https://your-resource.cognitiveservices.azure.com/",
    docintel_key="your-api-key"
)

result = md.convert("complex-document.pdf")
print(result.text_content)
```

**장점:**

- 복잡한 레이아웃 처리 향상
- 다국어 지원
- 표와 양식 추출 정확도 향상

**설정 가이드**: [Azure Document Intelligence 리소스 생성](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/how-to-guides/create-document-intelligence-resource?view=doc-intel-4.0.0)

## 플러그인 개발

3rd-party 플러그인을 개발하여 MarkItDown 기능 확장 가능:

**참고 자료:**

- 샘플 플러그인: `packages/markitdown-sample-plugin`
- GitHub에서 `#markitdown-plugin` 검색

**플러그인 개발 단계:**

1. 샘플 플러그인 구조 참조
2. 커스텀 DocumentConverter 구현
3. setup.py에서 entry_points 정의
4. PyPI에 배포

## 커뮤니티 및 기여

### 프로젝트 통계

- ⭐ **82,100+ Stars**
- 👀 **281 Watchers**
- 🔀 **4,600+ Forks**
- 👥 **73 Contributors**
- 📦 **1,900+ Dependents**

### 기여 방법

1. **이슈 확인**
   - [모든 이슈](https://github.com/microsoft/markitdown/issues)
   - [기여 가능한 이슈](https://github.com/microsoft/markitdown/issues?q=is%3Aissue+is%3Aopen+label%3A%22open+for+contribution%22)

2. **PR 리뷰**
   - [모든 PR](https://github.com/microsoft/markitdown/pulls)
   - [리뷰 가능한 PR](https://github.com/microsoft/markitdown/pulls?q=is%3Apr+is%3Aopen+label%3A%22open+for+reviewing%22)

3. **테스트 및 검사 실행**

   ```bash
   cd packages/markitdown
   pip install hatch
   hatch test

   # pre-commit 체크
   pre-commit run --all-files
   ```

### CLA(Contributor License Agreement)

- 첫 PR 제출 시 CLA 동의 필요
- 자동으로 처리됨 (봇이 안내)
- Microsoft 저장소 전체에 한 번만 필요

## 관련 기술 및 프로젝트

### LLM 프레임워크 통합

- **LangChain** - 문서 로더로 활용
- **AutoGen** - 에이전트 확장으로 사용
- **OpenAI** - 이미지 설명 생성

### 관련 도구

- **Textract** - 범용 텍스트 추출 도구
- **PyPDF2** - PDF 전용 파싱
- **python-docx** - Word 문서 처리
- **Pandoc** - 범용 문서 변환기

## 라이선스 및 행동 강령

- **라이선스**: MIT
- **행동 강령**: [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)
- **보안 정책**: [SECURITY.md](https://github.com/microsoft/markitdown/blob/main/SECURITY.md)

## 관련 학습 자료

- [[bRAG-langchain - RAG 애플리케이션 구축 가이드|bRAG-langchain]] - RAG 시스템 구축
- [[학습 자료 모음]] - LangChain 및 LangGraph 학습 자료

## 릴리스 정보

- **최신 버전**: v0.1.3 (2025년 8월 26일)
- **총 릴리스**: 15개
- [전체 릴리스 노트 보기](https://github.com/microsoft/markitdown/releases)

---

**추가 정보**:

- [공식 저장소](https://github.com/microsoft/markitdown)
- [이슈 트래커](https://github.com/microsoft/markitdown/issues)
- [기여 가이드](https://github.com/microsoft/markitdown/blob/main/README.md#contributing)
