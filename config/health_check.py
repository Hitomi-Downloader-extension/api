import requests

for _ in range(5):
    try:
        r = requests.get("http://localhost:6009/ping")
        if r.status_code == 200:
            print("OK")
            break
    except:
        pass
