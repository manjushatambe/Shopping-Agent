from playwright.sync_api import sync_playwright
import sys
from urllib.parse import quote

def search_amazon(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.amazon.in/s?k={quote(query)}"

            print("Step 1: Launching browser", file=sys.stderr)

            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-blink-features=AutomationControlled"
                ]
            )

            print("Step 2: Creating context", file=sys.stderr)

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="en-IN"
            )

            print("Step 3: Creating page", file=sys.stderr)

            page = context.new_page()

            # CRITICAL DEBUG BLOCK
            try:
                print("Step 4: Before goto", file=sys.stderr)
                page.goto(url, timeout=10000)
                print("Step 5: After goto", file=sys.stderr)

                print("PAGE TITLE:", page.title(), file=sys.stderr)
                print(page.content()[:500], file=sys.stderr)

            except Exception as e:
                print("GOTO FAILED:", e, file=sys.stderr)
                return []

            # simulate human
            page.wait_for_timeout(3000)
            page.mouse.move(100, 200)
            page.mouse.wheel(0, 800)

            # detect block
            content = page.content().lower()
            if "captcha" in content or "access denied" in content:
                print("Amazon blocked scraping", file=sys.stderr)
                return []

            print("Step 6: Waiting for selector", file=sys.stderr)

            page.wait_for_selector('[data-component-type="s-search-result"]', timeout=5000)

            items = page.query_selector_all('[data-component-type="s-search-result"]')

            print(f"Step 7: Found {len(items)} items", file=sys.stderr)

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
                    print("Item parse error:", e, file=sys.stderr)

            browser.close()

        except Exception as e:
            print("Amazon scraper failed:", e, file=sys.stderr)
            return []

    print(f"Amazon results: {len(results)}", file=sys.stderr)
    return results