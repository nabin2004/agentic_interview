import json
from pydantic import ValidationError
from typing import Optional

from agentic_interview.core.schemas.agent_io import ScoringInput, ScoringOutput
from agentic_interview.core.schemas.scoring import SkillScore, InterviewScorecard
from agentic_interview.core.schemas.evidence import EvidenceSnippet
from agentic_interview.ml.llm.base import LLMClient


class ScoringAgent:
    """Converts evidence snippets into structured skill scores."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def run(self, data: ScoringInput) -> ScoringOutput:
        """
        Args:
            data: EvidenceOutput from SignalExtractionAgent
        Returns:
            ScoringOutput with structured InterviewScorecard
        """
        evidence = data.evidence
        skill_scores = []

        # Build a JSON input for the LLM or use deterministic mapping
        # For now, I have mapped a simple rules for initial phase
        for snippet in evidence:
            score = None
            confidence = 0.0
            if snippet.strength == "strong":
                score = 5
                confidence = 0.95
            elif snippet.strength == "weak":
                score = 3
                confidence = 0.6
            elif snippet.strength == "insufficient":
                score = None
                confidence = 0.0

            rationale = snippet.text if snippet.text else "No evidence"
            skill_scores.append(
                SkillScore(
                    skill=snippet.skill,
                    score=score,
                    confidence=confidence,
                    rationale=rationale,
                )
            )

        # Simple overall recommendation
        avg_score = (
            sum(s.score for s in skill_scores if s.score is not None) /
            max(1, sum(1 for s in skill_scores if s.score is not None))
        )

        if avg_score >= 4:
            overall = "advance"
        elif avg_score >= 2:
            overall = "hold"
        else:
            overall = "no_decision"

        return ScoringOutput(
            scorecard=InterviewScorecard(
                scores=skill_scores,
                overall_recommendation=overall,
            )
        )
