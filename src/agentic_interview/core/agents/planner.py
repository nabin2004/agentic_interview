from agentic_interview.core.schemas.agent_io import PlannerInput, PlannerOutput


class InterviewPlannerAgent:
    async def run(self, data: PlannerInput) -> PlannerOutput:
        raise NotImplementedError
