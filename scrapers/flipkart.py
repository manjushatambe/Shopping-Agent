from playwright.sync_api import sync_playwright
import sys
from urllib.parse import quote

def search_flipkart(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.flipkart.com/s?k={quote(query)}"

            browser = p.chromium.launch(
                 headless=True,
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

            print("Step 3: Creating page", file=sys.stderr)

            page = context.new_page()

            # CRITICAL DEBUG BLOCK
            try:
                print("Step 4: Before goto", file=sys.stderr)
                page.goto(url, timeout=30000)
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
                print("Flipkart blocked scraping", file=sys.stderr)
                return []

            print("Step 6: Waiting for selector", file=sys.stderr)

            page.wait_for_selector("div._1AtVbE", timeout=30000)

            items = page.query_selector_all("div._1AtVbE")

            print(f"Step 7: Found {len(items)} items", file=sys.stderr)

            for item in items[:5]:
                try:
                    title_el = item.query_selector("div._4rR01T, a.s1Q9rs")
                    price_el = item.query_selector("div._30jeq3")

                    if not title_el or not price_el:
                        continue

                    title = title_el.inner_text()
                    price = price_el.inner_text().replace(",", "")

                    results.append({
                        "title": title,
                        "price": float(price),
                        "source": "flipkart"
                    })

                except Exception as e:
                    print("Item parse error:", e, file=sys.stderr)

            browser.close()

        except Exception as e:
            print("Flipkart scraper failed:", e, file=sys.stderr)
            return []

    print(f"Flipkart results: {len(results)}", file=sys.stderr)
    return results