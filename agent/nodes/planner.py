from core.llm import chat_with_ai

def planner_node(state):
    question = state["question"]
    topic = state.get("current_topic", "")
    summary = state.get("conversation_summary", "")

    prompt = (
        "Bạn là AI planner.\n\n"
        f"Chủ đề: {topic}\n"
        f"Tóm tắt hội thoại: {summary}\n"
        f"Câu hỏi: {question}\n\n"
        "Quyết định nên tra từ nguồn nào:\n"
        "internal, wikipedia, vietnamnet, health, general_web\n\n"
        "Chỉ trả về danh sách nguồn hợp lệ, phân cách bằng dấu phẩy.\n"
        "Không giải thích thêm."
    )

    # Ask with a control question so model focuses on planning instruction in context.
    plan_text = chat_with_ai("planner", prompt)

    allowed = {"internal", "wikipedia", "vietnamnet", "health", "general_web"}
    raw_tokens = [s.strip().lower() for s in plan_text.split(",") if s.strip()]
    sources = [s for s in raw_tokens if s in allowed]

    q = question.lower()
    is_realtime = any(k in q for k in [
        "hôm nay", "hom nay", "rạng sáng", "rang sang", "thời tiết", "thoi tiet",
        "kết quả", "ket qua", "live", "tỷ số", "ty so", "score", "trực tiếp", "truc tiep"
    ])

    if not sources:
        sources = ["general_web"] if is_realtime else ["internal", "general_web"]

    return { **state, "plan": plan_text, "sources": sources }