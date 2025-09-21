from __future__ import annotations

from pathlib import Path


def load_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')
