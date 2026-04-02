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


def search_croma(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            viewport={"width": 1280, "height": 800},
            permissions=[]  # 🔥 remove location popup
        )

        page = context.new_page()

        # ✅ CORRECT URL
        encoded = quote(query)
        url = f"https://www.croma.com/searchB?q={encoded}%3Arelevance&text={encoded}"

        print("Opening Croma...", file=sys.stderr)

        page.goto(url, timeout=30000)

        # ✅ wait properly
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        # scroll to trigger lazy load
        for _ in range(3):
            page.mouse.wheel(0, 2500)
            page.wait_for_timeout(2000)

        # ✅ now this will work
        page.wait_for_selector("a[href*='/p/']", timeout=30000)

        items = page.query_selector_all("a[href*='/p/']")

        print(f"Croma found: {len(items)} items", file=sys.stderr)

        for item in items[:10]:
            try:
                link = item.get_attribute("href")
                title = item.inner_text().strip()

                if not title or not link:
                    continue

                results.append({
                    "title": title,
                    "price": None,
                    "source": "croma",
                    "link": f"https://www.croma.com{link}"
                })

            except Exception as e:
                print("Item error:", e, file=sys.stderr)

        browser.close()

    print(f"Croma results: {len(results)}", file=sys.stderr)
    return results