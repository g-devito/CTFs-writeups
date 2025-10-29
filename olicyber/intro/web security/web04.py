import requests

headers = {'Accept':'application/xml'}
r = requests.get("http://web-04.challs.olicyber.it/users", headers=headers)
if r.status_code == 200:
    print(r.text)
