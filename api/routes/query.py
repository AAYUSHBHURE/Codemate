from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_orchestrator
from ..schemas import QueryRequest, QueryResponse
from agent.orchestrator import ResearchOrchestratorError

router = APIRouter(prefix='/query', tags=['query'])


@router.post('/', response_model=QueryResponse)
async def run_query(payload: QueryRequest, orchestrator: ResearchOrchestrator = Depends(get_orchestrator)) -> QueryResponse:
    try:
        return await orchestrator.run_query(payload)
    except ResearchOrchestratorError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
