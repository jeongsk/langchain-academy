---
title: "C.R.A.F.T.E.D. 프롬프트 프레임워크: AI로 소프트웨어 엔지니어링 작업 수행하기"
author: "Steven Levey & Gregor Ojstersek"
source: https://newsletter.eng-leadership.com/p/how-to-use-ai-to-help-with-software
created: 2025-10-25
company: Revtelligent
tags:
  - 프롬프트엔지니어링
  - AI도구
  - 소프트웨어엔지니어링
  - 생산성
  - 프레임워크
  - 베스트프랙티스
related:
  - "[[학습 자료 모음]]"
  - "[[MarkItDown - 파일을 Markdown으로 변환하는 도구]]"
---

# C.R.A.F.T.E.D. 프롬프트 프레임워크: AI로 소프트웨어 엔지니어링 작업 수행하기

## 개요

다양한 도구를 활용하여 일상 업무를 더 쉽고 생산적으로 만드는 것이 훌륭한 엔지니어가 하는 일입니다. AI는 다른 도구와 마찬가지이지만, 차이점은 사용하기가 훨씬 더 모호하다는 것입니다. 일상 업무에 특화된 "완벽한 가이드"를 거의 찾을 수 없습니다.

하지만 이 문서에서는 완벽한 청사진에 최대한 가까이 다가가려고 합니다!

> **저자 소개**
> - **Steven Levey**: Revtelligent의 창립자 겸 CEO, 15년 이상의 혁신 리더십 경험
> - **Gregor Ojstersek**: Engineering Leadership 뉴스레터 운영자

## 소개: AI를 도구로 활용하기

### 핵심 원칙

AI는 생산성을 높이는 도구이지만, 효과적으로 사용하려면 체계적인 접근이 필요합니다. C.R.A.F.T.E.D. 프레임워크는 다음을 제공합니다:

- ✅ **구조화된 방법론**: 고품질 프롬프트 구성을 위한 반복 가능한 방법
- ✅ **예측 가능한 결과**: AI 모델에서 최상의 결과를 얻기 위한 논리적 워크플로우
- ✅ **실용적 청사진**: 일반적인 소프트웨어 엔지니어링 작업을 위한 코드 예제

### 이 문서의 특징

일반적인 문서보다 코드 예제가 더 많이 포함되어 있습니다. 그 이유는:

1. **즉시 사용 가능**: 특정 프롬프트 구조의 청사진 제공
2. **예상 출력 표시**: 어떤 결과를 기대할 수 있는지 명확히 보여줌
3. **실용적 학습**: 실제 사용 사례를 통한 학습

---

## C.R.A.F.T.E.D. 프레임워크란?

이 프레임워크는 페르소나, 컨텍스트, 명확한 지시사항 제공의 핵심 개념을 기반으로 하되, 개발자가 문제에 접근하는 방식을 반영하는 논리적 워크플로우로 구성합니다.

### 약어 의미

**C.R.A.F.T.E.D.**는 다음을 나타냅니다:

- **C**ontext (컨텍스트): 배경과 "무엇"을 제공
- **R**ole (역할): AI가 채택할 페르소나 정의
- **A**ction (행동): 주요하고 구체적인 작업 명시
- **F**ormat (형식): 원하는 출력 구조 지정
- **T**one (톤): 커뮤니케이션 스타일 정의
- **E**xamples (예시): 보여주기, 단순히 말하지 말기
- **D**efinition of Done (완료 정의): 규칙과 경계 설정

---

## 1. Context (컨텍스트) - "무엇"

### 목표

작업을 지시하기 전에 AI에게 필요한 모든 정보를 제공합니다. 이것이 가장 중요한 단계입니다. 버그 티켓이나 사용자 스토리를 읽은 후 코드를 작성하는 것처럼, 관련된 "도서관의 책들"을 AI에게 제공해야 합니다.

### 중요성

컨텍스트를 먼저 배치하면 모델이 "사고 과정" 전체를 상황의 세부 사항에 기반하게 됩니다. 조급한 지시에 기반한 결론으로 점프하는 것을 방지하고, 행동하기 전에 제공된 데이터를 분석하도록 강제합니다.

### 포함할 내용

1. **코드 스니펫**: 작업할 함수, 클래스, 컴포넌트
2. **오류 메시지 & 스택 트레이스**: 실패한 프로세스의 전체 출력
3. **API 문서 또는 스키마**: 데이터 또는 엔드포인트의 구조
4. **파일 차이**: 커밋 또는 풀 리퀘스트의 변경사항
5. **사용자 스토리 또는 요구사항**: 기능 또는 버그 설명
6. **관련 설정**: package.json, Dockerfile, tsconfig.json 등

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
다음 JavaScript 유틸리티 함수를 사용하고 있습니다:
```javascript
// utils.js
export function isString(value) {
  return typeof value === 'string';
}
```

다른 파일에 업데이트가 필요한 다른 함수가 있습니다:
```javascript
// dataProcessor.js
import { isString } from './utils.js';

function processData(data) {
  // ... 일부 로직
  if (typeof data.name == 'string') { // 이 줄은 규칙 위반
    console.log("Processing a string name");
  }
  // ... 더 많은 로직
}
```

우리 팀의 스타일 가이드는 명시적으로 다음과 같이 명시합니다:
"모든 런타임 타입 체킹에는 `typeof` 연산자를 직접 사용하는 대신
`utils.js`의 래퍼 유틸리티 함수를 사용해야 합니다.
이는 일관성을 보장하고 향후 로깅 및 디버깅을 더 쉽게 만듭니다."
</context>

제공된 스타일 가이드 규칙을 준수하도록 `dataProcessor.js`의
`processData` 함수를 업데이트하세요.
</prompt>
````

### AI 출력 결과

```javascript
// dataProcessor.js
import { isString } from './utils.js';

function processData(data) {
  // ... 일부 로직
  if (isString(data.name)) { // 스타일 가이드 준수로 업데이트됨
    console.log("Processing a string name");
  }
  // ... 더 많은 로직
}
```

**설명**: `typeof data.name == 'string'`을 팀의 스타일 가이드를 준수하는 `isString(data.name)`으로 교체했습니다.

---

## 2. Role (역할) - "누구"

### 목표

AI가 되어야 할 사람을 알려줍니다. 이는 모델을 특정 지식 도메인에 집중시켜 응답의 관련성과 품질을 향상시킵니다.

### 중요성

역할을 정의하면 AI가 컨텍스트를 분석해야 하는 렌즈를 제공합니다. "문제를 찾으라"는 지시는 AI의 역할이 "사이버 보안 전문가", "성능 최적화 전문가" 또는 "UI/UX 디자이너"인지에 따라 매우 다른 결과를 낳습니다.

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
다음 AWS IAM 정책 문서를 검토하세요. 이 정책은 애플리케이션을 위해
특정 S3 버킷에 대한 읽기 전용 액세스를 부여하기 위한 것입니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::my-company-reports"
    }
  ]
}
```
</context>

<role>
클라우드 인프라 전문 수석 보안 엔지니어로 행동하세요.
주요 관심사는 잠재적 취약점, 경쟁 조건, 안전하지 않은 기본값을 식별하는 것입니다.
</role>

제공된 IAM 정책의 보안 취약점을 분석하세요.
과도하게 허용적인 설정을 식별하고 잠재적 위험을 설명하세요.

Markdown으로 분석을 제공하세요.
"## 취약점 분석" 제목을 사용하고 각 문제를 설명하는 글머리 기호 목록을 사용하세요.
</prompt>
````

### AI 출력 결과

## 취약점 분석

- **과도하게 허용적인 작업**: 정책은 `s3:*`를 사용하여 모든 S3 작업을 허용합니다. 여기에는 `s3:DeleteObject`, `s3:PutBucketPolicy`, `s3:DeleteBucket`과 같은 파괴적인 작업이 포함됩니다. 읽기 전용 액세스의 경우, 이는 `s3:GetObject` 및 `s3:ListBucket`으로 제한되어야 합니다.

- **리소스 범위 누락**: 리소스 ARN이 버킷 수준(`arn:aws:s3:::my-company-reports`)만 지정하고 객체를 포함하지 않습니다. 객체 액세스를 위해서는 `arn:aws:s3:::my-company-reports/*`도 필요합니다.

- **권한 상승 위험**: 이 정책으로 엔티티는 버킷 정책을 수정하여 추가 권한을 부여하거나 버킷을 완전히 삭제할 수 있습니다.

- **데이터 유출 경로**: `s3:PutObject` 권한으로 공격자는 버킷을 악성 콘텐츠로 채워 비용을 발생시키거나 합법적인 데이터를 방해할 수 있습니다.

**권장 정책**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-company-reports",
        "arn:aws:s3:::my-company-reports/*"
      ]
    }
  ]
}
```

---

## 3. Action (행동) - "하기"

### 목표

수행하고자 하는 단일하고 가장 중요한 작업을 명시합니다. 구체적이고 명확하게. 강력하고 직접적인 동작 동사를 사용하세요.

### 중요성

명확하고 직접적인 동작 동사는 주요 목표에 대한 모든 모호성을 제거합니다. 컨텍스트와 역할로 준비된 후, AI는 구체적인 명령을 받을 준비가 되었습니다. 모호한 요청은 일반적인 답변으로 이어지고, 정확한 행동은 정확한 결과로 이어집니다.

### 예제

"제공된 Python 함수에 대한 pytest 프레임워크를 사용하여 세 가지 엣지 케이스 단위 테스트를 생성하세요."

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
다음은 숫자 리스트의 제곱 합을 계산하는 Python 함수입니다.

```python
def sum_of_squares(numbers):
    return sum(x*x for x in numbers)
```
</context>

<role>
Python을 사용한 테스트 주도 개발 전문 소프트웨어 엔지니어입니다.
</role>

<action>
`pytest` 프레임워크를 사용하여 제공된 Python 함수에 대한
세 가지 개별 단위 테스트를 생성하세요.
각 테스트는 다른 엣지 케이스를 다루어야 합니다:
빈 리스트, 음수가 있는 리스트, 0을 포함하는 리스트.
</action>

단일 코드 블록에 테스트를 위한 Python 코드만 반환하세요.
설명을 포함하지 마세요.
</prompt>
````

### AI 출력 결과

```python
import pytest
from solution import sum_of_squares

def test_empty_list():
    assert sum_of_squares([]) == 0

def test_negative_numbers():
    assert sum_of_squares([-1, -2, -3]) == 14

def test_list_with_zero():
    assert sum_of_squares([0, 1, 2]) == 5
```

---

## 4. Format (형식) - "어떻게"

### 목표

출력의 정확한 구조를 지정합니다. AI가 원하는 형식을 추측할 것이라고 가정하지 마세요. 여기서 명시적으로 지정하면 재롤링이나 편집에 상당한 시간을 절약할 수 있습니다.

### 중요성

형식을 지정하면 출력을 즉시 사용할 수 있게 만듭니다. 명시적인 지시 없이는 대화형 텍스트에 묻힌 완벽한 코드 스니펫을 얻을 수 있습니다. 출력 구조를 정의함으로써("코드만 반환", "JSON 객체 사용") 즉시 복사, 붙여넣기 및 프로그래밍 방식으로 사용할 수 있는 응답을 얻습니다.

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
다음 Python 함수를 분석하세요:

```python
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```
</context>

<role>
당신은 자동화된 코드 분석 도구입니다.
</role>

<action>
함수를 분석하고 이름, 매개변수 목록, 반환 타입을 제공하세요.
</action>

<format>
분석을 단일 축소된 JSON 객체로 반환하세요.
객체는 세 개의 키를 가져야 합니다:
'functionName' (문자열), 'parameters' (문자열 배열),
'returnType' (문자열, 예: 'number', 'string', 'any').
다른 텍스트나 설명을 포함하지 마세요.
</format>
</prompt>
````

### AI 출력 결과

```json
{"functionName":"calculate_average","parameters":["numbers"],"returnType":"number"}
```

---

## 5. Tone (톤) - "목소리"

### 목표

커뮤니케이션 스타일을 지정합니다. 이는 문서, 코드 주석 또는 다른 청중을 위한 설명을 생성하는 작업에 중요합니다.

### 중요성

톤은 의도된 청중을 위해 출력을 형성합니다. 코드 주석은 간결하고 기술적이어야 합니다. 비기술 이해관계자를 위한 설명은 간단하고 고수준이어야 합니다. 주니어 개발자를 위한 튜토리얼은 격려적이어야 합니다. 톤을 정의하면 코드만큼 효과적인 커뮤니케이션을 보장합니다.

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
주니어 개발자가 이 Python 코드 줄에 혼란스러워합니다:
`results = [process(item) for item in data if item is not None]`
</context>

<role>
주니어 개발자와 페어 프로그래밍을 하는 인내심 있고
지식이 풍부한 시니어 개발자입니다.
</role>

<action>
이 코드 줄이 무엇을 하는지 설명하세요.
</action>

<tone>
친근하고, 격려적이며, 약간 소크라테스식 톤을 채택하세요.
답을 직접 제공하기 전에 질문을 통해 사용자를 답으로 안내하세요.
답을 바로 주지 마세요.
</tone>
</prompt>
````

### AI 출력 결과

좋은 질문이네요! 이 줄을 함께 분석해봅시다.

먼저, 대괄호 `[]`를 보면 무엇이 만들어지고 있는지 알 수 있나요?

맞아요, 리스트입니다!

이제 `for item in data` 부분을 보세요. 이것은 무엇을 하고 있나요?

정확해요 - `data`를 반복하고 있습니다.

그런데 `if item is not None` 부분은 어떤가요? 이것이 어떤 항목을 포함할지 어떻게 영향을 미칠까요?

완벽합니다! 그래서 종합하면, 이 줄은 `data`의 각 항목을 반복하면서, `None`이 아닌 항목만 유지하고, 각각에 대해 `process()`를 호출한 다음, 그 결과를 새 리스트에 수집합니다.

이것을 **리스트 컴프리헨션(list comprehension)**이라고 합니다 - 기존 이터러블에서 새 리스트를 만드는 간결한 방법이죠. 이해가 되나요?

---

## 6. Examples (예시) - "보여주기"

### 목표

원하는 입력/출력 패턴을 명확하게 보여줍니다. "퓨샷 프롬프팅(few-shot prompting)"으로 알려진 이 기법은 정확하고 맞춤형 형식의 결과를 얻는 가장 효과적인 방법입니다.

### 중요성

예시는 명확성의 궁극적인 형태입니다. 특히 복잡하거나 맞춤형 형식의 경우, 요청에서 모든 모호성을 제거합니다. 청사진을 설명하는 것과 AI에게 청사진을 보여주는 것의 차이입니다. 비표준 작업의 경우, 이것이 올바른 응답을 보장하는 가장 강력한 도구입니다.

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
"로그인 버튼을 수정했고 인증 모듈도 리팩토링했습니다."
</context>

<role>
당신은 Conventional Commit 메시지 작성 전문가입니다.
</role>

<action>
코드 변경에 대한 간단한 자연어 설명을
구조화된 Conventional Commit 메시지로 변환해야 합니다.
</action>

<examples>
다음은 필요한 변환의 예입니다:
입력: "사용자 프로필을 위한 새 기능 추가"
출력: "feat: Implement user profile feature"
</examples>

최종 커밋 메시지만 단일 문자열로 반환하세요.
"Output:"이나 다른 레이블을 포함하지 마세요.
</prompt>
````

### AI 출력 결과

```
fix: Repair login button and refactor auth module
```

---

## 7. Definition of Done (완료 정의) - "규칙"

### 목표

최종 제약 조건, 경계 및 성공 기준을 설정합니다. 여기서 AI가 하지 말아야 할 것과 다른 중요한 요구사항을 명시합니다.

### 중요성

규칙을 마지막에 배치하면 "최신 효과(recency effect)"로 알려진 현상을 활용합니다 - 모델은 마지막에 받은 지시사항에 매우 주의를 기울이는 경향이 있습니다. 이러한 최종 제약 조건은 출력에 대한 엄격한 필터 역할을 하여, AI가 응답을 생성할 때 가장 중요한 경계("외부 라이브러리를 사용하지 마세요"와 같은)를 준수하도록 합니다.

### 실무 예제: C.R.A.F.T.E.D 사용

````xml
<prompt>
<context>
Python에서 단일 리스트로 평탄화해야 하는 중첩 리스트가 있습니다.

```python
nested_list = [[1, 2, 3], [4, 5], [6]]
```
</context>

<role>
당신은 도움이 되는 Python 프로그래밍 보조자입니다.
</role>

<action>
중첩 리스트를 받아 단일 평탄화된 리스트를 반환하는
`flatten_list`라는 Python 함수를 작성하세요.
</action>

<format>
코드 블록에 완전한 Python 함수만 반환하세요.
설명이나 주변 텍스트를 제공하지 마세요.
</format>

<definition_of_done>
제약조건: numpy나 itertools 같은 외부 라이브러리를 사용하지 마세요.
솔루션은 표준 Python 언어 기능만 사용하여 구현되어야 합니다.
</definition_of_done>
</prompt>
````

### AI 출력 결과

```python
def flatten_list(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result
```

**참고**: definition_of_done 없이 위를 시도하면, 다른 모델들이 내장 라이브러리 대신 3rd party 라이브러리를 사용하는 것을 볼 수 있습니다.

---

## 종합 예제: 완전한 C.R.A.F.T.E.D. 프롬프트

### 시나리오

느린 Python 함수가 있고 최적화하고 코드 리뷰를 위한 설명을 받아야 합니다.

### 완전한 C.R.A.F.T.E.D. 프롬프트

````xml
<prompt>
<context>
다음 Ruby 메서드는 큰 배열에 대해 비효율적입니다:

```ruby
def find_common_elements(list1, list2)
  common = []
  list1.each do |item1|
    list2.each do |item2|
      if item1 == item2
        common << item1
      end
    end
  end
  common
end
```
</context>

<role>
깨끗하고 효율적이며 관용적인 코드 작성 전문가인
시니어 Ruby 개발자로 행동하세요.
</role>

<action>
특히 큰 입력 배열에 대해 더 성능이 좋도록
위의 메서드를 리팩토링하세요.
</action>

<format>
응답을 Markdown 파일로 반환하세요.
먼저 코드 블록에 최적화된 Ruby 코드를 포함하세요.
코드 다음에 "## Explanation"이라는 제목의 섹션을 추가하고
변경 사항과 성능이 향상되는 이유를 자세히 설명하는
글머리 기호 목록을 포함하세요.
</format>

<tone>
설명의 톤은 명확하고 전문적이어야 하며,
풀 리퀘스트 설명에 적합해야 합니다.
</tone>

<definition_of_done>
- 외부 gem을 사용하지 마세요.
- 메서드 시그니처(이름 및 인수)는 동일하게 유지되어야 합니다.
- 솔루션은 오류를 발생시키지 않고 빈 배열을 입력으로 처리해야 합니다.
</definition_of_done>
</prompt>
````

**참고**: 위에는 의도적으로 `<examples>` 섹션이 없습니다! (마지막 생각 참조)

### AI 출력 결과

```markdown
# 최적화된 find_common_elements 메서드

```ruby
def find_common_elements(list1, list2)
  return [] if list1.empty? || list2.empty?

  list2_set = list2.to_set
  list1.select { |item| list2_set.include?(item) }
end
```

## Explanation

- **list2를 Set으로 변환**: 원래 중첩 루프 접근 방식은 O(n×m) 시간 복잡도를 가집니다. `list2`를 Set으로 변환하면 조회가 O(m) 대신 O(1) 평균 케이스가 되어 전체 복잡도가 O(n+m)으로 감소합니다.

- **include?와 함께 select 사용**: 명시적 루프와 배열 빌딩을 Ruby의 관용적인 `select` 메서드와 Set의 `include?` 메서드로 교체하여 코드를 더 읽기 쉽게 만들고 최적화된 네이티브 구현을 활용합니다.

- **빈 배열에 대한 조기 반환 추가**: 입력 중 하나가 비어 있으면 즉시 빈 배열을 반환하여 불필요한 처리를 피하고 엣지 케이스를 우아하게 처리합니다.

- **중복 결과 제거**: 원래 구현은 `list1`에 여러 번 나타나는 경우 동일한 요소를 여러 번 추가했을 것입니다. 새로운 접근 방식은 모든 요소를 반복하는 대신 멤버십을 확인하여 이를 자연스럽게 처리합니다.

- **메모리 할당 감소**: `<<`로 배열에 반복적으로 추가하는 대신, 단일 작업으로 결과 배열을 생성하는 `select`를 사용하여 가비지 컬렉션 오버헤드를 줄입니다.

리팩토링된 메서드는 동일한 인터페이스를 유지하면서 상당한 성능 향상을 제공하며, O(n×m)과 O(n+m) 복잡도의 차이가 상당해지는 큰 입력 배열에서 특히 눈에 띕니다.
```

---

## 실무 적용 가이드

### 언제 전체 프레임워크를 사용할까?

위의 거의 모든 예제는 간단하며 프레임워크 뒤의 아이디어를 강화하기 위한 것입니다.

**일상적인 AI 사용에서**:
- 진정으로 일회성이고 기본적인 질문이나 리팩토링이 있다면 전체 C.R.A.F.T.E.D. 프레임워크가 필요하지 않습니다
- 재량껏 사용하세요
- 때로는 예시, 톤 또는 형식을 추가할 필요가 없습니다

**프레임워크를 사용해야 할 때**:
- 결과가 좋지 않을 때
- 코드베이스가 복잡성이 커질 때
- `<context>` 섹션이 커지기 시작할 때
- 원하는 결과를 얻을 때까지 섹션을 레이어링하세요

### 핵심 인사이트

**모든 것은 컨텍스트입니다**:
- 각 섹션은 구조를 위해 XML 태그로 감싸져 있지만, 모델에 제공되는 컨텍스트일 뿐입니다
- 수동으로 컨텍스트를 구축하거나
- 프로그래밍 방식으로 컨텍스트를 구축할 수 있습니다 (도구, MCP, 웹훅, 데이터 파이프라인 등)

---

## 실제 사용 사례

### 1. 코드 리뷰 자동화

```xml
<prompt>
<context>
[풀 리퀘스트 diff]
</context>
<role>시니어 소프트웨어 엔지니어</role>
<action>보안 취약점, 성능 문제, 모범 사례 위반을 검토하세요</action>
<format>Markdown 체크리스트</format>
<tone>건설적이고 교육적</tone>
</prompt>
```

### 2. 단위 테스트 생성

```xml
<prompt>
<context>[함수 코드]</context>
<role>TDD 전문가</role>
<action>엣지 케이스를 다루는 포괄적인 테스트 생성</action>
<format>코드만 (설명 없음)</format>
<examples>[샘플 테스트 패턴]</examples>
<definition_of_done>100% 코드 커버리지, 외부 모킹 없음</definition_of_done>
</prompt>
```

### 3. API 문서 작성

```xml
<prompt>
<context>[API 엔드포인트 코드]</context>
<role>기술 문서 작성자</role>
<action>OpenAPI 3.0 사양 생성</action>
<format>YAML</format>
<tone>명확하고 간결</tone>
<definition_of_done>모든 응답 코드 포함, 예제 포함</definition_of_done>
</prompt>
```

### 4. 성능 최적화

```xml
<prompt>
<context>[느린 함수 + 프로파일링 데이터]</context>
<role>성능 최적화 전문가</role>
<action>병목 현상 식별 및 최적화된 버전 제공</action>
<format>원래 코드, 최적화된 코드, 벤치마크</format>
<tone>기술적, 데이터 기반</tone>
<definition_of_done>Big-O 복잡도 개선, 알고리즘 변경 없음</definition_of_done>
</prompt>
```

### 5. 레거시 코드 리팩토링

```xml
<prompt>
<context>[레거시 코드]</context>
<role>현대적 패턴의 시니어 개발자</role>
<action>코드를 현재 모범 사례로 현대화</action>
<format>Before/After 비교</format>
<tone>설명적</tone>
<examples>[원하는 패턴]</examples>
<definition_of_done>기능 동등성 유지, 테스트 통과</definition_of_done>
</prompt>
```

---

## 베스트 프랙티스

### Do's (해야 할 것)

✅ **컨텍스트부터 시작**: 항상 관련 정보를 먼저 제공
✅ **구체적으로**: 모호한 지시보다 정확한 동작 동사 사용
✅ **예시 제공**: 복잡한 형식의 경우 보여주기
✅ **반복**: 결과가 좋지 않으면 섹션 추가
✅ **실험**: 다른 모델과 온도 설정 시도

### Don'ts (하지 말아야 할 것)

❌ **프롬프트 과부하**: 한 번에 너무 많은 작업 요청
❌ **형식 가정**: 항상 명시적으로 지정
❌ **컨텍스트 생략**: "알아서 파악할 것"이라고 가정하지 말기
❌ **제약 무시**: Definition of Done이 중요함
❌ **예제 없이 복잡한 작업**: 쇼 앤 텔

---

## 고급 기법

### 1. 체이닝 프롬프트

복잡한 작업을 더 작은 C.R.A.F.T.E.D. 프롬프트로 분해:

```
프롬프트 1: 코드 분석 → 문제 식별
프롬프트 2: 각 문제에 대한 솔루션 생성
프롬프트 3: 솔루션 통합 및 테스트
```

### 2. 템플릿 시스템

일반적인 작업을 위한 재사용 가능한 템플릿 생성:

```xml
<!-- code-review-template.xml -->
<prompt>
<context>{{DIFF}}</context>
<role>{{REVIEWER_ROLE}}</role>
<action>{{REVIEW_FOCUS}}</action>
<format>Markdown</format>
<tone>Professional</tone>
<definition_of_done>{{STANDARDS}}</definition_of_done>
</prompt>
```

### 3. 반복적 개선

첫 번째 결과를 사용하여 더 나은 프롬프트 만들기:

```
1단계: 기본 C.R.A.F.T.E.D. 프롬프트
2단계: 결과 검토
3단계: 예시나 제약 추가
4단계: 재실행
```

---

## 측정 및 개선

### 성공 지표

- ⏱️ **시간 절약**: 작업 완료 시간 추적
- 🎯 **정확도**: 첫 시도 성공률
- 🔄 **반복 감소**: 재작업이 필요한 횟수
- 💡 **품질**: 출력이 기준을 충족하는 정도

### 지속적인 개선

1. **프롬프트 라이브러리 유지**: 효과적인 프롬프트 저장
2. **팀과 공유**: 모범 사례 문서화
3. **정기 검토**: 프롬프트 전략 업데이트
4. **피드백 수집**: 무엇이 작동하고 무엇이 작동하지 않는지

---

## 결론

C.R.A.F.T.E.D. 프레임워크는 단순한 프롬프트 템플릿이 아닙니다. AI와 효과적으로 협업하는 방법에 대한 사고 방식입니다.

### 핵심 요점

1. **컨텍스트가 왕**: 충분한 배경 없이는 AI가 추측합니다
2. **구조가 중요**: 체계적인 접근 방식이 일관된 결과를 낳습니다
3. **예시가 가장 강력**: 말하는 것보다 보여주는 것
4. **제약이 품질을 정의**: 경계가 우수성을 만듭니다

### 시작하기

1. 간단한 작업으로 시작
2. 한 번에 하나씩 섹션 추가
3. 효과적인 것 문서화
4. 반복하고 개선

### 최종 생각

거의 모든 예제는 간단한 연습용입니다. 진정으로 일회성이고 기본적인 질문이 있다면, 전체 C.R.A.F.T.E.D. 프레임워크를 구현할 필요가 없습니다. 재량껏 사용하세요.

**하지만 결과가 좋지 않을 때**, 이것으로 돌아와서 원하는 결과를 얻을 때까지 섹션을 레이어링하세요.

**코드베이스가 복잡성이 커지고 `<context>` 섹션이 커지기 시작할 때 이것이 훨씬 더 중요하고 유용해집니다.**

> 💡 **기억하세요**: 결국, 모든 것은 컨텍스트입니다. 각 섹션은 구조를 위해 XML 태그로 감싸져 있지만, 모델에 제공되는 컨텍스트일 뿐입니다. 수동으로 컨텍스트를 구축하거나, 프로그래밍 방식으로 컨텍스트를 구축할 수 있습니다 (도구, MCP, 웹훅, 데이터 파이프라인 등).

---

## 저자 소개

### Steven Levey

- **직책**: Revtelligent 창립자 겸 CEO
- **경험**: 15년 이상의 혁신 리더십
- **전문 분야**: AI 이론을 실제 영향으로 전환
- **LinkedIn**: [Steven Levey](https://www.linkedin.com/in/stevenmlevey/)
- **웹사이트**: [Revtelligent](https://www.revtelligent.com/)

**Steven은 엔지니어링 리더들이 AI 이론에서 실제 영향으로 이동하도록 조언하고 코칭합니다.** 5번의 창업자이자 엔지니어로서, AI 플랫폼을 구축하고 스타트업과 공개 기업에서 GTM 및 RevOps 팀을 이끌었습니다.

### Gregor Ojstersek

- **직책**: Engineering Leadership 뉴스레터 운영자
- **구독자**: 75,000+ 명
- **LinkedIn**: [Gregor Ojstersek](https://www.linkedin.com/in/gregorojstersek/)

---

## 관련 리소스

- [[학습 자료 모음|LangChain 학습 자료]]
- [[DeepAgents - LangChain으로 고급 주식 조사 에이전트 구축하기|DeepAgents 실습]]
- [[Agents 2.0 - Shallow 에이전트에서 Deep 에이전트로|에이전트 아키텍처]]

---

**마지막 업데이트**: 2025-10-25
