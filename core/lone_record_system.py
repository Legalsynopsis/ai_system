import os
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from ddgs import DDGS

# ==============================
# CONFIG
# ==============================

BASE_DIR = "/ai_system/data/RecordRoom"

CATEGORIES = {
    "Land": "Karnataka Land Revenue Act PDF",
    "Bhoomi": "Bhoomi RTC Karnataka PDF",
    "Survey": "Mojini survey Karnataka PDF",
    "Registration": "Kaveri registration Karnataka PDF",
    "Panchayat": "Panchayat Raj Act Karnataka PDF",
    "ESwathu": "E Swathu Karnataka PDF",
    "BDA": "BDA rules Bangalore PDF",
    "KIADB": "KIADB land allotment PDF",
    "EAasthi": "E Aasthi Karnataka PDF",
    "Municipal": "Municipal property rules Karnataka PDF"
}

ALLOWED_DOMAINS = [
    "karnataka.gov.in",
    "bbmp.gov.in",
    "landrecords.karnataka.gov.in",
    "bhoomojini.karnataka.gov.in",
    "kaveri.karnataka.gov.in",
    "bda.karnataka.gov.in",
    "panchayatraj.karnataka.gov.in",
    "kiadb.in"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ==============================
# FUNCTIONS
# ==============================

def is_allowed(url):
    domain = urlparse(url).netloc.lower()
    return any(d in domain for d in ALLOWED_DOMAINS)


def save_pdf(url, category):
    try:
        os.makedirs(f"{BASE_DIR}/{category}", exist_ok=True)

        filename = url.split("/")[-1]
        filepath = f"{BASE_DIR}/{category}/{filename}"

        if os.path.exists(filepath):
            return

        r = requests.get(url, headers=HEADERS, timeout=10, verify=False)

        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"✅ {category}: {filename}")

    except Exception as e:
        print(f"❌ Error: {url}")


def scan_page(url, category):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, "lxml")

        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(url, href)

            if full_url.endswith(".pdf") and is_allowed(full_url):
                save_pdf(full_url, category)

    except:
        pass


def search_and_download(query, category):
    print(f"\n🔍 {query}")

    with DDGS() as ddgs:
        results = ddgs.text(query + " filetype:pdf site:karnataka.gov.in", max_results=10)

        for r in results:
            url = r["href"]

            if is_allowed(url):
                if url.endswith(".pdf"):
                    save_pdf(url, category)
                else:
                    print(f"🌐 {url}")
                    scan_page(url, category)


# ==============================
# MAIN
# ==============================

def main():
    for category, query in CATEGORIES.items():
        search_and_download(query, category)


if __name__ == "__main__":
    main()
