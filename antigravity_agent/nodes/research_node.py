from tools.search_tool import search_web
from state.agent_state import AgentState

def research_node(state: AgentState):

    print("--- Research Node ---")

    MAX_SEARCH = 3

    collected = []

    for query in state.research_plan[:MAX_SEARCH]:
        print(f"Searching: {query}")
        result = search_web(query)

        if result:
            cleaned = result[:2000]  # prevent explosion
            collected.append(cleaned)

    state.tool_results = collected
    state.working_memory.extend(collected)

    return state
