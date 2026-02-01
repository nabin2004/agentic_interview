from agentic_interview.core.agents.planner import InterviewPlannerAgent
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.agents.scoring import ScoringAgent
from agentic_interview.core.schemas.agent_io import PlannerInput


class InterviewFlow:
    def __init__(
        self,
        planner: InterviewPlannerAgent,
        extractor: SignalExtractionAgent,
        scorer: ScoringAgent,
    ):
        self.planner = planner
        self.extractor = extractor
        self.scorer = scorer

    async def run(self, planner_input: PlannerInput):
        plan = await self.planner.run(planner_input)
        # transcript comes later
        return plan
