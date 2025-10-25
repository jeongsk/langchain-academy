---
title: "DeepAgents: LangChain으로 Claude 수준의 주식 조사 에이전트 구축하기"
author: Sagar
source: https://medium.com/@sagarnreddy/i-built-a-research-agent-like-claudes-analysis-tools-using-langchain-deepagents-795f51a3a63f
repository: https://github.com/sagar-n/deepagents
created: 2025-10-25 00:00:00
stars: 424
tags: [금융분석, 서브에이전트, 주식분석, AI에이전트, DeepAgents, Gradio, LangChain]
related:
  - "[[최신 AI 연구 논문 모음]]"
  - "[[Agents 2.0 - Shallow 에이전트에서 Deep 에이전트로]]"
updated: 2025-10-25 11:22:02
---
> 원문: https://medium.com/@sagarnreddy/i-built-a-research-agent-like-claudes-analysis-tools-using-langchain-deepagents-795f51a3a63f
# DeepAgents: LangChain으로 Claude 수준의 주식 조사 에이전트 구축하기

## 개요

Claude의 고급 분석 기능이 어떻게 작동하는지 궁금해본 적이 있나요? LangChain의 DeepAgent 프레임워크를 사용하여 전문가급 분석 도구에 필적하는 지능형 주식 조사 에이전트를 구축한 방법을 소개합니다.

> **저자**: Sagar (소프트웨어 개발자, AI 및 에이전트 탐구자)
> **GitHub**: <https://github.com/sagar-n/deepagents>
> **Medium**: <https://medium.com/@sagarnreddy>

## 기본 AI 에이전트의 문제점

대부분의 AI 챗봇은 대화에는 뛰어나지만 복잡한 다단계 연구 작업에서는 어려움을 겪습니다. 다음과 같은 능력이 부족합니다:

- **체계적인 계획 수립**: 큰 작업을 작은 단계로 분해
- **전문화된 분석**: 각 측면에 적합한 전문 지식 적용
- **데이터 관리**: 중간 결과의 구조화된 저장
- **종합적 추론**: 여러 데이터 포인트를 일관된 인사이트로 결합

이것이 **DeepAgents**가 빛을 발하는 부분입니다. 단순한 도구 호출 에이전트와 달리, DeepAgents는 계획, 특화된 서브 에이전트, 파일 관리, 종합적 추론을 통합합니다 - 마치 Claude의 연구 기능처럼 말입니다.

## 구축한 것: 완전한 주식 조사 시스템

이 에이전트는 다음을 결합하여 종합적인 주식 분석을 수행합니다:

- ✅ **실시간 금융 데이터** - 가격, 비율, 시가총액
- ✅ **기술적 지표** - RSI, 이동평균, 추세 신호
- ✅ **재무제표 분석** - 수익, 부채, 수익성
- ✅ **다각적 분석** - 특화된 서브 에이전트를 통한 분석
- ✅ **전문가급 보고서** - 명확한 투자 권고사항

## 아키텍처: 3계층 지능 시스템

### 시스템 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    사용자 인터페이스 (Gradio)               │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              마스터 DeepAgent 오케스트레이터                │
├─────────────────────────────────────────────────────────────┤
│  계획 도구 | 가상 파일 시스템 | 시스템 프롬프트            │
└─────────────┬───────────────────────────────────┬─────────┘
              │                                   │
    ┌─────────▼──────────┐                ┌──────▼──────────┐
    │   서브 에이전트    │                │  금융 도구      │
    │                    │                │                  │
    │ • 펀더멘털 분석    │                │ • 주가 조회      │
    │ • 기술적 분석      │                │ • 재무제표       │
    │ • 리스크 분석      │                │ • 기술적 지표    │
    └────────────────────┘                └──────┬──────────┘
                                                 │
                                     ┌──────────▼──────────┐
                                     │   데이터 소스       │
                                     │                     │
                                     │ • Yahoo Finance     │
                                     │ • 실시간 API        │
                                     │ • 시장 데이터       │
                                     └─────────────────────┘
```

### 계층 1: 커스텀 금융 도구

먼저 금융 데이터를 수집하고 처리하는 특화된 도구를 구축했습니다:

#### 1. 주가 조회 도구

```python
@tool
def get_stock_price(symbol: str) -> str:
    """주식의 현재 가격과 핵심 지표 조회"""
    stock = yf.Ticker(symbol)
    info = stock.info

    return f"""
    현재가: ${info.get('currentPrice', 'N/A')}
    시가총액: ${info.get('marketCap', 'N/A')}
    P/E 비율: {info.get('trailingPE', 'N/A')}
    52주 최고가: ${info.get('fiftyTwoWeekHigh', 'N/A')}
    52주 최저가: ${info.get('fiftyTwoWeekLow', 'N/A')}
    """
```

#### 2. 재무제표 도구

```python
@tool
def get_financial_statements(symbol: str) -> str:
    """손익계산서, 대차대조표, 현금흐름표 조회"""
    stock = yf.Ticker(symbol)

    # 최근 재무 데이터 추출
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow

    return financial_summary
```

#### 3. 기술적 지표 도구

```python
@tool
def get_technical_indicators(symbol: str) -> str:
    """RSI, 이동평균, 거래량 분석"""
    data = yf.download(symbol, period="6mo")

    # RSI 계산
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # 이동평균
    sma_20 = data['Close'].rolling(window=20).mean()
    sma_50 = data['Close'].rolling(window=50).mean()

    return indicators_summary
```

### 계층 2: 특화된 서브 에이전트

마법은 특화된 서브 에이전트에서 일어납니다. 각 에이전트는 자신의 도메인의 전문가입니다:

#### 펀더멘털 분석가

```python
fundamental_analyst = {
    "name": "fundamental-analyst",
    "description": "재무제표와 밸류에이션을 전문으로 하는 금융 분석가",
    "prompt": """
    당신은 기업 펀더멘털 전문 금융 분석가입니다.

    분석 시 집중할 사항:
    - 수익 성장 추세
    - 수익성 지표 (순이익률, ROE)
    - 부채 수준과 재무 건전성
    - 동종 업계 대비 밸류에이션

    데이터 기반의 명확하고 실행 가능한 인사이트를 제공하세요.
    """
}
```

#### 기술적 분석가

```python
technical_analyst = {
    "name": "technical-analyst",
    "description": "차트 패턴과 거래 신호 전문가",
    "prompt": """
    당신은 기술적 분석 전문가입니다.

    평가 항목:
    - 추세 방향 (강세/약세/횡보)
    - 지지선과 저항선
    - 모멘텀 지표 (RSI, MACD)
    - 거래량 패턴

    명확한 진입/청산 시그널을 제공하세요.
    """
}
```

#### 리스크 분석가

```python
risk_analyst = {
    "name": "risk-analyst",
    "description": "투자 리스크 평가 전문가",
    "prompt": """
    당신은 리스크 평가 전문가입니다.

    평가할 리스크:
    - 시장 변동성
    - 기업별 리스크 (경영진, 경쟁, 규제)
    - 거시경제 요인
    - 산업별 도전과제

    포트폴리오 리스크 관리 권장사항을 제공하세요.
    """
}
```

### 계층 3: 마스터 오케스트레이터

메인 에이전트는 체계적인 계획으로 모든 것을 조정합니다:

```python
from langchain_experimental.deepagents import DeepAgent

# DeepAgent 생성
agent = DeepAgent(
    llm=ollama_model,
    tools=tools,
    subagents=subagents,
    system_prompt="""
    당신은 포괄적인 주식 조사를 수행하는 전문 금융 분석 AI입니다.

    작업 수행 시:
    1. 먼저 조사를 논리적 단계로 나누는 명확한 계획을 수립하세요
    2. 각 전문 영역에 적합한 서브 에이전트를 활용하세요
    3. 모든 발견사항을 일관된 투자 논문으로 종합하세요
    4. 명확한 권고사항과 목표 가격을 제공하세요

    체계적이고 데이터 기반으로, 모든 주장을 실제 수치로 뒷받침하세요.
    """
)
```

## 사용자 경험: 간단한 질문, 전문가급 분석

모든 것을 깔끔한 Gradio 인터페이스로 감쌌습니다:

```python
import gradio as gr

def analyze_stock(query):
    """주식 분석 쿼리 처리"""
    result = agent.invoke({"input": query})
    return result["output"]

# Gradio UI 생성
interface = gr.Interface(
    fn=analyze_stock,
    inputs=gr.Textbox(
        label="분석 요청",
        placeholder="예: 6개월 투자를 위한 Apple Inc. (AAPL) 분석"
    ),
    outputs=gr.Textbox(label="분석 결과"),
    title="📊 DeepAgent 주식 조사 보조",
    description="LangChain DeepAgents를 활용한 전문가급 주식 분석"
)

interface.launch()
```

## 작동 방식: 무대 뒤의 마법

사용자가 "6개월 투자를 위한 Apple Inc. (AAPL) 분석"이라고 요청하면:

### 단계별 프로세스

1. **계획 수립**
   ```
   오케스트레이터: "이 분석을 3단계로 분해하겠습니다:
   1. 펀더멘털 분석가를 통한 재무 데이터 수집
   2. 기술적 분석가를 통한 차트 패턴 분석
   3. 리스크 분석가를 통한 리스크 평가"
   ```

2. **펀더멘털 분석 (서브 에이전트 1)**
   ```
   도구 호출: get_stock_price("AAPL")
   도구 호출: get_financial_statements("AAPL")

   분석: "애플의 수익은 전년 대비 1.3% 증가...
         P/E 비율 28.5배는 프리미엄이지만 강한 펀더멘털로 정당화됨..."
   ```

3. **기술적 분석 (서브 에이전트 2)**
   ```
   도구 호출: get_technical_indicators("AAPL")

   분석: "강세 추세 확인됨. RSI 62.3으로 과매수 아님.
         지지선 $175, 저항선 $195..."
   ```

4. **리스크 평가 (서브 에이전트 3)**
   ```
   분석: "주요 리스크:
         - 기술주 변동성 (보통)
         - 반독점 규제 우려 (보통)
         - 강한 대차대조표로 기업 리스크 낮음"
   ```

5. **최종 종합**
   ```
   권고사항: 매수
   목표가: $210 (12개월)
   리스크 수준: 보통

   근거: 강한 펀더멘털, 긍정적 기술적 모멘텀,
         관리 가능한 리스크 프로필...
   ```

## 이 접근 방식이 효과적인 이유

### 전통적 에이전트 vs. DeepAgent

**전통적 에이전트:**
```
단일 AI → 간단한 도구 호출 → 기본적인 응답
```

**DeepAgent:**
```
계획 수립 → 특화된 전문가들 → 데이터 종합 → 전문가급 분석
```

차이점은 한 명의 제너럴리스트에게 자문을 구하는 것과 전문가 팀을 구성하는 것의 차이와 같습니다.

## 시작하기: 5분 설정

### 1. 저장소 클론

```bash
git clone https://github.com/sagar-n/deepagents.git
cd deepagents
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
deepagents
langchain-ollama
langchain-core
yfinance
gradio
pandas
numpy
```

### 3. Ollama 설정

```bash
# Ollama 설치 (미설치 시)
curl -fsSL https://ollama.ai/install.sh | sh

# 모델 다운로드
ollama pull gpt-oss
```

### 4. 애플리케이션 실행

```bash
python research_agent.py
```

### 5. 브라우저에서 열기

```
http://localhost:7860
```

즉시 주식 분석을 시작할 수 있습니다!

## 고급 사용법

### 포트폴리오 분석

```python
query = """
포트폴리오 배분을 위해 AAPL, MSFT, GOOGL을 비교 분석하세요.
각 주식의:
- 성장 잠재력
- 리스크 프로필
- 밸류에이션 매력도
- 권장 배분 비율
"""
```

### 섹터 연구

```python
query = """
2025년 1분기 기술 섹터 전망을 분석하세요.
다음을 포함:
- 주요 성장 동인
- 업계 트렌드
- 규제 리스크
- 투자할 톱 3 기업
"""
```

### 리스크 평가

```python
query = """
Tesla (TSLA) 투자 리스크를 평가하세요.
특히 다음에 초점:
- 밸류에이션 리스크
- 경쟁 위협
- 규제 변화
- 실행 리스크
"""
```

## 커스터마이징

### 모델 설정

```python
from langchain_ollama import ChatOllama

ollama_model = ChatOllama(
    model="llama2",        # 또는 "codellama", "mistral"
    temperature=0,         # 창의성 vs 일관성 조절
)
```

### 커스텀 도구 추가

```python
@tool
def get_analyst_ratings(symbol: str) -> str:
    """애널리스트 등급 및 목표가 조회"""
    # 구현 코드
    return ratings_summary

# 도구 목록에 추가
tools = [
    get_stock_price,
    get_financial_statements,
    get_technical_indicators,
    get_analyst_ratings  # 커스텀 도구
]
```

### 서브 에이전트 커스터마이징

```python
# 새로운 특화 서브 에이전트 추가
esg_analyst = {
    "name": "esg-analyst",
    "description": "환경, 사회, 지배구조 요인 평가 전문가",
    "prompt": """
    당신은 ESG (환경, 사회, 지배구조) 전문가입니다.

    평가 항목:
    - 환경 영향 및 지속가능성 관행
    - 사회적 책임 및 노동 관행
    - 기업 지배구조 및 윤리
    - ESG 등급 및 인증

    장기 투자 가치에 대한 ESG 시사점을 제공하세요.
    """
}

subagents = [
    fundamental_analyst,
    technical_analyst,
    risk_analyst,
    esg_analyst  # 새 에이전트
]
```

## 예시 출력

```
=== 주식 조사 보고서 ===

APPLE INC. (AAPL) 투자 분석
생성일시: 2025-08-13 23:28:00

요약
현재가: $184.12
권고사항: 매수
목표가: $210.00 (12개월)
리스크 수준: 보통

펀더멘털 분석
• 매출 (TTM): $385.7B (+1.3% YoY)
• 순이익: $96.9B
• P/E 비율: 28.5배 (섹터 평균 24.1배 대비 프리미엄)
• ROE: 147.4% (우수)
• 부채비율: 1.73 (관리 가능)

기술적 분석
• 추세: 강세 (현재가 > 20일선 > 50일선)
• RSI: 62.3 (중립-강세)
• 지지선: $175, $165
• 저항선: $195, $205

리스크 평가
• 시장 리스크: 보통 (기술주 변동성)
• 기업 리스크: 낮음 (강한 대차대조표)
• 규제 리스크: 보통 (반독점 우려)

투자 논문
애플은 강한 펀더멘털, 견고한 재무 상태, 긍정적인 기술적
모멘텀을 보이고 있습니다. 프리미엄 밸류에이션에도 불구하고,
혁신 능력과 생태계 강점이 이를 정당화합니다...

[상세 보고서 계속...]
```

## 더 큰 그림

이 에이전트를 구축하면서 배운 것은, 진정한 AI 능력은 가장 똑똑한 모델을 갖는 것이 아니라 특화된 도구와 전문성을 체계적으로 조율하는 것이라는 점입니다.

**DeepAgents는 "스마트 챗봇"에서 복잡한 실제 워크플로우를 처리할 수 있는 "지능형 시스템"으로의 근본적인 전환을 나타냅니다.**

## 주요 통찰

### 1. 계획의 중요성

단순히 도구를 호출하는 것이 아니라, DeepAgent는 먼저 작업을 논리적 단계로 분해합니다. 이 체계적인 접근 방식이 일관되고 포괄적인 결과를 보장합니다.

### 2. 전문화의 힘

각 서브 에이전트가 자신의 도메인에 집중함으로써, 시스템은 어떤 단일 일반 에이전트보다 더 깊은 인사이트를 제공합니다.

### 3. 종합의 마법

여러 전문가의 발견사항을 결합하는 능력이 진정으로 전문가급 분석을 만들어냅니다.

### 4. 확장성

동일한 아키텍처를 다른 도메인에 적용할 수 있습니다:
- 법률 연구
- 의료 진단
- 기술 실사
- 시장 조사

## 프로젝트 통계

- ⭐ **424 Stars** (GitHub)
- 🍴 **73 Forks**
- 💻 **활발한 개발**

## 면책사항

이 도구는 교육 및 연구 목적으로만 사용됩니다. 금융 자문을 구성하지 않습니다. 투자 결정을 내리기 전에 항상 자격을 갖춘 금융 자문가와 상담하세요. 과거 성과가 미래 결과를 보장하지 않습니다.

## 감사의 말

- **LangChain Team** - DeepAgent 프레임워크 제공
- **Yahoo Finance** - 무료 금융 데이터 API 제공
- **Gradio Team** - 훌륭한 UI 프레임워크
- **Ollama** - 로컬 LLM 호스팅 기능

## 관련 자료

- [[Agents 2.0 - Shallow 에이전트에서 Deep 에이전트로|에이전트 2.0 아키텍처]]
- [[최신 AI 연구 논문 모음#초기 경험을 통한 에이전트 학습|Meta의 에이전트 학습 연구]]
- [[학습 자료 모음|LangChain 학습 자료]]

## 다음 단계

완전한 구현을 원하시나요?

- **GitHub**: <https://github.com/sagar-n/deepagents>
- **Medium**: 실용적인 AI 애플리케이션에 대한 더 많은 심층 분석

**더 많은 실용적 AI 애플리케이션을 위해 저를 팔로우하세요!**

---

**마지막 업데이트**: 2025-10-25

> 💡 **핵심 메시지**: 진정한 AI의 능력은 모델의 스마트함이 아니라, 특화된 도구와 전문성의 체계적인 조율에 있습니다.
