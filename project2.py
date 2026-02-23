import sys
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re


def get_page_title(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")

        if soup.title and soup.title.string:
            return soup.title.string.strip()
        else:
            return "No Title Found"

    except:
        return "Error fetching title"



def extract_body_and_links(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=10)
        html = response.read().decode("utf-8")

        soup = BeautifulSoup(html, "html.parser")

        body_text = soup.body.get_text(separator=" ")

        lines = body_text.split("\n")
        clean_lines = []

        for line in lines:
            line = line.strip()
            if line != "":
                clean_lines.append(line)

        clean_body = "\n".join(clean_lines)

        links = soup.find_all("a")
        urls = []

        from urllib.parse import urljoin
        for link in links:
            href = link.get("href")
            if href:
                urls.append(urljoin(url, href))

        return clean_body, urls

    except Exception as e:
        print("Error:", e)
        return "", []

def hash_word(word):
    p = 53
    m = 2**64

    hash_value = 0
    power = 1

    for ch in word:
        hash_value = (hash_value + ord(ch) * power) % m
        power = (power * p) % m
    return hash_value


def compute_simhash(freq_dict):
    vector = [0] * 64

    for word, count in freq_dict.items():
        h = hash_word(word)

        for i in range(64):
            bit = (h >> i) & 1

            if bit == 1:
                vector[i] += count
            else:
                vector[i] -= count

    simhash = 0
    for i in range(64):
        if vector[i] > 0:
            simhash |= (1 << i)

    return simhash


def process_url(url):
    body, _ = extract_body_and_links(url)

    words = re.findall(r"[a-z0-9]+", body.lower())

    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    return compute_simhash(freq)



def count_common_bits(h1, h2):
    count = 0
    for i in range(64):
        if ((h1 >> i) & 1) == ((h2 >> i) & 1):
            count += 1
    return count


if len(sys.argv) < 3:
    print("Usage: python3 seir-ass.py <url1> <url2>")
    sys.exit()

url1 = sys.argv[1]
url2 = sys.argv[2]
