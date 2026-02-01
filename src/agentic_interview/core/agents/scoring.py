from agentic_interview.core.schemas.agent_io import ScoringInput, ScoringOutput


class ScoringAgent:
    async def run(self, data: ScoringInput) -> ScoringOutput:
        raise NotImplementedError
