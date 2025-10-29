import requests
from bs4 import BeautifulSoup

r = requests.get("http://web-13.challs.olicyber.it")
print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')

for c in soup.find_all('span', class_="red"):
    print(c.contents[0], end='')
