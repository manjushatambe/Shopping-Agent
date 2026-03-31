import subprocess
import json


def is_blocked_or_empty(data):
    if not data:
        return True

    # optional: detect weird responses
    for item in data:
        title = item.get("title", "").lower()
        if "captcha" in title or "access denied" in title:
            return True

    return False


def search_products(query):
    try:
        print("🔍 Running scraper subprocess...")

        result = subprocess.run(
            ["python", "scrapers/runner.py", query],
            capture_output=True,
            text=True,
            timeout=60
        )

        # ❌ If script crashed
        if result.returncode != 0:
            print("⚠️ Scraper crashed:", result.stderr)
            return fallback_data()

        # ❌ If no output
        if not result.stdout.strip():
            print("⚠️ Empty output from scraper")
            return fallback_data()

        data = json.loads(result.stdout)

        # ❌ If blocked / empty
        if is_blocked_or_empty(data):
            print("❌ Scraper blocked or returned empty")
            return fallback_data()

        print(f"✅ Scraper success: {len(data)} items")
        return data

    except Exception as e:
        print("⚠️ Subprocess failed:", e)
        return fallback_data()


def fallback_data():
    print("🟡 Using fallback data")

    return [
        {
            "title": "iPhone 15 (Demo)",
            "price": 75000,
            "rating": 4.6,
            "source": "fallback"
        },
        {
            "title": "Samsung Galaxy S23 (Demo)",
            "price": 70000,
            "rating": 4.5,
            "source": "fallback"
        },
        {
            "title": "OnePlus 11R (Demo)",
            "price": 40000,
            "rating": 4.4,
            "source": "fallback"
        }
    ]