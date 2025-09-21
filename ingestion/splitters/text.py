from __future__ import annotations

from typing import List


def split_text(content: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    if chunk_size <= overlap:
        raise ValueError('chunk_size must be greater than overlap')
    chunks: List[str] = []
    start = 0
    while start < len(content):
        end = min(start + chunk_size, len(content))
        chunks.append(content[start:end])
        start = end - overlap
        if start < 0:
            start = 0
        if start >= len(content):
            break
    return chunks
