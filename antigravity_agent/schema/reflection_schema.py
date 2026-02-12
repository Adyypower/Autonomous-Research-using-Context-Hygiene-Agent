# schema/reflection_schema.py

from pydantic import BaseModel, Field
from typing import List

class ReflectionSchema(BaseModel):

    improvement_needed: bool = Field(
        description="True if research needs refinement, False if sufficient."
    )

    reasoning: str = Field(
        description="Short explanation based strictly on evaluator findings."
    )

    refinement_queries: List[str] = Field(
        description="Up to 2 concise follow-up research queries if improvement is needed."
    )

    final_decision: str = Field(
        description='Must be either "refine" or "accept".'
    )

    updated_confidence: float = Field(
        description="Revised confidence score between 0 and 1."
    )
