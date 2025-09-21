from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .base import TimestampedModel


class SummarizeRequest(BaseModel):
    text: Optional[str] = Field(default=None, description='Raw text payload to summarise.')
    document_id: Optional[str] = Field(default=None, description='Ingested document identifier to summarise.')
    budget_tokens: int = Field(default=512, ge=128, le=4096, description='Token budget for the summary stage.')
    domain: Optional[str] = Field(default=None, description='Optional domain hint (e.g., legal, scientific).')

    @property
    def has_input(self) -> bool:
        return bool((self.text and self.text.strip()) or self.document_id)


class SummarizeResponse(TimestampedModel):
    summary: str
    notes: Optional[str] = None
