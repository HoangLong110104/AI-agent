from typing import TypedDict, List

class AgentState(TypedDict):
    question: str
    history: List[dict]

    # ✅ MỨC B
    conversation_summary: str
    current_topic: str

    plan: str
    sources: list
    context: str
    answer: str