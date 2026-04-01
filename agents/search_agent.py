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
        print("========== SUBPROCESS OUTPUT ==========")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        print("=======================================")

        output = result.stdout.strip()

        print("RAW OUTPUT BEFORE JSON:", output[:500])

        if not output:
            return fallback_data()

        # Find JSON start
        json_start = output.find("[")
        if json_start != -1:
            output = output[json_start:]

        try:
            data = json.loads(output)
        except Exception as e:
            print("JSON parse error:", e)
            return fallback_data()

        # ✅ Ensure it's a list of dicts
        if not isinstance(data, list):
            return fallback_data()

        clean = [p for p in data if isinstance(p, dict)]

        return clean if clean else fallback_data()

    except Exception as e:
        print(f"Scraper failed: {e}")
        return fallback_data()