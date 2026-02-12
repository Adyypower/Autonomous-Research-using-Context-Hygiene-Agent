from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class AgentState(BaseModel):

    user_goal: str

    research_plan: List[str] = Field(default_factory=list)
    tool_results: List[str] = Field(default_factory=list)
    working_memory: List[str] = Field(default_factory=list)

    compressed_context: Optional[Dict[str, Any]] = None

    evaluation_score: float = 0.0
    confidence_score: float = 0.0

    reflection_notes: Optional[Dict[str, Any]] = None

    iteration_count: int = 0
    api_calls_used: int = 0
