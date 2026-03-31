from playwright.sync_api import sync_playwright


def search_flipkart(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.flipkart.com/search?q={query}"

            browser = p.chromium.launch(
                headless=True,
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

            print("Opening Amazon...")
            page.goto(url, timeout=60000)

            # simulate human behavior
            page.wait_for_timeout(2000)
            page.mouse.move(100, 200)
            page.mouse.wheel(0, 500)

            # 🔍 detect block
            content = page.content().lower()
            if "captcha" in content or "access denied" in content:
                print("❌ Amazon blocked scraping")
                return []

            items = page.query_selector_all(".s-result-item")

            for item in items[:5]:
                try:
                    title_el = item.query_selector("h2 span")
                    price_el = item.query_selector(".a-price-whole")

                    if not title_el or not price_el:
                        continue

                    title = title_el.inner_text()
                    price = price_el.inner_text().replace(",", "")

                    results.append({
                        "title": title,
                        "price": float(price),
                        "source": "amazon"
                    })

                except Exception as e:
                    print("Item parse error:", e)
                    continue

            browser.close()

        except Exception as e:
            print("Amazon scraper failed:", e)
            return []

    print(f"Amazon results: {len(results)}")
    return results