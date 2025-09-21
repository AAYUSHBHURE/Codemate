from __future__ import annotations

from typing import Iterable, List

from ..types import RetrievalHit


class HeuristicReranker:
    """Simple reranker placeholder that keeps the original order."""

    def rerank(self, hits: Iterable[RetrievalHit]) -> List[RetrievalHit]:
        return list(hits)
