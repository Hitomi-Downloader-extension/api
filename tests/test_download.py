def test_download(client):
    r = client.post("http://localhost:6009/download", json={"gal_num": "1570712"})
    assert r.json == {"status":"ok"}
