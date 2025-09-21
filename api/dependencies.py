from __future__ import annotations

from fastapi import Depends

from agent.orchestrator import ResearchOrchestrator
from codex.context import AppContext, get_app_context


def get_context() -> AppContext:
    return get_app_context()


def get_orchestrator(context: AppContext = Depends(get_context)) -> ResearchOrchestrator:
    return ResearchOrchestrator(context=context)
