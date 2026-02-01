import asyncio
from agentic_interview.core.agents.evidence import SignalExtractionAgent
from agentic_interview.core.agents.copilot import LiveCopilotAgent
from agentic_interview.apps.realtime.live_interview import LiveInterviewAgent
from agentic_interview.core.schemas.interview import InterviewPlan, Skill

class FakeLLM:
    async def generate(self, prompt: str) -> str:
        return """
        [
            {
                "skill": "Python",
                "text": "Candidate mentions Python projects",
                "strength": "strong"
            }
        ]
        """

async def main():
    llm = FakeLLM()

    # Initialize agents
    signal_agent = SignalExtractionAgent(llm=llm)
    copilot_agent = LiveCopilotAgent(llm=llm)

    # Initialize live interview agent
    def print_suggestions(copilot_output):
        print("Live Copilot Suggestions:", copilot_output.followup_suggestions)
        print("Uncovered Skills:", copilot_output.uncovered_skills)
        print("-" * 50)

    live_agent = LiveInterviewAgent(
        extractor=signal_agent,
        copilot=copilot_agent,
        update_callback=print_suggestions
    )

    # Define interview plan
    interview_plan = InterviewPlan(
        role="ML Engineer",
        level="mid",
        skills=[
            Skill(name="Python", description="Python programming"),
            Skill(name="SQL", description="SQL skills")
        ],
        questions={}
    )

    live_agent.set_interview_plan(interview_plan, covered_skills={"Python"})

    # Simulate a conversation
    utterances = [
        ("candidate", "I built data pipelines using Python and Pandas"),
        ("recruiter", "Great! Can you explain your SQL experience?"),
        ("candidate", "I used SQL to query databases and generate reports"),
        ("recruiter", "Nice, any experience with large datasets?")
    ]

    for speaker, text in utterances:
        await live_agent.add_utterance(speaker=speaker, text=text)
        await asyncio.sleep(0.5)  

asyncio.run(main())
