"""이메일 어시스턴트를 위한 도구 프롬프트 템플릿"""

# 프롬프트에 삽입할 표준 도구 설명
STANDARD_TOOLS_PROMPT = """
1. triage_email(ignore, notify, respond) - 이메일을 세 가지 카테고리 중 하나로 분류
2. write_email(to, subject, content) - 지정된 수신자에게 이메일 전송
3. schedule_meeting(attendees, subject, duration_minutes, preferred_day, start_time) - 일정 회의 예약 (preferred_day는 datetime 객체)
4. check_calendar_availability(day) - 특정 날짜의 가능한 시간대 확인
5. Done - 이메일 전송 완료
"""

# HITL 워크플로우를 위한 도구 설명
HITL_TOOLS_PROMPT = """
1. write_email(to, subject, content) - 지정된 수신자에게 이메일 전송
2. schedule_meeting(attendees, subject, duration_minutes, preferred_day, start_time) - 일정 회의 예약 (preferred_day는 datetime 객체)
3. check_calendar_availability(day) - 특정 날짜의 가능한 시간대 확인
4. Question(content) - 사용자에게 후속 질문하기
5. Done - 이메일 전송 완료
"""

# 메모리가 있는 HITL 워크플로우를 위한 도구 설명
# 참고: 메모리 관련 도구를 여기에 추가할 수 있습니다
HITL_MEMORY_TOOLS_PROMPT = """
1. write_email(to, subject, content) - 지정된 수신자에게 이메일 전송
2. schedule_meeting(attendees, subject, duration_minutes, preferred_day, start_time) - 일정 회의 예약 (preferred_day는 datetime 객체)
3. check_calendar_availability(day) - 특정 날짜의 가능한 시간대 확인
4. Question(content) - 사용자에게 후속 질문하기
5. Done - 이메일 전송 완료
"""

# 분류 없는 에이전트 워크플로우를 위한 도구 설명
AGENT_TOOLS_PROMPT = """
1. write_email(to, subject, content) - 지정된 수신자에게 이메일 전송
2. schedule_meeting(attendees, subject, duration_minutes, preferred_day, start_time) - 일정 회의 예약 (preferred_day는 datetime 객체)
3. check_calendar_availability(day) - 특정 날짜의 가능한 시간대 확인
4. Done - 이메일 전송 완료
"""
