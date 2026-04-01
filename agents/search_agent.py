import subprocess
import json
import sys
import os
from unittest import result

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
        #data = json.loads(result.stdout)
        
        output = result.stdout.strip()
        # Find JSON start
        json_start = output.find("[")
        if json_start != -1:
            output = output[json_start:]

        try:
            data = json.loads(output)
        except Exception as e:
            print("JSON parse error:", e)
            return fallback_data()
        
        # Normalize scraper output to match fallback format
        return {
            "all": data,
            "best": data[0] if data else None,
            "why": "Scraper data"
        }
    except Exception as e:
        print(f"Scraper failed: {e}")
        return fallback_data()