import requests
from bs4 import BeautifulSoup
from bs4 import Comment

r = requests.get("http://web-15.challs.olicyber.it")
soup = BeautifulSoup(r.text, 'html.parser')

sources = soup.find_all(src=True)
for source in sources:
    r = requests.get(f"http://web-15.challs.olicyber.it{source['src']}")
    for line in r.text.splitlines():
        if "flag{" in line:
            print(line)
