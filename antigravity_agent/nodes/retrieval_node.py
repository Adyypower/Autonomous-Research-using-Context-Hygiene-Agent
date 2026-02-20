from state.agent_state import AgentState
from config import memory_manager


def retrieval_node(state: AgentState):

    print("--- Retrieval Node ---")

    retrieved = []

    for query in state.research_plan:
        docs = memory_manager.retrieve(
            query,
            top_k=3,
            memory_type="raw_research"
        )
        retrieved.extend(docs)

    if retrieved:
        print(f"Retrieved {len(retrieved)} memory documents.")
        state.tool_results.extend(retrieved)

    # Observability Log
    state.logs.append({
        "node": "retrieval",
        "docs_retrieved": len(retrieved)
    })

    return state
