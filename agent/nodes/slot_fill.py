def slot_fill_node(state):
    if not state.get("pending_question"):
        return state

    user_input = state["question"].strip()
    pending = state["pending_question"]

    # Heuristic đơn giản: user chỉ trả lời slot
    if len(user_input.split()) <= 3:
        merged = f"{pending} ở {user_input}"
        return {
            **state,
            "question": merged,
            "pending_question": None,
            "need_user_input": False
        }

    return state
