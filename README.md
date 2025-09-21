
# Codex: Local-First Research Agent

Codex is a local-first research agent that combines high-quality retrieval, agentic reasoning, and report-grade outputs without relying on external services during production queries. This repository provides an MVP-friendly scaffolding that follows the architecture outlined in the design brief.

## Features

- Hybrid retrieval pipeline targeting Qdrant (stubbed for now) with optional compression.
- Agentic orchestration (ReAct-style) with traceable reasoning steps.
- Summarisation and report generation services backed by FastAPI.
- Configurable, on-prem deployment model via Docker Compose and YAML configs.

## Repository Layout

`
api/          FastAPI application and route handlers
agent/        Research orchestrator, prompts, and tools
codex/        Shared configuration and runtime utilities
configs/      Environment-specific YAML configuration
data/         Sample documents for ingestion tests
ingestion/    Document discovery, loaders, and pipeline stubs
infra/        Deployment and observability manifests
reporting/    Report renderer and Jinja templates
retriever/    Hybrid retrieval abstractions
tests/        Unit and integration test stubs
`

## Quickstart

1. Create and activate a Python 3.10+ environment.
2. Install dependencies:

   `ash
   pip install -e .
   `

3. Launch supporting services (development defaults use Docker Compose):

   `ash
   docker compose -f infra/docker-compose.yml up -d
   `

4. Run the API locally:

   `ash
   uvicorn api.main:app --reload
   `

5. Trigger a sample ingestion:

   `ash
   python -m ingestion.run --path data/samples/papers --config configs/dev.yaml
   `

6. Query the agent:

   `ash
   curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Compare Milvus and Qdrant for filtered search.", "trace": true}'
   `

## Configuration

Configuration is centralised in configs/. Override the CODEX_CONFIG environment variable to point to a different YAML file at runtime.

## Roadmap

- Replace Qdrant stub with real client integration.
- Connect embedding workers (FastEmbed) and persistence.
- Expand observability stack (Grafana dashboards, OpenTelemetry pipelines).
- Harden summarisation and reporting with LLM-backed synthesis.
- 
