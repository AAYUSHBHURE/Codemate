from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG_REL_PATH = Path('configs/dev.yaml')


@dataclass(slots=True)
class CodexConfig:
    environment: str
    embeddings: Dict[str, Any]
    vector_db: Dict[str, Any]
    llm: Dict[str, Any]
    retrieval: Dict[str, Any]
    pipeline: Dict[str, Any]
    security: Dict[str, Any]
    tracing: Dict[str, Any] | None = None
    storage: Dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CodexConfig":
        namespace = data.get('codex', data)
        return cls(
            environment=namespace.get('environment', 'dev'),
            embeddings=namespace.get('embeddings', {}),
            vector_db=namespace.get('vector_db', {}),
            llm=namespace.get('llm', {}),
            retrieval=namespace.get('retrieval', {}),
            pipeline=namespace.get('pipeline', {}),
            security=namespace.get('security', {}),
            tracing=namespace.get('tracing'),
            storage=namespace.get('storage'),
        )


def resolve_config_path(explicit_path: str | None = None) -> Path:
    if explicit_path:
        return Path(explicit_path).expanduser().resolve()
    env_path = os.getenv('CODEX_CONFIG')
    if env_path:
        return Path(env_path).expanduser().resolve()
    return (Path.cwd() / DEFAULT_CONFIG_REL_PATH).resolve()


def load_config(explicit_path: str | None = None) -> CodexConfig:
    config_path = resolve_config_path(explicit_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open('r', encoding='utf-8') as handle:
        raw = yaml.safe_load(handle) or {}
    return CodexConfig.from_dict(raw)
