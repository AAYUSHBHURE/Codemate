from __future__ import annotations

import argparse
from pathlib import Path
import sys

from codex.context import get_app_context
from ingestion.pipeline import IngestionService


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Run Codex ingestion pipeline.')
    parser.add_argument('--path', type=Path, default=Path('./data/samples/papers'), help='Target directory to ingest.')
    parser.add_argument('--config', type=str, default=None, help='Optional override config path.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.path.expanduser().resolve()
    if not source.exists():
        print(f'Path not found: {source}', file=sys.stderr)
        sys.exit(1)

    context = get_app_context(args.config)
    service = IngestionService(context.config)
    documents = service.run(source)
    print(f'Discovered {len(documents)} documents under {source}')


if __name__ == '__main__':
    main()
