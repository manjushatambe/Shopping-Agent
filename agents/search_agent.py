import subprocess
import json
import sys
import os

from agents.fallback import fallback_data

def search_products(query):

    script_path = os.path.abspath("scrapers/runner.py")

    result = subprocess.run(
        [sys.executable, script_path, query],
        capture_output=True,
        text=True,
        encoding="utf-8",   
        errors="ignore"     
    )

    print("STDOUT >>>", repr(result.stdout))
    print("STDERR >>>", result.stderr)

    # ✅ If no output → fallback
    if not result.stdout.strip():

        return fallback_data(query)

    try:
        return json.loads(result.stdout)
    except Exception as e:
       
        return fallback_data(query)