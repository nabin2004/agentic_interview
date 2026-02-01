from agentic_interview.core.schemas.agent_io import EvidenceInput, EvidenceOutput


class SignalExtractionAgent:
    async def run(self, data: EvidenceInput) -> EvidenceOutput:
        raise NotImplementedError
