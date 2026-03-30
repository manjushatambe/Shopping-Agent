import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from amazon import search_amazon
from flipkart import search_flipkart
import sys
import json

if __name__ == "__main__":
    query = sys.argv[1]

    results = []
    results.extend(search_amazon(query))
    results.extend(search_flipkart(query))

    print(json.dumps(results))