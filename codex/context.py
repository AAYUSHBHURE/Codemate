from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from .config import CodexConfig, load_config


@dataclass(slots=True)
class AppContext:
    config: CodexConfig


@lru_cache(maxsize=1)
def get_app_context(config_path: Optional[str] = None) -> AppContext:
    config = load_config(config_path)
    return AppContext(config=config)
