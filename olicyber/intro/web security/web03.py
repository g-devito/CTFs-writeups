import requests

headers = {'X-Password':'admin'}
r = requests.get("http://web-03.challs.olicyber.it/flag", headers=headers)
if r.status_code == 200:
    print(r.text)
