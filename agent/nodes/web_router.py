from tool.tool_gg import get_web_data


def web_router_node(state):
    """
    Node dùng khi agent quyết định search web
    """

    sources = state.get("sources", [])
    # Only run web retrieval when planner selected a web-capable source.
    if not any(s in sources for s in ["wikipedia", "vietnamnet", "health", "general_web"]):
        return state

    q = state["question"]

    web_context = get_web_data(q).strip()

    if not web_context:
        return state

    base_context = state.get("context", "").strip()
    merged_context = (
        f"{base_context}\n\n[WEB SEARCH RESULT]\n{web_context}"
        if base_context
        else f"[WEB SEARCH RESULT]\n{web_context}"
    )

    return {
        **state,
        "context": merged_context
    }