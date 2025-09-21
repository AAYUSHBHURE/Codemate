from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .clients.qdrant import QdrantClientStub
from .types import RetrievalHit

logger = logging.getLogger(__name__)


class HybridRetriever:
    def __init__(self, client: QdrantClientStub, default_k: int = 10):
        self.client = client
        self.default_k = default_k

    def retrieve(self, query: str, filters: Optional[Dict[str, object]] = None, k: Optional[int] = None) -> List[RetrievalHit]:
        limit = k or self.default_k
        logger.debug('Hybrid retriever call q=%s limit=%d filters=%s', query, limit, filters)
        return self.client.hybrid_search(query=query, filters=filters or {}, limit=limit)
