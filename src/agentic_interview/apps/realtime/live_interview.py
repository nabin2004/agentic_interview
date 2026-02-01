import asyncio
from typing import Callable, Optional, Set
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.agents.copilot import LiveCopilotAgent
from agentic_interview.core.schemas.transcript import Transcript, TranscriptUtterance
from agentic_interview.core.schemas.agent_io import EvidenceInput, CopilotInput, CopilotOutput
from datetime import datetime


class LiveInterviewAgent:
    """
    Real-time interview orchestrator.
    Streams candidate speech (ASR) → feeds SignalExtractionAgent and LiveCopilotAgent.
    Calls a callback with live copilot suggestions.
    """

    def __init__(
        self,
        extractor: SignalExtractionAgent,
        copilot: LiveCopilotAgent,
        update_callback: Optional[Callable[[CopilotOutput], None]] = None
    ):
        self.extractor = extractor
        self.copilot = copilot
        self.update_callback = update_callback or (lambda x: None)

        # internal transcript
        self.transcript = Transcript(utterances=[])

    async def add_utterance(self, speaker: str, text: str):
        """
        Add a new utterance to the transcript, update agents in real-time.
        """
        utterance = TranscriptUtterance(
            speaker=speaker,
            text=text,
            timestamp=datetime.utcnow()
        )
        self.transcript.utterances.append(utterance)

        # Run SignalExtractionAgent asynchronously
        evidence_input = EvidenceInput(
            transcript=self.transcript,
            interview_plan=getattr(self, "interview_plan", None)
        )
        evidence_task = asyncio.create_task(self.extractor.run(evidence_input))

        # Run LiveCopilotAgent asynchronously
        covered_skills: Set[str] = getattr(self, "covered_skills", set())
        copilot_input = CopilotInput(
            transcript=self.transcript,
            interview_plan=getattr(self, "interview_plan", None),
            covered_skills=covered_skills
        )
        copilot_task = asyncio.create_task(self.copilot.run(copilot_input))

        # Wait for copilot suggestions
        copilot_output = await copilot_task
        self.update_callback(copilot_output)

        # store or process evidence asynchronously
        _ = await evidence_task

    def set_interview_plan(self, interview_plan, covered_skills: Optional[Set[str]] = None):
        self.interview_plan = interview_plan
        self.covered_skills = covered_skills or set()

