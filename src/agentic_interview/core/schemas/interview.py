from pydantic import BaseModel
from typing import List


class Skill(BaseModel):
    name: str
    description: str
    required: bool = True


class InterviewPlan(BaseModel):
    role: str
    level: str  # junior / mid / senior
    skills: List[Skill]
    questions: dict[str, List[str]]  # skill -> questions
