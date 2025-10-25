"""정답 분류가 포함된 이메일 평가 데이터셋입니다."""

# 일반적인 회신 이메일
STANDARD_EMAIL = {
    "author": "앨리스 스미스 &lt;alice.smith@company.com&gt;",
    "to": "존 도 &lt;john.doe@company.com&gt;",
    "subject": "API 문서에 대한 간단한 질문",
    "email_thread": """안녕하세요, 존님,

새로운 인증 서비스의 API 문서를 검토하던 중, 몇몇 엔드포인트가 사양에서 누락된 것을 발견했습니다. 이것이 의도된 것인지, 아니면 문서를 업데이트해야 하는지 명확히 설명해주실 수 있나요?

특히 다음 엔드포인트에 대해 문의드립니다:
- /auth/refresh
- /auth/validate

감사합니다!
앨리스 드림""",
}

# 일반적인 알림 이메일
NOTIFICATION_EMAIL = {
    "author": "시스템 관리자 &lt;sysadmin@company.com&gt;",
    "to": "개발팀 &lt;dev@company.com&gt;",
    "subject": "예정된 유지보수 - 데이터베이스 다운타임",
    "email_thread": """안녕하세요, 팀원 여러분,

오늘 밤 동부 표준시 기준 오전 2시부터 4시까지 운영 데이터베이스에 대한 정기 유지보수를 수행할 예정임을 알려드립니다. 이 시간 동안 모든 데이터베이스 서비스는 이용할 수 없습니다.

업무 계획에 참고하시고, 이 시간 동안 중요한 배포가 예정되지 않도록 확인해 주시기 바랍니다.

감사합니다,
시스템 관리팀 드림""",
}

# 데이터셋 예시
email_input_1 = {
    "author": "앨리스 스미스 &lt;alice.smith@company.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "API 문서에 대한 간단한 질문",
    "email_thread": """안녕하세요, 랜스님,

새로운 인증 서비스의 API 문서를 검토하던 중, 몇몇 엔드포인트가 사양에서 누락된 것을 발견했습니다. 이것이 의도된 것인지, 아니면 문서를 업데이트해야 하는지 명확히 설명해주실 수 있나요?

특히 다음 엔드포인트에 대해 문의드립니다:
- /auth/refresh
- /auth/validate

감사합니다!
앨리스 드림""",
}

email_input_2 = {
    "author": "마케팅팀 &lt;marketing@company.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "새로운 회사 뉴스레터가 발행되었습니다",
    "email_thread": """안녕하세요, 랜스님,

최신 회사 뉴스레터가 인트라넷에 게시되었습니다. 이번 호에는 2분기 실적, 예정된 팀 빌딩 활동, 그리고 직원 소개에 대한 기사가 실렸습니다.

시간 되실 때 확인해 보세요!

감사합니다,
마케팅팀 드림""",
}

email_input_3 = {
    "author": "시스템 관리자 &lt;sysadmin@company.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "예정된 유지보수 - 데이터베이스 다운타임",
    "email_thread": """안녕하세요, 랜스님,

오늘 밤 동부 표준시 기준 오전 2시부터 4시까지 운영 데이터베이스에 대한 정기 유지보수를 수행할 예정임을 알려드립니다. 이 시간 동안 모든 데이터베이스 서비스는 이용할 수 없습니다.

업무 계획에 참고하시고, 이 시간 동안 중요한 배포가 예정되지 않도록 확인해 주시기 바랍니다.

감사합니다,
시스템 관리팀 드림""",
}

email_input_4 = {
    "author": "프로젝트 매니저 &lt;pm@client.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "세금 신고 기간 관련 통화 일정 조율 요청",
    "email_thread": """랜스님,

다시 세금 신고 기간이 돌아왔습니다. 올해 세금 계획 전략에 대해 논의하기 위해 통화 일정을 잡고 싶습니다. 비용을 절감할 수 있는 몇 가지 제안 사항이 있습니다.

다음 주 중 언제가 편하신가요? 저는 화요일이나 목요일 오후가 가장 좋으며, 약 45분 정도 소요될 것입니다.

감사합니다,
프로젝트 매니저 드림""",
}

email_input_5 = {
    "author": "인사부 &lt;hr@company.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "알림: 경비 보고서를 제출해 주세요",
    "email_thread": """안녕하세요, 랜스님,

지난달의 모든 경비 보고서는 이번 주 금요일까지 제출해야 함을 알려드립니다. 모든 영수증과 적절한 증빙 서류를 반드시 포함해 주시기 바랍니다.

제출 과정에 대해 궁금한 점이 있으시면 언제든지 인사팀에 문의해 주세요.

감사합니다,
인사부 드림""",
}

email_input_6 = {
    "author": "컨퍼런스 주최자 &lt;events@techconf.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "이 컨퍼런스에 참석하시겠습니까?",
    "email_thread": """안녕하세요, 랜스님,

5월 15일부터 17일까지 샌프란시스코에서 열리는 TechConf 2025에 귀하를 초대합니다.

이 컨퍼런스에는 주요 기술 기업의 기조 연설자, AI 및 ML 워크숍, 그리고 훌륭한 네트워킹 기회가 마련되어 있습니다. 조기 등록은 4월 30일까지 가능합니다.

참석에 관심이 있으신가요? 다른 팀원들이 함께 참여할 경우 단체 할인도 준비해 드릴 수 있습니다.

감사합니다,
컨퍼런스 주최팀 드림""",
}

email_input_7 = {
    "author": "사라 존슨 &lt;sarah.j@partner.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "제출 전에 이 문서들을 검토해 주실 수 있나요?",
    "email_thread": """랜스님,

헨더슨 프로젝트 제안서의 최종 버전을 첨부했습니다. 금요일에 고객에게 제출하기 전에 기술 사양 부분(15-20페이지)을 검토해 주실 수 있을까요?

귀하의 전문 지식이 필요한 모든 세부 사항을 다루는 데 큰 도움이 될 것입니다.

미리 감사드립니다,
사라 드림""",
}

email_input_8 = {
    "author": "커뮤니티 수영장 &lt;info@cityrecreation.org&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "따님의 수영 강좌 등록 안내",
    "email_thread": """랜스님께,

여름 수영 강좌 등록이 시작되었습니다! 작년에 따님이 참여했던 기록을 바탕으로, 중급반이 월요일과 수요일 오후 4시 또는 화요일과 목요일 오후 5시에 개설되었음을 알려드립니다.

수업은 6월 1일에 시작하여 8주간 진행됩니다. 정원이 제한되어 있으니 조기 등록을 권장합니다.

자리를 예약하고 싶으시면 알려주세요.

감사합니다,
시민 레크리에이션부 드림""",
}

email_input_9 = {
    "author": "GitHub &lt;notifications@github.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "PR #42: alex-dev님의 댓글",
    "email_thread": """안녕하세요!

alex-dev님이 langchain-ai/project의 풀 리퀘스트 #42에 댓글을 남겼습니다:

&gt; 변경 사항을 검토했으며 모든 것이 좋아 보입니다. auth_controller.py의 오류 처리 부분에 대한 작은 제안이 하나 있습니다. 요청이 중단되는 것을 방지하기 위해 타임아웃 매개변수를 추가하는 것이 어떨까요?

댓글 보기: https://github.com/langchain-ai/project/pull/42#comment-12345

---
이 스레드를 작성하셨기 때문에 이 알림을 받으셨습니다.
이 이메일에 직접 회신하거나 GitHub에서 확인하세요.
""",
}

email_input_10 = {
    "author": "팀장 &lt;teamlead@company.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "분기별 계획 회의",
    "email_thread": """안녕하세요, 랜스님,

분기별 계획 회의 시간입니다. 다음 주에 3분기 로드맵을 논의하기 위해 90분짜리 회의를 잡고 싶습니다.

월요일이나 수요일에 가능한 시간을 알려주시겠어요? 오전 10시에서 오후 3시 사이가 이상적입니다.

새로운 기능 우선순위에 대한 귀하의 의견을 기대하겠습니다.

감사합니다,
팀장 드림""",
}

email_input_11 = {
    "author": "AWS 모니터링 &lt;no-reply@aws.amazon.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "시스템 관리자 경고: 인스턴스 CPU 사용률이 임계값을 초과했습니다",
    "email_thread": """경고: 높은 CPU 사용률

다음 EC2 인스턴스가 15분 이상 CPU 사용률 임계값인 90%를 초과했습니다:

인스턴스 ID: i-0b2d3e4f5a6b7c8d9
리전: us-west-2
현재 사용률: 95.3%

이 메시지는 자동으로 생성되었습니다. 회신하지 마십시오.
""",
}

email_input_12 = {
    "author": "고객 성공팀 &lt;success@vendor.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "구독이 자동으로 갱신됩니다",
    "email_thread": """안녕하세요, 랜스님,

귀하의 개발자 프로 플랜 연간 구독이 2025년 4월 15일에 자동으로 갱신될 예정임을 알려드립니다.

**** 4567로 끝나는 결제 수단으로 $1,499.00가 청구될 것입니다.

구독에 변경 사항이 있으시면 갱신일 전에 계정 설정을 방문하시거나 저희 지원팀에 문의해 주십시오.

지속적인 이용에 감사드립니다!

고객 성공팀 드림""",
}

email_input_13 = {
    "author": "로버츠 박사 &lt;droberts@medical.org&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "연례 건강 검진 알림",
    "email_thread": """안녕하세요, 랜스님,

연례 건강 검진을 받을 시기임을 알려드립니다. 저희 기록에 따르면 마지막 방문이 약 1년 전이었습니다.

가장 빠른 시일 내에 저희 사무실 (555) 123-4567로 전화하여 예약을 잡아주시기 바랍니다.

감사합니다,
로버츠 박사 사무실 드림""",
}

email_input_14 = {
    "author": "소셜 미디어 플랫폼 &lt;notifications@social.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "5명이 회원님의 게시물을 좋아합니다",
    "email_thread": """안녕하세요, 랜스님,

5명이 회원님의 최근 게시물 "NLP를 위한 머신러닝 기법"을 좋아했습니다.

누가 회원님의 게시물을 좋아했는지 확인하고 대화를 계속 이어가세요!

[활동 보기]

이러한 알림을 구독 취소하려면 여기에서 설정을 조정하세요.
""",
}

email_input_15 = {
    "author": "프로젝트팀 &lt;project@company.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "다음 달 공동 발표",
    "email_thread": """안녕하세요, 랜스님,

경영진이 다음 달 전사 회의에서 최근 프로젝트 성공 사례에 대한 공동 발표를 준비해달라고 요청했습니다.

제가 슬라이드 작성을 시작했는데, 기술 아키텍처 부분에 대한 귀하의 의견을 듣고 싶습니다. 다음 주 중 언젠가 약 60분 정도 시간을 내어 협업할 수 있을까요?

저는 보통 화요일과 목요일에 시간이 있습니다.

감사합니다,
프로젝트팀 드림""",
}

email_input_16 = {
    "author": "마케팅팀 &lt;marketing@openai.com&gt;",
    "to": "랜스 마틴 &lt;lance@company.com&gt;",
    "subject": "뉴스레터: OpenAI의 새로운 모델",
    "email_thread": """안녕하세요, 랜스님,

OpenAI에서 새로운 모델을 출시했다는 기쁜 소식을 전해드립니다!

이름은 "GPT-5"이며 GPT-4의 후속 모델입니다.

지금 바로 사용 가능하며, 자세한 정보는 [여기](https://openai.com/gpt-5)에서 확인하실 수 있습니다.

감사합니다,
마케팅팀 드림""",
}

# 분류 결과: "ignore"(무시), "notify"(알림), "respond"(응답)
triage_output_1 = "respond"
triage_output_2 = "ignore"
triage_output_3 = "notify"
triage_output_4 = "respond"
triage_output_5 = "notify"
triage_output_6 = "respond"
triage_output_7 = "respond"
triage_output_8 = "respond"
triage_output_9 = "notify"
triage_output_10 = "respond"
triage_output_11 = "notify"
triage_output_12 = "notify"
triage_output_13 = "respond"
triage_output_14 = "ignore"
triage_output_15 = "respond"
triage_output_16 = "notify"

# 응답 기준 (해당하는 경우)
response_criteria_1 = """
• write_email 도구 호출을 사용하여 이메일을 보내 질문을 인지했음을 알리고 조사가 진행될 것임을 확인합니다.
"""

response_criteria_2 = """
• 응답 필요 없음
• 무시 처리되도록 합니다.
"""

response_criteria_3 = """
• 응답 필요 없음
• 사용자에게 알림이 가도록 합니다.
"""

response_criteria_4 = """
• check_calendar_availability 도구 호출을 사용하여 다음 주 화요일 또는 목요일 오후의 일정 가능 여부를 확인합니다.
• 45분 회의 가능 여부를 확인합니다.
• schedule_meeting 도구 호출을 사용하여 캘린더 초대장을 보냅니다.
• write_email 도구 호출을 사용하여 이메일을 보내 세금 계획 요청을 인지했음을 알리고 회의가 예약되었음을 알립니다.
"""

response_criteria_5 = """
• 응답 필요 없음
• 사용자에게 알림이 가도록 합니다.
"""

response_criteria_6 = """
• TechConf 2025 참석에 관심을 표명합니다.
• AI/ML 워크숍에 대한 구체적인 질문을 합니다.
• 단체 할인 세부 정보에 대해 문의합니다.
• write_email 도구 호출을 사용하여 이메일을 보내 TechConf 2025 참석에 대한 관심을 표명하고, AI/ML 워크숍에 대한 구체적인 질문을 하며, 단체 할인 세부 정보를 문의합니다.
"""

response_criteria_7 = """
• 기술 사양 검토에 명시적으로 동의합니다.
• 금요일 마감일을 인지합니다.
• write_email 도구 호출을 사용하여 이메일을 보내 기술 사양 검토에 명시적으로 동의하고 금요일 마감일을 인지했음을 알립니다.
"""

response_criteria_8 = """
• write_email 도구 호출을 사용하여 이메일을 보내 딸의 수영 강좌 등록에 관심을 표명합니다.
"""

response_criteria_9 = """
• 응답 필요 없음
• 사용자에게 알림이 가도록 합니다.
"""

response_criteria_10 = """
• check_calendar_availability 도구 호출을 사용하여 월요일 또는 수요일에 90분 회의 가능 여부를 확인합니다.
• write_email 도구 호출을 사용하여 이메일을 보내 요청을 인지하고 가능한 시간을 제공합니다.
"""

response_criteria_11 = """
• 응답 필요 없음
• 사용자에게 알림이 가도록 합니다.
"""

response_criteria_12 = """
• 응답 필요 없음
• 사용자에게 알림이 가도록 합니다.
"""

response_criteria_13 = """
• 연례 건강 검진 알림을 인지합니다.
• write_email 도구 호출을 사용하여 이메일을 보내 연례 건강 검진 알림을 인지했음을 알립니다.
"""

response_criteria_14 = """
• 응답 필요 없음
• 무시 처리되도록 합니다.
"""

response_criteria_15 = """
• check_calendar_availability 도구 호출을 사용하여 화요일 또는 목요일에 60분 회의 가능 여부를 확인합니다.
• schedule_meeting 도구 호출을 사용하여 캘린더 초대장을 보냅니다.
• write_email 도구 호출을 사용하여 이메일을 보내 공동 발표 협업에 동의하고 회의가 예약되었음을 알립니다.
"""

response_criteria_16 = """
• 응답 필요 없음
• 사용자에게 알림이 가도록 합니다.
"""

examples_triage = [
    {
        "inputs": {"email_input": email_input_1},
        "outputs": {"classification": triage_output_1},
    },
    {
        "inputs": {"email_input": email_input_2},
        "outputs": {"classification": triage_output_2},
    },
    {
        "inputs": {"email_input": email_input_3},
        "outputs": {"classification": triage_output_3},
    },
    {
        "inputs": {"email_input": email_input_4},
        "outputs": {"classification": triage_output_4},
    },
    {
        "inputs": {"email_input": email_input_5},
        "outputs": {"classification": triage_output_5},
    },
    {
        "inputs": {"email_input": email_input_6},
        "outputs": {"classification": triage_output_6},
    },
    {
        "inputs": {"email_input": email_input_7},
        "outputs": {"classification": triage_output_7},
    },
    {
        "inputs": {"email_input": email_input_8},
        "outputs": {"classification": triage_output_8},
    },
    {
        "inputs": {"email_input": email_input_9},
        "outputs": {"classification": triage_output_9},
    },
    {
        "inputs": {"email_input": email_input_10},
        "outputs": {"classification": triage_output_10},
    },
    {
        "inputs": {"email_input": email_input_11},
        "outputs": {"classification": triage_output_11},
    },
    {
        "inputs": {"email_input": email_input_12},
        "outputs": {"classification": triage_output_12},
    },
    {
        "inputs": {"email_input": email_input_13},
        "outputs": {"classification": triage_output_13},
    },
    {
        "inputs": {"email_input": email_input_14},
        "outputs": {"classification": triage_output_14},
    },
    {
        "inputs": {"email_input": email_input_15},
        "outputs": {"classification": triage_output_15},
    },
    {
        "inputs": {"email_input": email_input_16},
        "outputs": {"classification": triage_output_16},
    },
]

email_inputs = [
    email_input_1,
    email_input_2,
    email_input_3,
    email_input_4,
    email_input_5,
    email_input_6,
    email_input_7,
    email_input_8,
    email_input_9,
    email_input_10,
    email_input_11,
    email_input_12,
    email_input_13,
    email_input_14,
    email_input_15,
    email_input_16,
]

email_names = [
    "email_input_1",
    "email_input_2",
    "email_input_3",
    "email_input_4",
    "email_input_5",
    "email_input_6",
    "email_input_7",
    "email_input_8",
    "email_input_9",
    "email_input_10",
    "email_input_11",
    "email_input_12",
    "email_input_13",
    "email_input_14",
    "email_input_15",
    "email_input_16",
]

response_criteria_list = [
    response_criteria_1,
    response_criteria_2,
    response_criteria_3,
    response_criteria_4,
    response_criteria_5,
    response_criteria_6,
    response_criteria_7,
    response_criteria_8,
    response_criteria_9,
    response_criteria_10,
    response_criteria_11,
    response_criteria_12,
    response_criteria_13,
    response_criteria_14,
    response_criteria_15,
    response_criteria_16,
]

triage_outputs_list = [
    triage_output_1,
    triage_output_2,
    triage_output_3,
    triage_output_4,
    triage_output_5,
    triage_output_6,
    triage_output_7,
    triage_output_8,
    triage_output_9,
    triage_output_10,
    triage_output_11,
    triage_output_12,
    triage_output_13,
    triage_output_14,
    triage_output_15,
    triage_output_16,
]

# 내용 분석을 기반으로 각 이메일 응답에 대해 예상되는 도구 호출 정의
# 옵션: write_email, schedule_meeting, check_calendar_availability, done
expected_tool_calls = [
    ["write_email", "done"],  # email_input_1: API 문서 질문
    [],  # email_input_2: 뉴스레터 알림 - 무시
    [],  # email_input_3: 시스템 유지보수 알림 - 알림만
    [
        "check_calendar_availability",
        "schedule_meeting",
        "write_email",
        "done",
    ],  # email_input_4: 세금 관련 통화 일정 조율
    [],  # email_input_5: 경비 보고서 알림 - 알림만
    ["write_email", "done"],  # email_input_6: 컨퍼런스 초대 - 응답 필요
    ["write_email", "done"],  # email_input_7: 문서 검토 요청
    ["write_email", "done"],  # email_input_8: 수영 강좌 등록
    [],  # email_input_9: GitHub PR 댓글 - 알림만
    ["check_calendar_availability", "write_email", "done"],  # email_input_10: 계획 회의
    [],  # email_input_11: AWS 경고 - 알림만
    [],  # email_input_12: 구독 갱신 - 무시
    ["write_email", "done"],  # email_input_13: 병원 예약 알림
    [],  # email_input_14: 소셜 미디어 알림 - 조치 필요 없음
    [
        "check_calendar_availability",
        "schedule_meeting",
        "write_email",
        "done",
    ],  # email_input_15: 공동 발표
    [],  # email_input_16: 뉴스레터 - 알림만
]
