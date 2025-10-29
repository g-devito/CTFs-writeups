import requests

r = requests.put("http://web-10.challs.olicyber.it/")

print(r.headers)
print(r.text)
