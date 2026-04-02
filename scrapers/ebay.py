from playwright.sync_api import sync_playwright
from urllib.parse import quote
import sys

def search_ebay(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.ebay.com/sch/i.html?_nkw={quote(query)}"

            browser = p.chromium.launch(
                 headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="en-IN"
            )

            page = browser.new_page()

            print("Opening eBay...", file=sys.stderr)
            page.goto(url, timeout=30000)

            page.wait_for_selector("li.s-item",state="attached", timeout=30000)

            items = page.query_selector_all("li.s-item")

            for item in items[:5]:
                try:
                    title = item.query_selector("li.s-item__title").inner_text()
                    price = item.query_selector("li.s-item__price").inner_text()

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