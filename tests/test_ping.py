def test_ping(client):
    response = client.get("http://localhost:6009/ping")
    assert response.status_code == 200
