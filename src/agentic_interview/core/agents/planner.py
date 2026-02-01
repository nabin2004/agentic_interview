import json
from agentic_interview.ml.llm.base import LLMClient
from agentic_interview.core.schemas.interview import InterviewPlan, Skill
from agentic_interview.core.prompts.planner import INTERVIEW_PLAN_PROMPT


class InterviewPlannerAgent:
    """Generates a structured InterviewPlan from a job description or candidate profile."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def run(self, job_description: str, role: str, level: str) -> InterviewPlan:
        prompt = INTERVIEW_PLAN_PROMPT.format(
            role=role,
            level=level,
            job_description=job_description
        )

        raw_output = await self.llm.generate(prompt)

        try:
            parsed = json.loads(raw_output)
            skills = [Skill(**s) for s in parsed.get("skills", [])]
            questions = parsed.get("questions", {})
        except Exception:
            raise RuntimeError(
                f"PlannerAgent failed to parse LLM output: {raw_output}"
            ) from e


        return InterviewPlan(
            role=role,
            level=level,
            skills=skills,
            questions=questions
        )
