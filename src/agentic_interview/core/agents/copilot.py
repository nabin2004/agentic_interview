from agentic_interview.core.schemas.agent_io import CopilotInput, CopilotOutput


class LiveCopilotAgent:
    async def run(self, data: CopilotInput) -> CopilotOutput:
        raise NotImplementedError
