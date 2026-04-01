from playwright.sync_api import sync_playwright
from urllib.parse import quote
import sys

def search_newegg(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.newegg.com/p/pl?d={quote(query)}"

            browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
            page = browser.new_page()

            print("Opening Newegg...", file=sys.stderr)
            page.goto(url, timeout=10000)

            page.wait_for_selector(".item-cell", timeout=5000)

            items = page.query_selector_all(".item-cell")

            for item in items[:5]:
                try:
                    title = item.query_selector(".item-title").inner_text()
                    price = item.query_selector(".price-current").inner_text()

                    price = price.replace("$", "").replace(",", "").split()[0]

                    results.append({
                        "title": title,
                        "price": float(price) * 83,
                        "source": "newegg"
                    })
                except:
                    continue

            browser.close()

        except Exception as e:
            print("Newegg failed:", e, file=sys.stderr)
            return []

    print(f"Newegg results: {len(results)}", file=sys.stderr)
    return results