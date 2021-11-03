import requests
import time


t = 0
while True:
    t += 1
    try:
        r = requests.get("http://localhost:6009/ping")
        if r.status_code == 200:
            print("OK")
            break
    except:
        print(f"No response. try again after {t} second")
        time.sleep(t)
