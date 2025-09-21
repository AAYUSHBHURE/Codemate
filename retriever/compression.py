from __future__ import annotations

from typing import Iterable, List

from .types import RetrievalHit


def simple_compression(hits: Iterable[RetrievalHit], max_chars: int = 1200) -> List[RetrievalHit]:
    compressed: List[RetrievalHit] = []
    for hit in hits:
        text = hit.text
        if len(text) > max_chars:
            text = text[:max_chars].rsplit(' ', 1)[0] + '...'
        compressed.append(RetrievalHit(document_id=hit.document_id, score=hit.score, text=text, metadata=hit.metadata))
    return compressed
