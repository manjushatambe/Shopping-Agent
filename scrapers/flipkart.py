from playwright.sync_api import sync_playwright
import sys
import re
from urllib.parse import quote


def parse_price(price_text):
    if not price_text:
        return None
    try:
        clean = re.sub(r"[^\d.]", "", price_text)
        return float(clean) if clean else None
    except:
        return None


def search_flipkart(query):
    results = []

    with sync_playwright() as p:
        try:
            url = f"https://www.flipkart.com/search?q={quote(query)}&otracker=search&otracker1=search"

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

            print("Step 3: Creating page", file=sys.stderr)
            page = context.new_page()

            try:
                print("Step 4: Before goto", file=sys.stderr)
                page.goto(url, timeout=60000)
                print("Step 5: After goto", file=sys.stderr)

                print("PAGE TITLE:", page.title(), file=sys.stderr)

            except Exception as e:
                print("GOTO FAILED:", e, file=sys.stderr)
                return []

            # Close login popup if present
            try:
                page.click("button._2KpZ6l._2doB4z", timeout=3000)
                print("Closed login popup", file=sys.stderr)
            except:
                pass

            # simulate human behavior
            page.wait_for_timeout(4000)
            page.mouse.move(100, 200)
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(2000)

            # detect blocking
            content = page.content().lower()
            if "captcha" in content or "access denied" in content:
                print("Flipkart blocked scraping", file=sys.stderr)
                return []

            print("Step 6: Waiting for selector", file=sys.stderr)

            page.wait_for_selector("div[data-id]", timeout=60000)

            items = page.query_selector_all("div[data-id]")

            print(f"Step 7: Found {len(items)} items", file=sys.stderr)

            for item in items[:10]:   # increased from 5 → 10
                try:
                    title_el = item.query_selector("div._4rR01T, a.s1Q9rs, div.KzDlHZ")
                    price_el = item.query_selector("div._30jeq3")
                    link_el = item.query_selector("a")

                    title_text = title_el.inner_text().strip() if title_el else None
                    price_text = price_el.inner_text().strip() if price_el else None
                    link_href = link_el.get_attribute("href") if link_el else None

                    price = parse_price(price_text)

                    print("DEBUG:", title_text, price_text, price, file=sys.stderr)

                    # ✅ only require title
                    if not title_text:
                        continue

                    results.append({
                        "title": title_text,
                        "price": price,
                        "source": "flipkart",
                        "link": f"https://www.flipkart.com{link_href}" if link_href else None
                    })

                except Exception as e:
                    print("Item parse error:", e, file=sys.stderr)

            browser.close()

        except Exception as e:
            print("Flipkart scraper failed:", e, file=sys.stderr)
            return []

    print(f"Flipkart results: {len(results)}", file=sys.stderr)
    return results