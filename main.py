import asyncio
from agentic_interview.core.orchestration.interview_flow import InterviewFlow
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.agents.scoring import ScoringAgent
from agentic_interview.core.agents.copilot import LiveCopilotAgent
from agentic_interview.ml.llm.base import LLMClient
from agentic_interview.core.schemas.interview import InterviewPlan, Skill
from agentic_interview.core.schemas.transcript import Transcript, TranscriptUtterance
from agentic_interview.core.schemas.agent_io import EvidenceInput

class FakeLLM(LLMClient):
    async def generate(self, prompt: str) -> str:
        return ""  

async def main():
    llm = FakeLLM()
    extractor = SignalExtractionAgent(llm)
    scorer = ScoringAgent(llm)
    copilot = LiveCopilotAgent(llm)

    flow = InterviewFlow(
        planner=None,
        extractor=extractor,
        scorer=scorer,
        copilot=copilot
    )

    plan = InterviewPlan(
        role="ML Engineer",
        level="mid",
        skills=[Skill(name="Python", description="Python skills")],
        questions={}
    )

    transcript = Transcript(
        utterances=[
            TranscriptUtterance(speaker="candidate", text="I built pipelines in Python", timestamp="2026-02-01T12:00:00")
        ]
    )

    evidence_input = EvidenceInput(transcript=transcript, interview_plan=plan)
    result = await flow.run(evidence_input, transcript_input=evidence_input, covered_skills={"Python"})

    print(result)

asyncio.run(main())
