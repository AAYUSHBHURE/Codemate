from __future__ import annotations

from typing import Any, Dict


def format_filters(filters: Dict[str, Any]) -> Dict[str, Any]:
    if not filters:
        return {}
    formatted: Dict[str, Any] = {}
    for key, value in filters.items():
        if value is None:
            continue
        formatted[key] = value
    return formatted
