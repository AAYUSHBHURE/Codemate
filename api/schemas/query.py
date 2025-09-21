from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .base import Citation, DocumentHit, TimestampedModel, TraceStep


class QueryRequest(BaseModel):
    query: str = Field(..., description='Natural language prompt for the research agent.')
    filters: Optional[Dict[str, Any]] = Field(default=None, description='Metadata filters forwarded to retrieval.')
    k: int = Field(default=10, ge=1, le=32, description='Number of child chunks to retrieve.')
    trace: bool = Field(default=False, description='Include intermediate reasoning trace when true.')


class QueryResponse(TimestampedModel):
    answer: str
    citations: list[Citation]
    trace: Optional[list[TraceStep]] = None
    used_docs: Optional[list[DocumentHit]] = None
