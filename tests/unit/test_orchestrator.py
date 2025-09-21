from __future__ import annotations

from agent.orchestrator import ResearchOrchestrator
from api.schemas import QueryRequest
from codex.context import get_app_context


def test_orchestrator_returns_answer() -> None:
    context = get_app_context()
    orchestrator = ResearchOrchestrator(context=context)
    request = QueryRequest(query='Test query', trace=True)
    response = asyncio_run(orchestrator.run_query(request))
    assert response.answer.startswith('Query: Test query')
    assert response.citations
    assert response.used_docs
    assert response.trace is not None


def asyncio_run(coro):
    import asyncio

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)
