import pytest
from datetime import datetime
from agentic_interview.core.orchestration.interview_flow import InterviewFlow
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.agents.scoring import ScoringAgent
from agentic_interview.core.agents.copilot import LiveCopilotAgent
from agentic_interview.ml.llm.base import LLMClient
from agentic_interview.core.schemas.agent_io import EvidenceInput
from agentic_interview.core.schemas.interview import InterviewPlan, Skill
from agentic_interview.core.schemas.transcript import Transcript, TranscriptUtterance


class FakeLLM(LLMClient):
    async def generate(self, prompt: str) -> str:
        # Deterministic output for testing SignalExtractionAgent
        return """
        [
            {
                "skill": "Python",
                "text": "I built pipelines in Python",
                "strength": "strong"
            }
        ]
        """


@pytest.mark.asyncio
async def test_interview_flow_end_to_end():
    llm = FakeLLM()
    extractor = SignalExtractionAgent(llm=llm)
    scorer = ScoringAgent(llm=llm)
    copilot = LiveCopilotAgent(llm=llm)

    flow = InterviewFlow(
        planner=None,
        extractor=extractor,
        scorer=scorer,
        copilot=copilot
    )

    # Setup interview plan and transcript
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
                text="I built pipelines in Python",
                timestamp=datetime.utcnow()
            )
        ]
    )

    evidence_input = EvidenceInput(transcript=transcript, interview_plan=plan)
    result = await flow.run(evidence_input, transcript_input=evidence_input, covered_skills={"Python"})

    # ---- Assertions ----

    # Evidence extraction
    evidence = result["evidence"].evidence
    assert any(e.skill == "Python" for e in evidence)

    # Scoring
    scorecard = result["scorecard"]
    python_score = next(s for s in scorecard.scores if s.skill == "Python")
    assert python_score.score == 5
    assert python_score.confidence > 0.9

    # Copilot
    copilot_output = result["copilot"]
    assert "SQL" in copilot_output.uncovered_skills
    assert any("SQL" in suggestion for suggestion in copilot_output.followup_suggestions)
