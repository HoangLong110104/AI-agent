from core.llm import chat_with_ai

def answer_node(state):
    answer = chat_with_ai(
        state["question"],
        state["context"]
    )
    return {
        **state,
        "answer": answer
    }