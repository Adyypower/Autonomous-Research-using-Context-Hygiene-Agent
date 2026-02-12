# nodes/hygiene_node.py

from langchain_google_genai import ChatGoogleGenerativeAI
from schema.hygiene_schema import HygieneSchema
from prompts.hygiene_prompt import HYGIENE_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0
)

structured_llm = llm.with_structured_output(HygieneSchema)

def hygiene_node(state: AgentState):

    print("--- Hygiene Node ---")

    # Combine raw tool results safely
    raw_content = "\n\n".join(state.tool_results)

    # Hard cap input size (VERY IMPORTANT)
    raw_content = raw_content[:8000]

    # Get previous context safely
    previous = str(state.compressed_context) if state.compressed_context else "None"

    prompt = HYGIENE_PROMPT.format(
        user_goal=state.user_goal,
        previous_context=previous,
        research_content=raw_content
    )

    try:
        response: HygieneSchema = structured_llm.invoke(prompt)
    except Exception as e:
        print(f"Hygiene failed: {e}")
        return state

    # Store compressed structured data
    compressed = response.model_dump()

    state.compressed_context = compressed

    # Replace working memory with compressed context only
    state.working_memory = [str(compressed)]

    print("Context compressed successfully")

    return state
