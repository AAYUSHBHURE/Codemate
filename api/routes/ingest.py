from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool

from ..dependencies import get_context
from ..schemas import IngestRequest, IngestResponse
from codex.context import AppContext
from ingestion.pipeline import IngestionService, ensure_run_id

router = APIRouter(prefix='/ingest', tags=['ingestion'])


@router.post('/', response_model=IngestResponse)
async def ingest_documents(payload: IngestRequest, context: AppContext = Depends(get_context)) -> IngestResponse:
    target_path = _resolve_path(payload, context)
    if not target_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Path not found: {target_path}')

    service = IngestionService(config=context.config)
    run_id = ensure_run_id(payload.run_id)

    documents = await run_in_threadpool(service.run, target_path)
    details = f'Discovered {len(documents)} documents under {target_path}'
    return IngestResponse(run_id=run_id, status='completed', details=details)


def _resolve_path(payload: IngestRequest, context: AppContext) -> Path:
    if payload.path:
        return Path(payload.path).expanduser().resolve()
    storage_cfg = context.config.storage or {}
    base_path = storage_cfg.get('data_root', './data')
    return Path(base_path).expanduser().resolve()
