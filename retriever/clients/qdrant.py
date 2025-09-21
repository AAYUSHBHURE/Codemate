from __future__ import annotations

import logging
from typing import Any, Dict, Iterable, List

from .utils import format_filters
from ..types import RetrievalHit

logger = logging.getLogger(__name__)


class QdrantClientStub:
    """Lightweight stand-in for the Qdrant client until integration."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def search(self, query: str, filters: Dict[str, Any] | None, limit: int) -> List[RetrievalHit]:
        logger.debug('Stub search: q=%s filters=%s limit=%d', query, filters, limit)
        payload = format_filters(filters) if filters else {}
        return [
            RetrievalHit(
                document_id='stub-doc-1',
                score=0.42,
                text=f'Stubbed result for: {query}',
                metadata={'source': 'stub', 'filters': payload},
            )
        ]

    def hybrid_search(self, query: str, filters: Dict[str, Any] | None, limit: int) -> List[RetrievalHit]:
        return self.search(query, filters, limit)


__all__ = ['QdrantClientStub']
