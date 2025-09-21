from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from codex.config import CodexConfig

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredDocument:
    path: Path
    media_type: str


class IngestionService:
    def __init__(self, config: CodexConfig):
        self.config = config

    def run(self, source_path: Path) -> List[DiscoveredDocument]:
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        if source_path.is_file():
            source_path = source_path.parent

        documents = list(self._discover_documents(source_path))
        if not documents:
            logger.warning('No documents found under %s', source_path)
            return []
        logger.info('Discovered %d documents for ingestion', len(documents))
        return documents

    def _discover_documents(self, source_path: Path) -> Iterable[DiscoveredDocument]:
        for path in source_path.rglob('*'):
            if not path.is_file():
                continue
            media_type = self._infer_media_type(path)
            yield DiscoveredDocument(path=path, media_type=media_type)

    @staticmethod
    def _infer_media_type(path: Path) -> str:
        suffix = path.suffix.lower()
        mapping = {
            '.pdf': 'application/pdf',
            '.md': 'text/markdown',
            '.txt': 'text/plain',
            '.html': 'text/html',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        }
        return mapping.get(suffix, 'application/octet-stream')


def ensure_run_id(value: str | None) -> str:
    return value or uuid.uuid4().hex
