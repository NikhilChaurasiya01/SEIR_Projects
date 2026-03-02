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
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = "No Title Found"

    content = soup.find("main")
    if content is None:
        content = soup.find("article")
    if content is None:
        content = soup.body

    if content:
        body_text = content.get_text(separator="\n")
        lines = body_text.split("\n")
        clean_lines = []

        for line in lines:
            line = line.strip()
            if line != "":
                clean_lines.append(line)

        clean_body = "\n".join(clean_lines)
    else:
        clean_body = ""

    links = soup.find_all("a")
    urls = []

    for link in links:
        href = link.get("href")
        if href:
            absolute_url = urljoin(url, href)
            urls.append(absolute_url)

except Exception as e:
    print("Error fetching the page:", e)
    sys.exit()

print(title)
print(clean_body)
for i in urls:
    print(i)