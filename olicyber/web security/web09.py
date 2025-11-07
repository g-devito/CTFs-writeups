import requests

headers = {"Content-type":"application/json"}
data = {"username":"admin","password":"admin"}

r = requests.post("http://web-09.challs.olicyber.it/login", json=data, headers=headers)

print(r.text)
