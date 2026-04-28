from tool.web import (
    fetch_wikipedia,
    fetch_general_web
)

def tool_router_node(state):
    # ✅ Nếu nội bộ dùng được → không search
    if state.get("found_internal"):
        return state

    question = state["question"]
    intent = state.get("intent", "")

    print(">>> TOOL ROUTER intent =", intent)

    text = ""

    # ✅ FACT / DANH SÁCH / LỊCH SỬ → WIKIPEDIA
    if intent == "static_fact":
        print(">>> Using Wikipedia")
        text = fetch_wikipedia(question, lang="en")

    # ✅ FALLBACK → GENERAL WEB
    if not text.strip():
        print(">>> Fallback to general web")
        text = fetch_general_web(question)

    if not text.strip():
        print(">>> WEB SEARCH FAILED")
        return state

    return {
        **state,
        "context": "[WEB DATA]\n" + text,
        "tool_used": True
    }