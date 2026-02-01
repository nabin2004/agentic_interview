from typing import Optional
from agentic_interview.core.agents.planner import InterviewPlannerAgent
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.agents.scoring import ScoringAgent
from agentic_interview.core.agents.copilot import LiveCopilotAgent
from agentic_interview.core.schemas.agent_io import (
    PlannerInput, PlannerOutput,
    EvidenceInput, EvidenceOutput,
    ScoringInput, ScoringOutput,
    CopilotInput, CopilotOutput
)


class InterviewFlow:
    """
    Orchestrates the end-to-end interview pipeline:
    Planner -> SignalExtraction -> Scoring -> LiveCopilot
    """

    def __init__(
        self,
        planner: Optional[InterviewPlannerAgent],
        extractor: SignalExtractionAgent,
        scorer: ScoringAgent,
        copilot: LiveCopilotAgent
    ):
        self.planner = planner
        self.extractor = extractor
        self.scorer = scorer
        self.copilot = copilot

    async def run(
        self,
        planner_input: PlannerInput,
        transcript_input: Optional[EvidenceInput] = None,
        covered_skills: Optional[set[str]] = None
    ):
        # Step 1: Generate interview plan if planner exists
        if self.planner:
            plan_output: PlannerOutput = await self.planner.run(planner_input)
            interview_plan = plan_output.interview_plan
        else:
            # If no planner, must provide interview_plan in transcript_input
            if transcript_input is None:
                raise ValueError("Either planner or transcript_input must be provided.")
            interview_plan = transcript_input.interview_plan

        # Step 2: Extract evidence from transcript
        if transcript_input is None:
            raise ValueError("transcript_input is required for running extraction")
        evidence_output: EvidenceOutput = await self.extractor.run(transcript_input)

        # Step 3: Score evidence
        scoring_input = ScoringInput(evidence=evidence_output.evidence)
        scoring_output: ScoringOutput = await self.scorer.run(scoring_input)

        # Step 4: Generate live copilot suggestions
        copilot_input = CopilotInput(
            transcript=transcript_input.transcript,
            interview_plan=interview_plan,
            covered_skills=covered_skills or set()
        )
        copilot_output: CopilotOutput = await self.copilot.run(copilot_input)

        return {
            "evidence": evidence_output,
            "scorecard": scoring_output.scorecard,
            "copilot": copilot_output
        }
