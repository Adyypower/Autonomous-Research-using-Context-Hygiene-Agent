from pydantic import BaseModel
from typing import List , Optional

class AgentState(BaseModel):
    user_goal: str
    research_plan: List[str] = []
    tool_results: List[str] = []
    working_memory: List[str] = []
    compressed_context: Optional[str] = None
    evaluation_score: float = 0.0
    reflection_notes: Optional[str] = None
    confidence_score: float = 0.0
    iteration_count: int = 0

    