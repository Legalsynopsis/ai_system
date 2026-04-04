from playwright.sync_api import sync_playwright
import os
import time

DOWNLOAD_DIR = "/ai_system/data/downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def automate_site(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        print(f"Opening {url} ...")
        page.goto(url)

        # Screenshot
        page.screenshot(path="/ai_system/data/screenshot.png")

        print("Looking for downloadable files...")

        links = page.query_selector_all("a")

        for link in links:
            href = link.get_attribute("href")

            if href and (".pdf" in href or ".doc" in href):
                print(f"Downloading: {href}")
                try:
                    with page.expect_download() as download_info:
                        link.click()
                    download = download_info.value
                    download.save_as(os.path.join(DOWNLOAD_DIR, download.suggested_filename))
                except:
                    pass

        print("Automation completed.")
        time.sleep(5)
        browser.close()


if __name__ == "__main__":
    url = input("Enter website URL: ")
    automate_site(url)
