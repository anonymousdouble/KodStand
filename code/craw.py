import requests
from bs4 import BeautifulSoup
import os
import shutil


def crawl_page(url, start_url, depth, visited, max_depth, dir):
    if depth > max_depth:
        return
    if url in visited:
        return
    tmp_url = url.removeprefix(start_url)
    tmp_url.strip()
    if tmp_url != "" and not ("#" in tmp_url):
        tmp_url = tmp_url.replace("/", "_")
        path = os.path.join(dir, tmp_url)
        if not url.endswith(".html") and not url.endswith(".xml"):
            path = path + ".html"
        print(path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(requests.get(url).text)
    visited.add(url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a"):
                next_url = link.get("href")
                if next_url and start_url in next_url:
                    crawl_page(next_url, start_url, depth + 1, visited, max_depth, dir)
    except Exception as e:
        print("Error crawling:", url)
        print(e)


if __name__ == "__main__":
    start_url = "https://google.github.io/styleguide/go"
    tmp_url = "https://google.github.io/styleguide/go"
    max_depth = 10
    visited = set()
    dir = "data/input/next"
    shutil.rmtree(dir, ignore_errors=True)
    os.makedirs(dir, exist_ok=True)
    crawl_page(start_url, start_url, 0, visited, max_depth, dir)
