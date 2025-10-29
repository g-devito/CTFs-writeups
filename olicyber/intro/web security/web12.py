import requests
from bs4 import BeautifulSoup

r = requests.get("http://web-12.challs.olicyber.it")
soup = BeautifulSoup(r.text, 'html.parser')

print(soup.find_all('pre')[0].contents[0])
