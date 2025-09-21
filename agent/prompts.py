from __future__ import annotations

from textwrap import dedent

DEFAULT_SYSTEM_PROMPT = dedent(
    """
    You are Codex, a local-first research assistant. Answer using the provided context.
    Cite sources using their identifiers. If the context is insufficient, state that clearly.
    """
)


def build_system_prompt(extra_instructions: str | None = None) -> str:
    if not extra_instructions:
        return DEFAULT_SYSTEM_PROMPT
    return f"{DEFAULT_SYSTEM_PROMPT}\n\n{extra_instructions.strip()}"
