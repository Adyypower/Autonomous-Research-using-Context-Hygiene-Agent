from tools.search_tool import search_web
from state.agent_state import AgentState

def research_node(state:AgentState):
    for step in state.research_plan:
        result = search_web(step)
        state.tool_results.append(result)
        state.working_memory.append(f"Research on {step}: {result}")
    return state
    