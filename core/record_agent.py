import os
import requests
from bs4 import BeautifulSoup

BASE_PATH = "/ai_system/RecordRoom"

sources = [
    ("https://landrecords.karnataka.gov.in", "Karnataka_Land"),
    ("https://rdservices.karnataka.gov.in", "Revenue"),
    ("https://panchayatraj.karnataka.gov.in", "Panchayat"),
    ("https://bbmp.gov.in", "Municipal"),
]

def download_file(url, folder):
    try:
        local_filename = url.split("/")[-1]
        path = os.path.join(BASE_PATH, folder, local_filename)

        r = requests.get(url, stream=True, timeout=20)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {local_filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def scan_site(base_url, folder):
    try:
        print(f"\nScanning {base_url}")
        r = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for link in soup.find_all("a"):
            href = link.get("href")

            if href and (".pdf" in href or ".doc" in href):
                full_url = href if href.startswith("http") else base_url + href
                download_file(full_url, folder)

    except Exception as e:
        print(f"Error scanning {base_url}: {e}")

def main():
    for url, folder in sources:
        scan_site(url, folder)

if __name__ == "__main__":
    main()
