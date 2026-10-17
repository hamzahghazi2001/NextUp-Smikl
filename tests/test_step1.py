
from fastapi.testclient import TestClient

from nextup.main import app

client = TestClient(app)


def test_health_says_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_is_not_a_page():
    response = client.get("/")
    assert response.status_code == 404