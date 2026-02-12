from langgraph.graph import StateGraph, END
from state.agent_state import AgentState

from nodes.planner_node import planner_node
from nodes.research_node import research_node
from nodes.hygiene_node import hygiene_node
from nodes.evaluator_node import evaluator_node
from nodes.reflection_node import reflection_node
from nodes.router_node import router_node

def build_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("research", research_node)
    workflow.add_node("hygiene", hygiene_node)
    workflow.add_node("evaluate", evaluator_node)
    workflow.add_node("reflect", reflection_node)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "research")
    workflow.add_edge("research", "hygiene")
    workflow.add_edge("hygiene", "evaluate")
    workflow.add_edge("evaluate", "reflect")

    workflow.add_conditional_edges(
        "reflect",
        router_node,
        {
            "research": "research",
            "end": END
        }
    )

    return workflow.compile()
