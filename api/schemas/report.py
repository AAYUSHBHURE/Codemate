from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from .base import Citation, TimestampedModel


class ReportSection(BaseModel):
    title: str
    content: str


class ReportRequest(BaseModel):
    summary: str
    key_findings: List[str] = Field(default_factory=list)
    qa_pairs: List[dict] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)
    format: str = Field(default='md', pattern='^(md|html|pdf)$')


class ReportResponse(TimestampedModel):
    content: str
    format: str
    filename: str
    warnings: Optional[List[str]] = None
