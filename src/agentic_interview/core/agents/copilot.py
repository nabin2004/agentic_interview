from typing import List, Set
from agentic_interview.core.schemas.agent_io import CopilotInput, CopilotOutput
from agentic_interview.ml.llm.base import LLMClient
from pydantic import BaseModel


class LiveCopilotAgent:
    """
    Provides real-time interview suggestions for the recruiter based on
    the transcript, interview plan, and covered skills.
    """
    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def run(self, data: CopilotInput) -> CopilotOutput:
        # Determines uncovered skills
        planned_skills: Set[str] = {skill.name for skill in data.interview_plan.skills}
        uncovered_skills: Set[str] = planned_skills - data.covered_skills

        followup_suggestions: List[str] = []

        # If no uncovered skills, maybe prompt for deeper exploration
        if not uncovered_skills:
            followup_suggestions.append(
                "All planned skills covered. Consider asking for examples or challenges the candidate has faced."
            )
        else:
            for skill in uncovered_skills:
                followup_suggestions.append(f"Ask the candidate a question to assess their {skill} skills.")

        # # TODO: Placeholder for LLM integration later
        # prompt = build_prompt(data.transcript, uncovered_skills)
        # raw_suggestions = await self.llm.generate(prompt)
        # followup_suggestions = parse_suggestions(raw_suggestions)

        return CopilotOutput(
            followup_suggestions=followup_suggestions,
            uncovered_skills=list(uncovered_skills)
        )
