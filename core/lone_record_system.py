import os
import requests
from ddgs import DDGS

BASE_PATH = "/ai_system/data/RecordRoom"

KEYWORDS = {
    "LandRevenue": "Karnataka Land Revenue Act 1964 PDF site:karnataka.gov.in",
    "Survey": "Mojini Karnataka survey rules PDF site:karnataka.gov.in",
    "Registration": "Kaveri registration rules Karnataka PDF site:karnataka.gov.in",
    "Panchayat": "E Swathu Panchayat Raj Karnataka Act PDF site:karnataka.gov.in",
    "BDA": "Bangalore Development Authority Act rules PDF site:karnataka.gov.in",
    "KIADB": "KIADB land allotment rules Karnataka PDF site:karnataka.gov.in",
    "Municipal": "Karnataka Municipal Act property tax rules PDF site:karnataka.gov.in"
}

BLOCK_WORDS = [
    "textile", "garment", "solar", "wildlife", "energy",
    "audit", "budget", "policy", "scheme", "tender"
]

def is_valid(url):
    url_lower = url.lower()

    if not url_lower.endswith(".pdf"):
        return False

    if "karnataka" not in url_lower:
        return False

    if ".gov.in" not in url_lower:
        return False

    for word in BLOCK_WORDS:
        if word in url_lower:
            return False

    return True

def download_pdf(url, folder):
    try:
        filename = url.split("/")[-1]
        path = os.path.join(BASE_PATH, folder, filename)

        if os.path.exists(path):
            return

        response = requests.get(url, timeout=15, verify=False)
        with open(path, "wb") as f:
            f.write(response.content)

        print(f"✅ {folder}: {filename}")

    except:
        print(f"❌ Skipped: {url}")

def run():
    for folder, query in KEYWORDS.items():
        print(f"\n🔍 {query}")

        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=15)

            for r in results:
                url = r.get("href", "")

                if is_valid(url):
                    download_pdf(url, folder)

if __name__ == "__main__":
    run()
