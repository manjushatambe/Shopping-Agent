import subprocess
import json

def search_products(query):
    result = subprocess.run(
        ["python", "scrapers/runner.py", query],
        capture_output=True,
        text=True
    )

    try:
        return json.loads(result.stdout)
    except:
        print("Scraper error:", result.stderr)
        return []