from playwright.sync_api import sync_playwright


def search_flipkart(query):
    with sync_playwright() as p:
        #browser = p.chromium.launch(headless=True)
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page()
        page.goto(f"https://www.flipkart.com/search?q={query}")

        items = page.query_selector_all("._1AtVbE")
        results = []

        for item in items[:5]:
            try:
                title = item.query_selector("div._4rR01T").inner_text()
                price = item.query_selector("div._30jeq3").inner_text()

                results.append({
                    "title": title,
                    "price": float(price.replace('₹','').replace(',', '')),
                    "source": "flipkart"
                })
            except:
                pass

        browser.close()
        return results