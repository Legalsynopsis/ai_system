from playwright.sync_api import sync_playwright

def extract_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url)

        content = page.inner_text("body")

        browser.close()
        return content[:2000]
