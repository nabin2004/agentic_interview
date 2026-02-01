import pytest
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.schemas.agent_io import EvidenceInput
from agentic_interview.core.schemas.interview import InterviewPlan, Skill
from agentic_interview.core.schemas.transcript import Transcript, TranscriptUtterance
from datetime import datetime


class FakeLLM:
    async def generate(self, prompt: str) -> str:
        return """
        [
          {
            "skill": "Python",
            "text": "I built data pipelines using Python and Pandas",
            "strength": "strong"
          }
        ]
        """


@pytest.mark.asyncio
async def test_signal_extraction_agent():
    agent = SignalExtractionAgent(llm=FakeLLM())

    plan = InterviewPlan(
        role="ML Engineer",
        level="mid",
        skills=[Skill(name="Python", description="Python skills")],
        questions={},
    )

    transcript = Transcript(
        utterances=[
            TranscriptUtterance(
                speaker="candidate",
                text="I built data pipelines using Python and Pandas",
                timestamp=datetime.utcnow(),
            )
        ]
    )

    data = EvidenceInput(transcript=transcript, interview_plan=plan)
    result = await agent.run(data)

    assert result.evidence[0].skill == "Python"
    assert result.evidence[0].strength == "strong"
