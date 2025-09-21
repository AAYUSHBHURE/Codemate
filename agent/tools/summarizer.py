from __future__ import annotations

import asyncio
from pathlib import Path

from codex.context import AppContext
from api.schemas import SummarizeRequest, SummarizeResponse


class SummarizerError(RuntimeError):
    pass


class Summarizer:
    def __init__(self, context: AppContext):
        self.context = context

    async def summarize(self, request: SummarizeRequest) -> SummarizeResponse:
        if not request.has_input:
            raise SummarizerError('Either text or document_id must be provided.')

        text = await self._resolve_text(request)
        condensed = self._truncate(text, request.budget_tokens)
        notes = None
        if len(text) > len(condensed):
            notes = 'Summary truncated to comply with token budget.'
        return SummarizeResponse(summary=condensed, notes=notes)

    async def _resolve_text(self, request: SummarizeRequest) -> str:
        if request.text:
            return request.text
        return await asyncio.to_thread(self._read_document, request.document_id)

    @staticmethod
    def _read_document(document_id: str | None) -> str:
        if not document_id:
            raise SummarizerError('Missing document identifier.')
        path = Path(document_id).expanduser().resolve()
        if not path.exists():
            raise SummarizerError(f'Document not found: {path}')
        return path.read_text(encoding='utf-8')

    @staticmethod
    def _truncate(text: str, budget_tokens: int) -> str:
        # Basic heuristic: assume 4 characters per token.
        target_chars = budget_tokens * 4
        if len(text) <= target_chars:
            return text
        return text[:target_chars].rsplit(' ', 1)[0] + '...'
