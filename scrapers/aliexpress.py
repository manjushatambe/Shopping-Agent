from playwright.sync_api import sync_playwright
from urllib.parse import quote
import sys

def search_aliexpress(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.aliexpress.com/wholesale?SearchText={quote(query)}"

            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            page = browser.new_page()

            print("Opening AliExpress...", file=sys.stderr)
            page.goto(url, timeout=60000)

            page.wait_for_selector("._12A8D", timeout=15000)

            items = page.query_selector_all("._12A8D")

            for item in items[:5]:
                try:
                    title = item.query_selector("._18_85").inner_text()
                    price = item.query_selector("._30jeq3").inner_text()

                    price = price.replace("$", "").replace(",", "")

                    results.append({
                        "title": title,
                        "price": float(price) * 83,
                        "source": "aliexpress"
                    })
                except:
                    continue

            browser.close()

        except Exception as e:
            print("AliExpress failed:", e, file=sys.stderr)
            return []

    print(f"AliExpress results: {len(results)}", file=sys.stderr)
    return results