# Codex Architecture

Codex is designed to operate as a self-contained research agent that can ingest heterogeneous, evolving corpora and answer grounded questions without leaving the premises.

## Goals

- Local-first and offline-friendly: no production dependency on external APIs.
- High-quality retrieval with semantic + lexical hybrid search.
- Transparent agentic reasoning (ReAct) with traceable tool invocations.
- Report-grade outputs (Markdown, HTML, PDF) suitable for audit trails.

## System Overview

`
Raw Sources --? Ingestion --? Vector Store --? Hybrid Retrieval --? ReAct Agent --? Reporting
`

- **Ingestion**: batch/delta orchestrations (Airflow/Prefect ready) that load, split, embed, and store content.
- **Vector Store**: Qdrant (HNSW, payload filters, hybrid search). Stubbed client included for development.
- **Agent**: ReAct loop running on local LLMs (llama.cpp / Mixtral / Llama 3). Provides trace outputs.
- **Reporting**: Jinja2 templates rendered to Markdown/HTML with optional PDF conversion (WeasyPrint planned).
- **API/UI**: FastAPI backend powering chat, CLI, and REST surfaces.

## Key Components

### Embeddings

- Primary model: BAAI/bge-base-en-v1.5 served via FastEmbed (ONNX Runtime).
- Configurable alternatives defined in configs/.

### Retrieval

- Hybrid KNN (semantic) + BM25 style lexical filters.
- Optional contextual compression prior to prompt assembly.
- Re-ranker placeholder ready for LLM or cross-encoder integration.

### Reasoning

- ReAct format with deterministic tool whitelist (ector_search, hybrid_search, summarize).
- Structured trace returned alongside answers when requested.

### Reporting

- Templates in eporting/templates/ covering Markdown and HTML defaults.
- PDF export planned via WeasyPrint (currently returns HTML with warning).

### Observability & Ops

- Prometheus/Grafana stack scaffolding in infra/.
- Configurable metrics/tracing exporters via YAML.
- Index hygiene and rollout guidelines summarised in docs/operations.md (forthcoming).

## Roadmap Snapshot

1. **MVP hardening**: Real Qdrant + FastEmbed integration, ingestion workers, minimal UI.
2. **Production readiness**: RBAC, mTLS, golden-set evaluation harness, multi-node scale-out.
3. **Explainability**: Extended traces, memory, and enriched reporting exports.

Refer to the design brief for a comprehensive breakdown of phases, testing strategy, and threat model.
