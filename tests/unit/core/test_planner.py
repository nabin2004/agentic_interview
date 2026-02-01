import pytest
from agentic_interview.core.agents.planner import InterviewPlannerAgent

class FakeLLM:
    async def generate(self, prompt: str) -> str:
        return """
        {
            "skills": [
                {"name": "Python", "description": "Python programming"},
                {"name": "SQL", "description": "SQL skills"}
            ],
            "questions": {
                "Python": ["Explain a Python project you've built."],
                "SQL": ["Write a SQL query to find top customers."]
            }
        }
        """

@pytest.mark.asyncio
async def test_planner_agent():
    llm = FakeLLM()
    planner = InterviewPlannerAgent(llm=llm)

    plan = await planner.run(
        job_description="Looking for a mid-level ML Engineer with Python and SQL skills",
        role="ML Engineer",
        level="mid"
    )

    assert any(skill.name == "Python" for skill in plan.skills)
    assert "SQL" in plan.questions
