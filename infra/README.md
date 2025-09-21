# Infrastructure Notes

- docker-compose.yml provisions Qdrant, Ollama, the Codex API, and Grafana for observability.
- Mounts the repository into the API service for rapid iteration.
- Persistent data volumes stored under ../data for vector indexes and model weights.
- Extend with Prometheus and OpenTelemetry collectors as production requirements grow.
