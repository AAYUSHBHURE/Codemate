from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_health_endpoint() -> None:
    client = TestClient(create_app())
    response = client.get('/health/')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'
