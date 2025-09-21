from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ..schemas import ReportRequest, ReportResponse
from reporting.renderer import ReportRenderer

router = APIRouter(prefix='/report', tags=['reporting'])


@router.post('/', response_model=ReportResponse)
async def create_report(payload: ReportRequest) -> ReportResponse:
    if payload.format not in {'md', 'html', 'pdf'}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Unsupported format.')
    renderer = ReportRenderer()
    return renderer.render(payload)
