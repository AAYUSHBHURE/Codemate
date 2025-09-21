from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ..dependencies import get_context
from ..schemas import SummarizeRequest, SummarizeResponse
from agent.tools.summarizer import Summarizer, SummarizerError
from codex.context import AppContext

router = APIRouter(prefix='/summarize', tags=['summaries'])


@router.post('/', response_model=SummarizeResponse)
async def summarize(payload: SummarizeRequest, context: AppContext = Depends(get_context)) -> SummarizeResponse:
    summarizer = Summarizer(context=context)
    try:
        return await summarizer.summarize(payload)
    except SummarizerError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
