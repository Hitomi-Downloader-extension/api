import requests
import time

for _ in range(1, 6):
    try:
        r = requests.get("http://localhost:6009/ping")
        if r.status_code == 200:
            print("OK")
            break
        time.sleep(_)
    except:
        pass
