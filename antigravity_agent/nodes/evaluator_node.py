# nodes/evaluator_node.py

from langchain_google_genai import ChatGoogleGenerativeAI
from schema.evaluator_schema import EvaluatorSchema
from prompts.evaluator_prompt import EVALUATOR_PROMPT
from config import MODEL_NAME
from state.agent_state import AgentState

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0
)

structured_llm = llm.with_structured_output(EvaluatorSchema)

def evaluator_node(state: AgentState):

    print("--- Evaluator Node ---")

    if not state.compressed_context:
        print("No compressed context to evaluate.")
        return state

    prompt = EVALUATOR_PROMPT.format(
        user_goal=state.user_goal,
        compressed_context=state.compressed_context
    )

    try:
        response: EvaluatorSchema = structured_llm.invoke(prompt)
    except Exception:
        print("Evaluation failed.")
        return state

    scores = response.model_dump()

    state.evaluation_score = scores["overall_confidence"]
    state.confidence_score = scores["overall_confidence"]

    print(f"Evaluation Score: {state.confidence_score}")

    return state
