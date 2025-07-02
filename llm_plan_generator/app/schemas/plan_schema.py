from pydantic import BaseModel

class PlanInput(BaseModel):
    goal: str
    deadline: str  # ISO date string, e.g., "2025-07-31"
