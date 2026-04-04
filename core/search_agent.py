import os
import requests
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# BASE PATH
BASE_PATH = "/ai_system/RecordRoom"

# SEARCH KEYWORDS
KEYWORDS = [
    "Karnataka Land Revenue Act PDF",
    "Bhoomi RTC Karnataka PDF",
    "Mojini survey Karnataka PDF",
    "Kaveri registration Karnataka PDF",
    "Panchayat Raj Act Karnataka PDF",
    "E Swathu Karnataka PDF",
    "BDA rules Bangalore PDF",
    "KIADB land allotment PDF",
    "E Aasthi Karnataka PDF",
    "Municipal property rules Karnataka PDF"
]

# ALLOWED DOMAINS
ALLOWED_DOMAINS = ["gov.in", "nic.in"]

# DEPARTMENT CLASSIFICATION
DEPARTMENTS = {
    "land": "Karnataka_Land",
    "bhoomi": "Karnataka_Land",
    "survey": "Survey",
    "mojini": "Survey",
    "registration": "Registration",
    "kaveri": "Registration",
    "panchayat": "Panchayat",
    "swathu": "Panchayat",
    "bda": "BDA",
    "kiadb": "KIADB",
    "aasthi": "GBA",
    "municipal": "Municipal"
}

# CREATE FOLDERS
def setup_folders():
    for folder in set(DEPARTMENTS.values()):
        os.makedirs(os.path.join(BASE_PATH, folder), exist_ok=True)
    os.makedirs(os.path.join(BASE_PATH, "Misc"), exist_ok=True)

# CHECK DOMAIN
def is_allowed(url):
    domain = urlparse(url).netloc
    return any(d in domain for d in ALLOWED_DOMAINS)

# CLASSIFY FILE
def classify(url):
    url_lower = url.lower()
    for key, folder in DEPARTMENTS.items():
        if key in url_lower:
            return folder
    return "Misc"

# DOWNLOAD FILE
def download(url):
    try:
        filename = url.split("/")[-1].split("?")[0]

        if not filename.endswith((".pdf", ".doc", ".docx")):
            return

        folder = classify(url)
        save_folder = os.path.join(BASE_PATH, folder)
        path = os.path.join(save_folder, filename)

        # SKIP duplicates
        if os.path.exists(path):
            print(f"⚠️ Skipped (exists): {filename}")
            return

        r = requests.get(url, timeout=20, verify=False)

        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"✅ Saved → {folder}/{filename}")

    except Exception as e:
        print(f"❌ Error: {e}")

# MAIN SEARCH SYSTEM
def run():
    setup_folders()

    with DDGS() as ddgs:
        for query in KEYWORDS:
            print(f"\n🔍 Searching: {query}")

            results = ddgs.text(query, max_results=10)

            for r in results:
                url = r["href"]

                if is_allowed(url):
                    download(url)

if __name__ == "__main__":
    run()
