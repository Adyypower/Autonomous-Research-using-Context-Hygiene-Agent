# nodes/hygiene_node.py

from langchain_google_genai import ChatGoogleGenerativeAI
from schema.hygiene_schema import HygieneSchema
from prompts.hygiene_prompt import HYGIENE_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState
from config import memory_manager

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
    if state.iteration_count > 0 and state.compressed_context:
        previous = str(state.compressed_context)
    else:
        previous = "None"

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
    memory_manager.store_compressed_context(
        state.compressed_context,
        iteration=state.iteration_count
    )

    # Replace working memory with compressed context only
    import json
    state.working_memory = [json.dumps(compressed)]
    state.tool_results = []
    print("Context compressed successfully")

    return state
