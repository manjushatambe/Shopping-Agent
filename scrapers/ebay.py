from playwright.sync_api import sync_playwright
from urllib.parse import quote
import sys

def search_ebay(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.ebay.com/sch/i.html?_nkw={quote(query)}"

            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()

            print("Opening eBay...", file=sys.stderr)
            page.goto(url, timeout=10000)

            page.wait_for_selector(".s-item", timeout=5000)

            items = page.query_selector_all(".s-item")

            for item in items[:5]:
                try:
                    title = item.query_selector(".s-item__title").inner_text()
                    price = item.query_selector(".s-item__price").inner_text()

                    price = price.replace("$", "").replace(",", "").split(" ")[0]

                    results.append({
                        "title": title,
                        "price": float(price) * 83,  # convert USD → INR
                        "source": "ebay"
                    })

                except:
                    continue

            browser.close()

        except Exception as e:
            print("eBay failed:", e, file=sys.stderr)
            return []

    print(f"eBay results: {len(results)}", file=sys.stderr)
    return results