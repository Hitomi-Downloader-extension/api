from requests.sessions import Session


def test_ping(client: Session):
    response = client.get("http://localhost:6009/ping")
    assert response.json() == {"status": "ok"}
