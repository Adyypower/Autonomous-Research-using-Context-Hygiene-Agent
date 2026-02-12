# schema/evaluator_schema.py

from pydantic import BaseModel, Field
from typing import List

class EvaluatorSchema(BaseModel):

    relevance_score: float = Field(
        description="Score from 0 to 1 indicating how well content addresses user goal."
    )

    completeness_score: float = Field(
        description="Score from 0 to 1 indicating coverage of important aspects."
    )

    clarity_score: float = Field(
        description="Score from 0 to 1 indicating clarity and structure."
    )

    major_gaps: List[str] = Field(
        description="List of critical missing aspects if any. Keep concise."
    )

    overall_confidence: float = Field(
        description="Final confidence score from 0 to 1 combining all criteria."
    )
