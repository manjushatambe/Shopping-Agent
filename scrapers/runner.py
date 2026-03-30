import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from plug import search_plug
from nomad import search_nomad
from peak import search_peak


def safe_run(scraper_func, query, name):
    try:
        print(f"Running {name} scraper...")
        results = scraper_func(query)

        if not results:
            print(f"{name} returned empty → possibly blocked")
            return []

        print(f"{name} success: {len(results)} items")
        return results

    except Exception as e:
        print(f"{name} failed:", e)
        return []


def search_products(query):
    results = []

    # run scrapers safely
    results += safe_run(search_plug, query, "Plug")
    results += safe_run(search_nomad, query, "Nomad")
    results += safe_run(search_peak, query, "Peak")

    # 🚨 fallback if ALL fail
    if not results:
        print("All scrapers failed → using fallback")

        results = [
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
            }
        ]

    return results