from pydantic import BaseModel
from typing import Optional


class SkillScore(BaseModel):
    skill: str
    score: Optional[int]  # None = insufficient signal
    confidence: float  # 0.0 – 1.0
    rationale: str


class InterviewScorecard(BaseModel):
    scores: list[SkillScore]
    overall_recommendation: Optional[str]  # advance / hold / no_decision
