import tiktoken
from config import TOKEN_LIMIT
from state.agent_state import AgentState

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def hygiene_node(state:AgentState):
    combined = " ".join(state.working_memory)

    if count_tokens(combined)>TOKEN_LIMIT:  
        state.compressed_context  = combined[:2000]
        state.working_memory = [state.compressed_context]

    return state    