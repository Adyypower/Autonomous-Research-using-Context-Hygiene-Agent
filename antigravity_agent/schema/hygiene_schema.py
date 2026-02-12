# schema/hygiene_schema.py

from pydantic import BaseModel, Field
from typing import List

class HygieneSchema(BaseModel):

    key_findings: List[str] = Field(
        description=(
            "Core factual insights directly related to the user goal. "
            "Each item must be concise, specific, and evidence-based. "
            "Avoid repetition and avoid vague statements."
        )
    )

    benefits: List[str] = Field(
        description=(
            "Clearly identified positive impacts or advantages related to the user goal. "
            "Each item should describe one concrete benefit."
        )
    )

    risks: List[str] = Field(
        description=(
            "Clearly identified risks, limitations, or negative consequences "
            "associated with the topic. Each item should describe one concrete risk."
        )
    )

    regulatory_notes: List[str] = Field(
        description=(
            "Relevant regulatory, legal, governance, or policy-related insights "
            "that affect or influence the topic."
        )
    )

    summary: str = Field(
        description=(
            "A concise synthesis (max 150 words) summarizing the overall findings "
            "in a structured and neutral tone."
        )
    )
