from langgraph.graph import StateGraph, END
from agent.state import AgentState

from agent.nodes.memory import memory_node
from agent.nodes.coref import coref_node
from agent.nodes.planner import planner_node
from agent.nodes.rag_internal import internal_rag_node
from agent.nodes.web_router import web_router_node
from agent.nodes.answer import answer_node

g = StateGraph(AgentState)

g.add_node("memory", memory_node)
g.add_node("coref", coref_node)
g.add_node("planner", planner_node)
g.add_node("rag", internal_rag_node)
g.add_node("web", web_router_node)
g.add_node("answer", answer_node)

g.set_entry_point("memory")
g.add_edge("memory", "coref")
g.add_edge("coref", "planner")
g.add_edge("planner", "rag")
g.add_edge("rag", "web")
g.add_edge("web", "answer")
g.add_edge("answer", END)

rag_agent = g.compile()