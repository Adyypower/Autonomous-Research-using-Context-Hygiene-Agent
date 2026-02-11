from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

def evaluator_node(state: AgentState):
    print("--- Evaluator Node ---")
    content = " ".join(state.working_memory)

    prompt = f"""
    Evaluate this research summary from 0 to 1:
    {content}

    Return only a number.
    """

    response = llm.invoke(prompt)

    try:
        state.evaluation_score = float(response.content.strip())
    except:
        state.evaluation_score = 0.5

    state.confidence_score = state.evaluation_score
    return state
