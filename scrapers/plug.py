from playwright.sync_api import sync_playwright

def search_plug(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = f"https://plug.tech/search?q={query}"
        page.goto(url, timeout=60000)

        items = page.query_selector_all(".product-card")

        for item in items[:5]:
            try:
                title = item.query_selector(".product-title").inner_text()
                price = item.query_selector(".price").inner_text().replace("$", "")

                results.append({
                    "title": title,
                    "price": float(price),
                    "source": "plug"
                })
            except:
                continue

        browser.close()

    return results