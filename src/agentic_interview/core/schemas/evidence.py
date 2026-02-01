from pydantic import BaseModel
from typing import Literal


class EvidenceSnippet(BaseModel):
    skill: str
    text: str
    strength: Literal["strong", "weak", "insufficient"]
