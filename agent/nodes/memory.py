from core.llm import chat_with_ai

def memory_node(state):
    history = state.get("history", [])
    prev_summary = state.get("conversation_summary", "")

    history_text = ""
    for m in history[-6:]:
        role = "User" if m["role"] == "user" else "Assistant"
        history_text += f"{role}: {m['content']}\n"

    prompt = (
        "Bạn là AI quản lý trí nhớ hội thoại.\n\n"
        f"Tóm tắt trước đó (nếu có):\n{prev_summary}\n\n"
        f"Hội thoại mới:\n{history_text}\n\n"
        "Hãy:\n"
        "1. Cập nhật tóm tắt hội thoại ngắn gọn (2–3 câu).\n"
        "2. Xác định CHỦ ĐỀ HIỆN TẠI của cuộc hội thoại.\n\n"
        "Trả về theo dạng:\n"
        "SUMMARY: ...\n"
        "TOPIC: ..."
    )

    res = chat_with_ai("memory", prompt)

    summary, topic = "", ""
    for line in res.splitlines():
        if line.startswith("SUMMARY:"):
            summary = line.replace("SUMMARY:", "").strip()
        if line.startswith("TOPIC:"):
            topic = line.replace("TOPIC:", "").strip()

    return {
        **state,
        "conversation_summary": summary,
        "current_topic": topic,
    }