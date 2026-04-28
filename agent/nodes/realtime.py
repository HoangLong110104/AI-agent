from tool.realtime import realtime_search

def realtime_node(state):
    if "realtime" not in state["sources"]:
        return state

    query = state["question"]
    live_text = realtime_search(query)

    return {
        **state,
        "context": state.get("context", "") + "\n\n" + live_text
    }