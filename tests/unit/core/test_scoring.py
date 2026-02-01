import pytest
from datetime import datetime

from agentic_interview.core.agents.scoring import ScoringAgent
from agentic_interview.core.schemas.agent_io import ScoringInput
from agentic_interview.core.schemas.evidence import EvidenceSnippet


class FakeLLM:
    async def generate(self, prompt: str) -> str:
        return ""


@pytest.mark.asyncio
async def test_scoring_agent_basic():
    agent = ScoringAgent(llm=FakeLLM())

    evidence = [
        EvidenceSnippet(
            skill="Python",
            text="I built pipelines using Python",
            strength="strong"
        ),
        EvidenceSnippet(
            skill="SQL",
            text="Some experience with SQL",
            strength="weak"
        ),
        EvidenceSnippet(
            skill="ML",
            text="",
            strength="insufficient"
        ),
    ]

    input_data = ScoringInput(evidence=evidence)
    result = await agent.run(input_data)

    scores = result.scorecard.scores
    assert scores[0].skill == "Python"
    assert scores[0].score == 5
    assert scores[1].score == 3
    assert scores[2].score is None

    assert result.scorecard.overall_recommendation == "advance"
