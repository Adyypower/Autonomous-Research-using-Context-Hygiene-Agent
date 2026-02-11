from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

def reflection_node(state: AgentState):
    print("--- Reflection Node ---")
    prompt = f"""
    Evaluation score: {state.evaluation_score}
    What improvements are needed?
    """

    response = llm.invoke(prompt)
    state.reflection_notes = response.content
    return state
