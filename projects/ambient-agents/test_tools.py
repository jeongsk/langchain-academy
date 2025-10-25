from dotenv import load_dotenv
from email_assistant.email_assistant import email_assistant
from email_assistant.eval.email_dataset import email_inputs, expected_tool_calls
from email_assistant.utils import extract_tool_calls, format_messages_string
from langsmith import testing as t
import pytest


load_dotenv(".env")


@pytest.mark.langsmith
@pytest.mark.parametrize(
    ("email_input", "expected_calls"),
    [
        # 이메일 답장이 예상되는 몇 가지 예시를 선택하세요
        (email_inputs[0], expected_tool_calls[0]),
        (email_inputs[3], expected_tool_calls[3]),
    ],
)
def test_email_dataset_tool_calls(email_input, expected_calls):
    """이메일 처리 과정에 예상되는 도구 호출이 포함되어 있는지 테스트합니다."""
    # 이메일 어시스턴트를 실행합니다.
    result = email_assistant.invoke({"email_input": email_input})

    # 메시지 목록에서 도구 호출 추출합니다.
    extracted_tool_calls = extract_tool_calls(result["messages"])

    # 추출된 도구 호출에 예상된 모든 호출이 포함되어 있는지 확인합니다.
    missing_calls = [
        call for call in expected_calls if call.lower() not in extracted_tool_calls
    ]

    t.log_outputs(
        {
            "missing_calls": missing_calls,
            "extracted_tool_calls": extracted_tool_calls,
            "response": format_messages_string(result["messages"]),
        }
    )

    # 예상된 호출이 누락되지 않으면 테스트가 통과됩니다.
    assert len(missing_calls) == 0
