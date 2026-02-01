from pydantic import BaseModel
from typing import Literal
from datetime import datetime


class TranscriptUtterance(BaseModel):
    speaker: Literal["candidate", "recruiter"]
    text: str
    timestamp: datetime


class Transcript(BaseModel):
    utterances: list[TranscriptUtterance]
