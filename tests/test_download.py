from requests.sessions import Session

url = "http://localhost:6009/download"


def test_download(client: Session):
    r = client.post(url, json={"gal_num": "1570712"})
    assert r.json() == {"status": "ok"}
    assert r.status_code == 200


def test_no_gal_num_download(client: Session):
    r = client.post(url, "http://localhost:6009/download", json={"test": "payload"})
    assert r.json() == {"error": "bad_request"}
    assert r.status_code == 400
