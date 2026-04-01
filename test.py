from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Opening Google...")
    page.goto("https://google.com")

    print("Title:", page.title())

    browser.close()