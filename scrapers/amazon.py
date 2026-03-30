from playwright.sync_api import sync_playwright


def search_amazon(query):
    with sync_playwright() as p:
        #browser = p.chromium.launch(headless=True
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = browser.new_page()
        page.goto(f"https://www.amazon.in/s?k={query}")

        items = page.query_selector_all(".s-result-item")
        results = []

        for item in items[:5]:
            try:
                title = item.query_selector("h2 span").inner_text()
                price = item.query_selector(".a-price-whole").inner_text()

                results.append({
                    "title": title,
                    "price": float(price.replace(',', '')),
                    "source": "amazon"
                })
            except:
                pass

        browser.close()
        return results