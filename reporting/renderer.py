from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape

from api.schemas import ReportRequest, ReportResponse


class ReportRenderer:
    def __init__(self, template_dir: Path | None = None):
        self.template_dir = template_dir or Path(__file__).resolve().parent / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, payload: ReportRequest) -> ReportResponse:
        template_name = self._template_for_format(payload.format)
        template = self.env.get_template(template_name)
        content = template.render(
            summary=payload.summary,
            key_findings=payload.key_findings,
            qa_pairs=payload.qa_pairs,
            citations=payload.citations,
            generated_at=dt.datetime.utcnow().isoformat(),
        )
        warnings: List[str] = []
        if payload.format == 'pdf':
            warnings.append('PDF rendering not implemented; returning HTML content instead.')
        filename = self._filename(payload.format)
        return ReportResponse(content=content, format=payload.format, filename=filename, warnings=warnings or None)

    @staticmethod
    def _template_for_format(fmt: str) -> str:
        mapping = {
            'md': 'report.md.j2',
            'html': 'report.html.j2',
            'pdf': 'report.html.j2',
        }
        return mapping[fmt]

    @staticmethod
    def _filename(fmt: str) -> str:
        timestamp = dt.datetime.utcnow().strftime('%Y%m%d-%H%M%S')
        extension = 'pdf' if fmt == 'pdf' else fmt
        return f'codex-report-{timestamp}.{extension}'
