from core.rag import hybrid_search

def internal_rag_node(state):
    if "internal" not in state["sources"]:
        return state

    docs = hybrid_search(state["question"], topk=3)
    ctx = "\n\n".join(docs)

    return {
        **state,
        "context": ctx
    }