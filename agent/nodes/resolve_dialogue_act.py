from core.llm import chat_with_ai
import json

def resolve_dialogue_act(state):
    ds = state.get("dialogue_state", {})
    if not ds.get("awaiting_reply"):
        return state

    user_input = state["question"]
    last_q = ds["last_question"]

    prompt = f"""
Câu hỏi trước:
\"{last_q}\"

Tin nhắn hiện tại của người dùng:
\"{user_input}\"

Hãy trả lời:
- Nếu đây là CÂU TRẢ LỜI cho câu hỏi trước → trả JSON {{ "type": "reply", "merged_question": "<câu hỏi hoàn chỉnh>" }}
- Nếu đây là MỘT CÂU HỎI MỚI → trả JSON {{ "type": "new_question" }}

Chỉ trả JSON.
"""

    resp = chat_with_ai(user_input, prompt)
    data = json.loads(resp)

    if data["type"] == "reply":
        return {
            **state,
            "question": data["merged_question"],
            "dialogue_state": {
                "awaiting_reply": False,
                "last_question": None
            }
        }

    # user hỏi câu mới → reset state
    return {
        **state,
        "dialogue_state": {
            "awaiting_reply": False,
            "last_question": None
        }
    }
