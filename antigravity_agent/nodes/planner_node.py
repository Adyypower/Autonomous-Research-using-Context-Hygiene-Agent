from langchain_google_genai import ChatGoogleGenerativeAI
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(model=MODEL_NAME)

def planner_node(state:AgentState):
    prompt = f"""
    Break this goal into structured research steps:
    {state.user_goal}
    """
    print("--- Planner Node ---")
    response = llm.invoke(prompt)
    print(f"Plan generated: {len(response.content.split())} words")
    state.research_plan = [step for step in response.content.split("\n") if step.strip()]
    return state