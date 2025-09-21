from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(slots=True)
class RetrievalHit:
    document_id: str
    score: float
    text: str
    metadata: Dict[str, Any]
