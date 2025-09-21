from __future__ import annotations

import logging

from fastapi import FastAPI

from codex.context import get_app_context
from codex.logging import setup_logging

from .routes import health, ingest, query, report, summarize

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(
        title='Codex Research Agent',
        version='0.1.0',
        description='Local-first RAG + agentic research service.',
    )
    app.state.context = get_app_context()

    app.include_router(health.router)
    app.include_router(query.router)
    app.include_router(ingest.router)
    app.include_router(summarize.router)
    app.include_router(report.router)

    @app.on_event('startup')
    async def _startup() -> None:
        logger.info('Codex API initialised for %s environment', app.state.context.config.environment)

    return app


app = create_app()
