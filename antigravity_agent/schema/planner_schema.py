from pydantic import BaseModel, Field
from typing import List

class PlanSchema(BaseModel):
    main_task: str = Field(description="Single concise restatement of user goal")
    sub_tasks: List[str] = Field(
        description="List of 3 to 5 concise searchable research queries"
    )
