from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class BaseSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        frozen = True
