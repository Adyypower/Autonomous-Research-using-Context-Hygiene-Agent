# nodes/hygiene_node.py

from langchain_google_genai import ChatGoogleGenerativeAI
from schema.hygiene_schema import HygieneSchema
from prompts.hygiene_prompt import HYGIENE_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState
from config import memory_manager, MAX_RAW_CONTENT_CHARS, MAX_RAG_CONTENT_CHARS

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0
)

structured_llm = llm.with_structured_output(HygieneSchema)

def hygiene_node(state: AgentState):

    print("--- Hygiene Node ---")

    MAX_RAG_CONTENT_CHARS = 5000
    MAX_RAW_CONTENT_CHARS = 15000
    from config import MAX_RAW_CONTENT_CHARS, MAX_RAG_CONTENT_CHARS # Lazy import or move to top

    # --- 1. Current Raw Content ---
    raw_content = "\n\n".join(state.tool_results)
    raw_content = raw_content[:MAX_RAW_CONTENT_CHARS] # Cap current content

    # --- 2. RAG Context (Long-term) ---
    rag_docs = memory_manager.retrieve(state.user_goal, top_k=3)
    rag_context = "\n".join(rag_docs)
    rag_context = rag_context[:MAX_RAG_CONTENT_CHARS] # Cap RAG content

    if not rag_docs:
        rag_context = "No relevant memory found."

    # --- 3. Previous Context ---
    if state.iteration_count > 0 and state.compressed_context:
        previous = str(state.compressed_context)
    else:
        previous = "None"

    prompt = HYGIENE_PROMPT.format(
        user_goal=state.user_goal,
        previous_context=previous,
        rag_context=rag_context,
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
    
    # Observability Log
    state.logs.append({
        "node": "hygiene",
        "raw_chars": len(raw_content),
        "rag_chars": len(rag_context),
        "findings_count": len(response.key_findings)
    })

    print(f"Context compressed. Raw: {len(raw_content)} chars, RAG: {len(rag_context)} chars.")

    return state
