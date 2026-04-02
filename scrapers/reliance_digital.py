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


def handle_reliance_popup(page):
    try:
        page.wait_for_timeout(3000)

        # detect popup using text
        if page.locator("text=Allow Location Access").count() > 0:
            print("Reliance popup detected", file=sys.stderr)

            for sel in [
                "button[aria-label='Close']",
                "button:has-text('×')",
                "button:has-text('Close')"
            ]:
                try:
                    btn = page.query_selector(sel)
                    if btn:
                        btn.click()
                        print("Popup closed", file=sys.stderr)
                        page.wait_for_timeout(2000)
                        return True
                except:
                    continue

        print("No popup or already closed", file=sys.stderr)
        return False

    except Exception as e:
        print("Popup error:", e, file=sys.stderr)
        return False


def search_reliance(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()

        url = f"https://www.reliancedigital.in/search?q={quote(query)}"

        print("Opening Reliance Digital...", file=sys.stderr)

        page.goto(url, timeout=30000)

        # ✅ HANDLE POPUP
        handle_reliance_popup(page)

        page.wait_for_timeout(4000)

        # 🔥 force content load
        for _ in range(3):
            page.mouse.move(200, 300)
            page.mouse.wheel(0, 2000)
            page.wait_for_timeout(2000)

        # 🔍 wait for ANY product link (stable approach)
        page.wait_for_selector("a[href*='/p/']", timeout=30000)

        items = page.query_selector_all("a[href*='/p/']")

        print(f"Reliance found: {len(items)} items", file=sys.stderr)

        for item in items[:10]:
            try:
                link = item.get_attribute("href")
                title = item.inner_text().strip()

                if not title or not link:
                    continue

                results.append({
                    "title": title,
                    "price": None,  # price extraction unreliable here
                    "source": "reliance_digital",
                    "link": f"https://www.reliancedigital.in{link}"
                })

            except Exception as e:
                print("Item error:", e, file=sys.stderr)

        browser.close()

    print(f"Reliance results: {len(results)}", file=sys.stderr)
    return results