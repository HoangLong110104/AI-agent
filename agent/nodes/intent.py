from core.llm import chat_with_ai

def intent_node(state):
    q = state["question"]

    prompt = (
        "Phân loại câu hỏi sau thành MỘT trong các loại:\n"
        "- static_fact\n"
        "- realtime_fact\n"
        "- news_event\n"
        "- opinion\n"
        "- ambiguous\n\n"
        f"Câu hỏi: {q}\n\n"
        "Chỉ trả về tên loại."
    )

    intent = chat_with_ai(q, prompt).strip().lower()

    return {**state, "intent": intent}