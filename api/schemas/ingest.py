from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .base import TimestampedModel


class IngestRequest(BaseModel):
    path: Optional[str] = Field(default=None, description='Filesystem path to ingest.')
    run_id: Optional[str] = Field(default=None, description='Client provided run identifier.')
    metadata: Optional[Dict[str, Any]] = Field(default=None, description='Arbitrary metadata attached to the run.')


class IngestResponse(TimestampedModel):
    run_id: str
    status: str
    details: Optional[str] = None
