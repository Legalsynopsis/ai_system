import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://kandaya.karnataka.gov.in/61/Acts%20and%20Rules/en"
SAVE_PATH = "/ai_system/data/RecordRoom/Karnataka_Acts"

os.makedirs(SAVE_PATH, exist_ok=True)


def download_file(url, folder):
    try:
        filename = url.split("/")[-1]

        if not filename.endswith(".pdf"):
            return

        path = os.path.join(folder, filename)

        if os.path.exists(path):
            print(f"Already exists: {filename}")
            return

        r = requests.get(url, timeout=10)

        with open(path, "wb") as f:
            f.write(r.content)

        print(f"Downloaded: {filename}")

    except Exception as e:
        print(f"Error: {url} -> {e}")


def scan_and_download(url):
    try:
        print(f"\n🔍 Scanning: {url}")

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, verify=False)

        soup = BeautifulSoup(res.text, "lxml")

        links = soup.find_all("a", href=True)

        for link in links:
            href = link["href"]

            full_url = urljoin(url, href)

            if ".pdf" in full_url.lower():
                download_file(full_url, SAVE_PATH)

    except Exception as e:
        print(f"Scan error: {e}")


if __name__ == "__main__":
    scan_and_download(BASE_URL)
