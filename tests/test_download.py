def test_download(client):
    r = client.post("http://localhost:6009/download", json={"gal_num": "1570712"})
    assert r.json() == {"status":"ok"}

det test_no_gal_num_download(client):
    r = client.post("http://localhost:6009/download", json={"test": "payload"})
    assert r.json() == {"error":"bad_request"}
