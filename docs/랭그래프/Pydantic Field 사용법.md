---
created: 2025-10-18 17:56:55
updated: 2025-10-19 11:14:35
tags:
  - Pydantic
  - Field
  - Python
  - 데이터_모델링
  - 타입_힌팅
---
Pydantic의 `Field` 사용법에 대한 차이점을 자세히 설명합니다. 이 내용은 [[docs/랭그래프/LangGraph|LangGraph]]의 상태(State)를 정의할 때 유용하게 사용됩니다.

## 1. `Field(description="설명")`

이것은 **필수 필드**를 만듭니다. 기본값이 없기 때문에 객체를 생성할 때 반드시 값을 제공해야 합니다.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(description="사용자 이름")
    age: int = Field(description="나이")

# 반드시 name과 age를 제공해야 함
user = User(name="홍길동", age=30)  # 정상 작동
# user = User(name="홍길동")  # 에러 발생 (age 누락)
```

## 2. `Field(None, description="설명")`

이것은 **선택적 필드**를 만들며, 기본값이 `None`입니다. 값을 제공하지 않으면 자동으로 `None`이 할당됩니다.

```python
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    name: str = Field(description="사용자 이름")
    nickname: Optional[str] = Field(None, description="별명")  # None이 기본값
    age: Optional[int] = Field(None, description="나이")

# nickname과 age는 생략 가능
user1 = User(name="홍길동")  # 정상 (nickname=None, age=None)
user2 = User(name="홍길동", nickname="길동이", age=30)  # 정상
```

## 3. `Field(..., description="설명")`

이것도 **필수 필드**를 만듭니다. `...` (Ellipsis)는 "이 필드는 필수이며 기본값이 없다"는 것을 명시적으로 표현합니다.

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(..., description="사용자 이름")  # 명시적으로 필수
    age: int = Field(..., description="나이")

# 반드시 name과 age를 제공해야 함
user = User(name="홍길동", age=30)  # 정상 작동
# user = User(name="홍길동")  # 에러 발생 (age 누락)
```

## 비교 정리

| 사용법 | 필수/선택 | 기본값 | 언제 사용? |
|--------|-----------|--------|------------|
| `Field(description="...")` | 필수 | 없음 | 필수 필드, 간단하게 작성 |
| `Field(None, description="...")` | 선택 | `None` | 선택적 필드, 값이 없어도 됨 |
| `Field(..., description="...")` | 필수 | 없음 | 필수 필드, 의도를 명확히 표현 |

## 실전 예시

```python
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    # 필수 필드 - 반드시 있어야 함
    id: int = Field(..., description="상품 ID")
    name: str = Field(description="상품명")  # 위와 동일

    # 선택 필드 - 없어도 됨
    description: Optional[str] = Field(None, description="상품 설명")
    discount: Optional[float] = Field(None, description="할인율")

# 사용 예시
product1 = Product(id=1, name="노트북")  # OK
product2 = Product(
    id=2,
    name="마우스",
    description="무선 마우스",
    discount=0.1
)  # OK
```

## 핵심 포인트

`Field(description="...")`와 `Field(..., description="...")`는 기능상 동일하지만, `...`를 사용하면 "이건 필수야!"라는 의도를 더 명확하게 표현할 수 있습니다!
