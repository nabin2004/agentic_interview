import pytest
from datetime import datetime
from agentic_interview.core.agents.copilot import LiveCopilotAgent
from agentic_interview.core.schemas.agent_io import CopilotInput
from agentic_interview.core.schemas.interview import InterviewPlan, Skill
from agentic_interview.core.schemas.transcript import Transcript, TranscriptUtterance


class FakeLLM:
    async def generate(self, prompt: str) -> str:
        return ""  


@pytest.mark.asyncio
async def test_live_copilot_agent_uncovered_skills():
    llm = FakeLLM()
    agent = LiveCopilotAgent(llm=llm)

    plan = InterviewPlan(
        role="ML Engineer",
        level="mid",
        skills=[
            Skill(name="Python", description="Python skills"),
            Skill(name="SQL", description="SQL skills")
        ],
        questions={}
    )

    transcript = Transcript(
        utterances=[
            TranscriptUtterance(
                speaker="candidate",
                text="I built pipelines using Python",
                timestamp=datetime.utcnow()
            )
        ]
    )

    covered_skills = {"Python"}
    input_data = CopilotInput(
        transcript=transcript,
        interview_plan=plan,
        covered_skills=covered_skills
    )

    result = await agent.run(input_data)

    assert "Ask the candidate a question to assess their SQL skills." in result.followup_suggestions
    assert "SQL" in result.uncovered_skills
