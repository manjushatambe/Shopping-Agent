import json
import sys

from amazon import search_amazon
from flipkart import search_flipkart
#from plug import search_plug
from ebay import search_ebay
#from newegg import search_newegg
#from bestbuy import search_bestbuy
#from aliexpress import search_aliexpress


# ✅ Handle missing query (for manual runs)
if len(sys.argv) < 2:
    print("⚠️ No query provided, using default", file=sys.stderr)
    query = "iphone"
else:
    query = sys.argv[1]


results = []


# ✅ Safe wrapper (skip failures)
def safe_run(scraper_fn, name):
    try:
        print(f"🔍 Running {name}...", file=sys.stderr)

        data = scraper_fn(query)

        # ✅ Skip empty / blocked
        if not data or len(data) == 0:
            print(f"⚠️ {name} returned no results → skipping", file=sys.stderr)
            return []

        print(f"✅ {name} success: {len(data)} items", file=sys.stderr)
        return data

    except Exception as e:
        print(f"❌ {name} failed: {e}", file=sys.stderr)
        return []


# 🔥 Run all scrapers safely
results += safe_run(search_amazon, "Amazon")
results += safe_run(search_flipkart, "Flipkart")
#results += safe_run(search_plug, "Plug")
results += safe_run(search_ebay, "eBay")
#results += safe_run(search_newegg, "Newegg")
#results += safe_run(search_bestbuy, "BestBuy")
#results += safe_run(search_aliexpress, "AliExpress")

# ✅ Always return valid JSON (NO prints allowed after this)
output = json.dumps(results, ensure_ascii=False)

# 🔥 FIX: force UTF-8 output (prevents Windows crash)
sys.stdout.buffer.write(output.encode("utf-8"))