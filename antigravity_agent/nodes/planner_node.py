from langchain_google_genai import ChatGoogleGenerativeAI
from schema.planner_schema import PlanSchema
from prompts.planner_prompt import PLANNER_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(model=MODEL_NAME , temperature = 0)

structured_llm = llm.with_structured_output(PlanSchema)

def planner_node(state: AgentState):

    print("--- Planner Node ---")

    prompt = PLANNER_PROMPT.format(user_goal=state.user_goal)

    try:
        response: PlanSchema = structured_llm.invoke(prompt)
    except Exception as e:
        print(f"Planner failed: {e}")
        state.research_plan = [state.user_goal]
        return state

    MAX_TASKS = 5

    tasks = response.sub_tasks[:MAX_TASKS]
    tasks = [t.strip()[:120] for t in tasks if t.strip()]
    tasks = list(dict.fromkeys(tasks))

    state.research_plan = tasks

    print(f"Generated {len(tasks)} sub tasks")
    for t in tasks:
        print(f"- {t}")

    return state
