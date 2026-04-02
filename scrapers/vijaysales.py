from playwright.sync_api import sync_playwright
from urllib.parse import quote
import re
import sys


def parse_price(text):
    if not text:
        return None
    try:
        clean = re.sub(r"[^\d.]", "", text)
        return float(clean) if clean else None
    except:
        return None


def search_vijaysales(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            viewport={"width": 1280, "height": 800},
            permissions=[]
        )

        page = context.new_page()

        # ✅ CORRECT URL
        url = f"https://www.vijaysales.com/search-listing?q={quote(query)}"

        print("Opening Vijay Sales...", file=sys.stderr)

        try:
            page.goto(url, timeout=30000)
        except Exception as e:
            print("Goto failed:", e, file=sys.stderr)
            return []

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        # ❗ check if page got blocked
        if page.is_closed():
            print("Page closed unexpectedly", file=sys.stderr)
            return []

        print("Page URL:", page.url, file=sys.stderr)

        # simulate human
        page.mouse.move(200, 300)
        page.wait_for_timeout(1000)

        # scroll to load products
        for _ in range(3):
            page.mouse.wheel(0, 2500)
            page.wait_for_timeout(2000)

        # ✅ robust selector
        page.wait_for_selector("a", timeout=30000)

        items = page.query_selector_all("div[class*='product']")

        print(f"Vijay Sales found: {len(items)} items", file=sys.stderr)

        for item in items[:10]:
            try:
                link = item.get_attribute("href")
                title = item.inner_text().strip()

                if not title or not link:
                    continue

                results.append({
                    "title": title,
                    "price": None,
                    "source": "vijay_sales",
                    "link": f"https://www.vijaysales.com{link}"
                })

            except Exception as e:
                print("Item error:", e, file=sys.stderr)

        browser.close()

    print(f"Vijay Sales results: {len(results)}", file=sys.stderr)
    return results