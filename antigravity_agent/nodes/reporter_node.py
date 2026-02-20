# nodes/reporter_node.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from prompts.reporter_prompt import REPORTER_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState
import json

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0.3
)

def reporter_node(state: AgentState):
    print("--- Reporter Node ---")
    
    # Gather context
    # We might have compressed context or working memory
    context_str = ""
    if state.compressed_context:
        context_str = json.dumps(state.compressed_context, indent=2)
    elif state.working_memory:
        context_str = "\n".join(state.working_memory)
    else:
        context_str = "No specific research data found."

    reflection_str = json.dumps(state.reflection_notes, indent=2) if state.reflection_notes else "None"
    
    prompt = REPORTER_PROMPT.format(
        user_goal=state.user_goal,
        context=context_str,
        reflection_notes=reflection_str
    )
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        final_report = response.content
    except Exception as e:
        final_report = f"Error generating report: {e}"
        print(f"Reporter error: {e}")

    state.final_report = final_report

    # Observability Log
    state.logs.append({
        "node": "reporter",
        "status": "Final Report Generated"
    })

    return state
