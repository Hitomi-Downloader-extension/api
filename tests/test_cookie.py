from requests.sessions import Session

url = "http://localhost:6009/cookie"


def test_cookie(client: Session):
    r = client.post(
        url,
        json={
            "cookies": [
                {"name": "value", "value": "value", "domain": "value", "expires": 0}
            ]
        },
    )
    assert r.json() == {"status": "ok"}
    assert r.status_code == 200


def test_no_cookies_cookie(client: Session):
    r = client.post(url, json={"test": "payload"})
    assert r.json() == {"error": "bad_request"}
    assert r.status_code == 400


def test_no_domain(client: Session):
    r = client.post(
        url,
        json={"cookies": [{"name": "value", "value": "value", "expires": 0}]},
    )
    assert r.json() == {"error": "['domain', 'name', 'value'] is required arguments"}
    assert r.status_code == 400


def test_no_name(client: Session):
    r = client.post(
        url,
        json={"cookies": [{"value": "value", "domain": "value", "expires": 0}]},
    )
    assert r.json() == {"error": "['domain', 'name', 'value'] is required arguments"}
    assert r.status_code == 400


def test_no_value(client: Session):
    r = client.post(
        url,
        json={"cookies": [{"name": "value", "domain": "value", "expires": 0}]},
    )
    assert r.json() == {"error": "['domain', 'name', 'value'] is required arguments"}
    assert r.status_code == 400
