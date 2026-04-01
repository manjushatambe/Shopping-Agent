from playwright.sync_api import sync_playwright
from urllib.parse import quote
import sys

def search_bestbuy(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.bestbuy.com/site/searchpage.jsp?st={quote(query)}"

            browser = p.chromium.launch(headless=False, args=["--no-sandbox"])
            page = browser.new_page()

            print("Opening BestBuy...", file=sys.stderr)
            page.goto(url, timeout=60000)

            page.wait_for_selector(".sku-item", timeout=10000)

            items = page.query_selector_all(".sku-item")

            for item in items[:5]:
                try:
                    title = item.query_selector(".sku-title").inner_text()
                    price = item.query_selector(".priceView-customer-price span").inner_text()

                    price = price.replace("$", "").replace(",", "")

                    results.append({
                        "title": title,
                        "price": float(price) * 83,
                        "source": "bestbuy"
                    })
                except:
                    continue

            browser.close()

        except Exception as e:
            print("BestBuy failed:", e, file=sys.stderr)
            return []

    print(f"BestBuy results: {len(results)}", file=sys.stderr)
    return results