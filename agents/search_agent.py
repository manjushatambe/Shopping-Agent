import subprocess
import json
import sys
import os

from agents.fallback import fallback_data

def search_products(query):

    script_path = os.path.abspath("scrapers/runner.py")
    try:

        result = subprocess.run(
            [sys.executable, script_path, query],
            capture_output=True,
            text=True,
            check=True,
            encoding="utf-8",   
            errors="ignore"     
            )
        data = json.loads(result.stdout)
        # Normalize scraper output to match fallback format
        return {
            "all": data,
            "best": data[0] if data else None,
            "why": "Scraper data"
        }
    except Exception as e:
        print(f"Scraper failed: {e}")
        return fallback_data()