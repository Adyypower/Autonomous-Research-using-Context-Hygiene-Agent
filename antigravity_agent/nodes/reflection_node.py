# nodes/reflection_node.py

from langchain_google_genai import ChatGoogleGenerativeAI
from schema.reflection_schema import ReflectionSchema
from prompts.reflection_prompt import REFLECTION_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0.2  # slight flexibility
)

structured_llm = llm.with_structured_output(ReflectionSchema)

def reflection_node(state: AgentState):

    print("--- Reflection Node ---")

    if not state.compressed_context:
        return state

    from config import MAX_RAG_CONTENT_CHARS, memory_manager # Lazy import

    # --- RAG check for Reflection ---
    rag_docs = memory_manager.retrieve(state.user_goal, top_k=3)
    rag_context = "\n".join(rag_docs)
    rag_context = rag_context[:MAX_RAG_CONTENT_CHARS]
    
    if not rag_docs:
        rag_context = "No relevant memory found."

    prompt = REFLECTION_PROMPT.format(
        user_goal=state.user_goal,
        rag_context=rag_context,
        current_context=state.compressed_context, # Renamed for clarity in prompt
        evaluation_score=state.evaluation_score # Pass evaluation score directly
    )

    try:
        response: ReflectionSchema = structured_llm.invoke(prompt)
    except Exception:
        print("Reflection failed.")
        return state

    reflection_data = response.model_dump()

    state.reflection_notes = reflection_data
    state.confidence_score = reflection_data["updated_confidence"]

    print(f"Decision: {reflection_data['final_decision']}")

    # --- Crucial Fix: Update state here for persistence ---
    if reflection_data['final_decision'] == 'refine':
        refinement_queries = reflection_data.get("refinement_queries", [])
        if refinement_queries:
            state.research_plan = refinement_queries[:2]
            state.tool_results = [] # Clear for new search
            state.iteration_count += 1
            print(f"Refinement Plan Updated. Iteration: {state.iteration_count}")

    return state
