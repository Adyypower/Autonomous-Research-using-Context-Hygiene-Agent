from graph.build_graph import build_graph
from state.agent_state import AgentState

if __name__ == "__main__":

    graph = build_graph()

    initial_state = AgentState(
        user_goal="Research impact of agentic AI in healthcare"
    )

    result = graph.invoke(initial_state)

    print(result)
