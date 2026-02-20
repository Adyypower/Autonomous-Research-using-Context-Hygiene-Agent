from tools.search_tool import search_web
from state.agent_state import AgentState
from config import memory_manager

def research_node(state: AgentState):

    print("--- Research Node ---")

    MAX_SEARCH = 6

    collected = []

    for query in state.research_plan[:MAX_SEARCH]:
        print(f"Searching: {query}")
        result = search_web(query)

        if result:
            cleaned = result[:2000]  # prevent explosion
            collected.append(cleaned)

    state.tool_results = collected
    state.working_memory.extend(collected)

    # Observability Log
    for i, query in enumerate(state.research_plan[:MAX_SEARCH]):
        res_len = len(collected[i]) if i < len(collected) else 0
        state.logs.append({
            "node": "research",
            "query": query,
            "tool": "search_web",
            "result_length": res_len
        })

    # long term memory storage
    memory_manager.store_raw_results(
        state.tool_results,
        query=str(state.research_plan),
        iteration=state.iteration_count
    )
    return state
