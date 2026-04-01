from playwright.sync_api import sync_playwright
from urllib.parse import quote
import sys

def search_plug(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.plug.tech/search?q={quote(query)}"

            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            page = context.new_page()

            print("Opening Plug...", file=sys.stderr)
            page.goto(url, timeout=60000)

            page.wait_for_timeout(3000)

            # 🔍 Detect block
            content = page.content().lower()
            if "access denied" in content or "captcha" in content:
                print("Plug blocked → skipping", file=sys.stderr)
                return []

            # 🧩 Plug selectors (may change)
            items = page.query_selector_all("div.product-card")

            for item in items[:5]:
                try:
                    title_el = item.query_selector("h3")
                    price_el = item.query_selector(".price")

                    if not title_el or not price_el:
                        continue

                    title = title_el.inner_text().strip()
                    price = price_el.inner_text().replace("$", "").replace(",", "").strip()

                    results.append({
                        "title": title,
                        "price": float(price),
                        "source": "plug"
                    })

                except Exception as e:
                    print("Plug item parse error:", e, file=sys.stderr)

            browser.close()

        except Exception as e:
            print("Plug scraper failed:", e, file=sys.stderr)
            return []

    print(f"Plug results: {len(results)}", file=sys.stderr)
    return results