# nodes/router_node.py

from config import CONFIDENCE_THRESHOLD, MAX_ITERATIONS
from state.agent_state import AgentState


def router_node(state: AgentState):

    print("\n--- Router Node ---")

    evaluator_conf = state.evaluation_score
    reflection_data = state.reflection_notes or {}

    reflection_decision = reflection_data.get("final_decision", "accept")
    refinement_queries = reflection_data.get("refinement_queries", [])
    updated_conf = reflection_data.get("updated_confidence", evaluator_conf)

    print(f"Evaluator Confidence: {evaluator_conf}")
    print(f"Reflection Decision: {reflection_decision}")
    print(f"Iteration Count: {state.iteration_count}")

    # --- 1️⃣ Hard Stop: High Confidence ---
    if evaluator_conf >= CONFIDENCE_THRESHOLD:
        print("High evaluator confidence. Generating Report.")
        return "report"

    # --- 2️⃣ Hard Stop: Reflection Accepts ---
    if reflection_decision == "accept":
        print("Reflection accepted output. Generating Report.")
        return "report"

    # --- 3️⃣ Hard Stop: Max Iterations Reached ---
    if state.iteration_count >= MAX_ITERATIONS:
        print("Max iterations reached. Generating Report.")
        return "report"

    # --- 4️⃣ Refinement Path (Surgical Mode) ---
    if reflection_decision == "refine" and refinement_queries:
        print("Continuing to refinement.")
        return "retrieve"

    # --- 5️⃣ Fallback ---
    print("Fallback to generating report.")
    return "report"
