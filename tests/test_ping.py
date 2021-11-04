from requests.sessions import Session


def test_ping(client: Session):
    r = client.get("http://localhost:6009/ping")
    assert r.json() == {"status": "ok"}
    assert r.status_code == 200
