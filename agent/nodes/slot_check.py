import json
from core.llm import chat_with_ai

def slot_check_node(state):
    question = state["question"]
    intent = state.get("intent")

    if intent == "realtime_fact":
        prompt = f"""
Câu hỏi: "{question}"

Kiểm tra xem câu hỏi đã đủ thông tin để trả lời chưa.
Nếu thiếu, hãy hỏi lại người dùng.

Nếu thiếu:
{{"status": "MISSING", "ask": "..."}}

Nếu đủ:
{{"status": "OK"}}
"""
        resp = chat_with_ai(question, prompt)
        data = json.loads(resp)

        if data["status"] == "MISSING":
            return {
                **state,
                "answer": data["ask"],
                "need_user_input": True,
                "pending_question": question   # ✅ CỰC QUAN TRỌNG
            }

    return state
