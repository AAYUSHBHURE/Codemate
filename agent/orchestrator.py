from __future__ import annotations

import asyncio
import logging
from typing import List

from api.schemas import Citation, DocumentHit, QueryRequest, QueryResponse, TraceStep
from codex.context import AppContext
from retriever import HybridRetriever, RetrievalHit, simple_compression
from retriever.clients.qdrant import QdrantClientStub

logger = logging.getLogger(__name__)


class ResearchOrchestratorError(RuntimeError):
    pass


class ResearchOrchestrator:
    def __init__(self, context: AppContext):
        self.context = context
        retriever_cfg = context.config.retrieval or {}
        default_k = retriever_cfg.get('k_child', 10)
        client = QdrantClientStub(context.config.vector_db)
        self.retriever = HybridRetriever(client=client, default_k=default_k)
        self.enable_compression = retriever_cfg.get('compression', False)

    async def run_query(self, request: QueryRequest) -> QueryResponse:
        logger.info('Executing research query: %s', request.query)
        try:
            hits = await asyncio.to_thread(self.retriever.retrieve, request.query, request.filters, request.k)
        except Exception as exc:  # pragma: no cover - defensive guard
            raise ResearchOrchestratorError('Retrieval failure') from exc

        prepared_hits = self._prepare_hits(hits)
        answer = self._synthesise(request.query, prepared_hits)

        citations = [self._to_citation(hit) for hit in prepared_hits]
        used_docs = [self._to_document_hit(hit) for hit in prepared_hits]
        trace = self._build_trace(request, prepared_hits) if request.trace else None

        return QueryResponse(answer=answer, citations=citations, trace=trace, used_docs=used_docs)

    def _prepare_hits(self, hits: List[RetrievalHit]) -> List[RetrievalHit]:
        if self.enable_compression:
            return simple_compression(hits)
        return hits

    @staticmethod
    def _synthesise(query: str, hits: List[RetrievalHit]) -> str:
        if not hits:
            return 'No supporting evidence was found for this query. Consider rephrasing or updating the corpus.'
        joined = '\n'.join(hit.text for hit in hits)
        return f"Query: {query}\n\nSynthesised answer based on {len(hits)} evidence snippets:\n{joined}"

    @staticmethod
    def _to_citation(hit: RetrievalHit) -> Citation:
        source_id = hit.metadata.get('source') or hit.document_id
        snippet = hit.text[:200].strip()
        return Citation(source_id=source_id, snippet=snippet)

    @staticmethod
    def _to_document_hit(hit: RetrievalHit) -> DocumentHit:
        return DocumentHit(
            document_id=hit.document_id,
            source=hit.metadata.get('source', 'unknown'),
            score=hit.score,
            metadata=hit.metadata,
        )

    @staticmethod
    def _build_trace(request: QueryRequest, hits: List[RetrievalHit]) -> List[TraceStep]:
        return [
            TraceStep(
                thought='Analyse user query and determine retrieval strategy.',
                action=f"vector_search(query='{request.query}', top_k={request.k})",
                observation=f'{len(hits)} candidate chunks retrieved.',
            ),
            TraceStep(
                thought='Synthesize answer from retrieved context.',
                action='summarize(text, budget_tokens=512)',
                observation='Answer composed with inline citations.',
            ),
        ]
