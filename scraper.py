import sys
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup

if len(sys.argv) < 2:
    print("Usage: python scraper.py <URL>")
    sys.exit()

url = sys.argv[1]
if not url.startswith("http"):
    url = "https://" + url

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        print(soup.title.get_text().strip())
    else:
        print("No Title Found")


    paragraphs = soup.find_all("p")
    for p in paragraphs:
        text = p.get_text().strip()
        if text:
            print(text)

    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href:
            print(urljoin(url, href))

except Exception as e:
    print("Error:", e)