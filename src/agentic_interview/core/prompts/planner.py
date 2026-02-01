PROMPT_VERSION="1.0.0"

INTERVIEW_PLAN_PROMPT = """
Generate a structured interview plan for a {role} ({level}) 
from the following job description:
{job_description}

Provide:
- List of skills with names and descriptions
- Suggested interview questions for each skill
Output as JSON:
{{
    "skills": [
        {{"name": "...", "description": "..."}}
    ],
    "questions": {{
        "skill_name": ["question1", "question2"]
    }}
}}
"""
