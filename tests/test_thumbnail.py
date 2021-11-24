from requests.sessions import Session


def test_thumbnail(client: Session):
    r = client.get("http://localhost:6009/thumbnail")
    assert r.json() == {"status": "not_found"}
    assert r.status_code == 404
