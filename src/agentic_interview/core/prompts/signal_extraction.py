PROMPT_VERSION = "1.0.0"

SIGNAL_EXTRACTION_PROMPT = """
You are analyzing an interview transcript.

Your task:
- Extract concrete evidence related to the listed skills.
- Only use information explicitly stated in the transcript.
- If there is insufficient evidence for a skill, say so.

Output format (JSON only):
[
  {{
    "skill": "<skill name>",
    "text": "<verbatim or near-verbatim evidence>",
    "strength": "strong | weak | insufficient"
  }}
]

Skills:
{skills}

Transcript:
{transcript}
"""
