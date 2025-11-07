import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "http://web-16.challs.olicyber.it"

session = requests.Session()
session.headers.update({"User-Agent": "flag-crawler/1.0"})

def find_flag(start_path=""):
    visited = set()
    queue = [urljoin(BASE, start_path)]

    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        try:
            r = session.get(url, timeout=5)
            r.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        flag_tags = soup.find_all("h1", string=lambda txt: txt and "flag{" in txt)
        if flag_tags:
            return flag_tags[0].get_text(strip=True)

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            next_url = urljoin(url, href)
            if next_url.startswith(BASE) and next_url not in visited:
                queue.append(next_url)

    return None

if __name__ == "__main__":
    flag = find_flag()
    if flag:
        print(flag)
    else:
        print("No flag found")

