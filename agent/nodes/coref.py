from core.llm import chat_with_ai

def coref_node(state):
    question = state["question"]
    topic = state.get("current_topic", "")
    summary = state.get("conversation_summary", "")

    prompt = (
        "Bạn là AI hiểu ngữ cảnh hội thoại.\n\n"
        f"Chủ đề hiện tại: {topic}\n"
        f"Tóm tắt hội thoại: {summary}\n\n"
        f"Câu hỏi mới: {question}\n\n"
        "Nếu câu hỏi mơ hồ (ví dụ: 'nó', 'các nước', 'cái đó'), "
        "hãy viết lại câu hỏi cho RÕ NGHĨA.\n"
        "Nếu đã rõ, giữ nguyên.\n\n"
        "Chỉ trả về câu hỏi đã chuẩn hoá."
    )

    clarified = chat_with_ai(question, prompt)

    return {
        **state,
        "question": clarified.strip()
    }