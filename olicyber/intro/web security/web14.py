import requests
from bs4 import BeautifulSoup
from bs4 import Comment

r = requests.get("http://web-14.challs.olicyber.it")
soup = BeautifulSoup(r.text, 'html.parser')
comments = soup.find_all(string=lambda text: isinstance(text, Comment))

for c in comments:
    print(c, end='')
