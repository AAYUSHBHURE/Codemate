from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TraceStep(BaseModel):
    thought: str
    action: Optional[str] = None
    observation: Optional[str] = None


class Citation(BaseModel):
    source_id: str
    page: Optional[str] = None
    snippet: Optional[str] = None


class DocumentHit(BaseModel):
    document_id: str
    source: str
    score: float
    metadata: Optional[Dict[str, Any]] = None


class TimestampedModel(BaseModel):
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
