import json
from agentic_interview.core.schemas.agent_io import EvidenceInput, EvidenceOutput
from agentic_interview.core.schemas.evidence import EvidenceSnippet
from agentic_interview.core.prompts.signal_extraction import SIGNAL_EXTRACTION_PROMPT
from agentic_interview.ml.llm.base import LLMClient
from pydantic import ValidationError


class SignalExtractionAgent:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def run(self, data: EvidenceInput) -> EvidenceOutput:
        skills = [skill.name for skill in data.interview_plan.skills]

        transcript_text = "\n".join(
            f"{u.speaker}: {u.text}" for u in data.transcript.utterances
        )

        prompt = SIGNAL_EXTRACTION_PROMPT.format(
            skills=", ".join(skills),
            transcript=transcript_text,
        )

        raw_output = await self.llm.generate(prompt)

        try:
            parsed = json.loads(raw_output)
            evidence = [EvidenceSnippet(**item) for item in parsed]
        except (json.JSONDecodeError, ValidationError) as e:
            # Fail safe: no hallucinated evidence
            evidence = [
                EvidenceSnippet(
                    skill=skill,
                    text="No reliable evidence extracted.",
                    strength="insufficient",
                )
                for skill in skills
            ]

        return EvidenceOutput(evidence=evidence)
