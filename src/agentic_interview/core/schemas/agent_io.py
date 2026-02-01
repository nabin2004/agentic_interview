from pydantic import BaseModel
from agentic_interview.core.schemas.interview import InterviewPlan
from agentic_interview.core.schemas.transcript import Transcript
from agentic_interview.core.schemas.evidence import EvidenceSnippet
from agentic_interview.core.schemas.scoring import InterviewScorecard

class PlannerInput(BaseModel):
    job_description: str
    resume: str


class PlannerOutput(BaseModel):
    interview_plan: InterviewPlan


class CopilotInput(BaseModel):
    transcript: Transcript
    interview_plan: InterviewPlan
    covered_skills: set[str]


class CopilotOutput(BaseModel):
    followup_suggestions: list[str]
    uncovered_skills: list[str]


class EvidenceInput(BaseModel):
    transcript: Transcript
    interview_plan: InterviewPlan


class EvidenceOutput(BaseModel):
    evidence: list[EvidenceSnippet]


class ScoringInput(BaseModel):
    evidence: list[EvidenceSnippet]


class ScoringOutput(BaseModel):
    scorecard: InterviewScorecard
