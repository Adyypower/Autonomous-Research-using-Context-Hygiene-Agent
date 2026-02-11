from config import CONFIDENCE_THRESHOLD, MAX_ITERATIONS
from state.agent_state import AgentState

def router_node(state: AgentState):

    if state.confidence_score < CONFIDENCE_THRESHOLD and state.iteration_count < MAX_ITERATIONS:
        state.iteration_count += 1
        return "replan"

    return "end"
