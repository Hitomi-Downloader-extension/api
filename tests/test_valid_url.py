from requests.sessions import Session

url = "http://localhost:6009/valid_url"


def test_valid_url(client: Session):
    r = client.post(url, json={"gal_num": "1"})
    assert r.json() == {"type": ["hitomi"]}
    assert r.status_code == 200


def test_not_valid_url(client: Session):
    r = client.post(url, json={"gal_num": "https://example.com"})
    assert r.json() == {"error": "not_valied"}
    assert r.status_code == 400


def test_no_gal_num_valid_url(client: Session):
    r = client.post(url, json={"test": "payload"})
    assert r.json() == {"error": "bad_request"}
    assert r.status_code == 400
