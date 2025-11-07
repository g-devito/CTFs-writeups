import requests

payload = {'id':'flag'}
r = requests.get("http://web-02.challs.olicyber.it/server-records", params=payload)
if r.status_code == 200:
    print(r.text)
