# =============================
# FULL FREE SHOPPING AI AGENT
# Backend: FastAPI
# Frontend: React (separate section below)
# Multi-Agent System (AutoGPT-style)
# =============================

# ---------- BACKEND ----------

# requirements.txt
"""
fastapi
uvicorn
playwright
psycopg2-binary
redis
python-dotenv
"""

# main.py
from fastapi import FastAPI
from agents.controller import run_agent

app = FastAPI()

@app.get("/search")
def search(q: str):
    result = run_agent(q)
    return {"result": result}

# ---------- AGENT SYSTEM ----------

# agents/controller.py
from agents.search_agent import search_products
from agents.rank_agent import rank_products
from agents.explain_agent import explain_choice


def run_agent(query):
    products = search_products(query)
    ranked = rank_products(products)
    best = ranked[0] if ranked else None
    explanation = explain_choice(best, query)

    return {
        "best": best,
        "all": ranked,
        "why": explanation
    }

# ---------- SEARCH AGENT ----------

# agents/search_agent.py
from scrapers.amazon import search_amazon
from scrapers.flipkart import search_flipkart


def search_products(query):
    results = []
    results.extend(search_amazon(query))
    results.extend(search_flipkart(query))
    return results

# ---------- RANK AGENT ----------

# agents/rank_agent.py

def score(p):
    price = float(p.get("price", 999999))
    rating = float(p.get("rating", 3))

    return (1/price)*0.7 + rating*0.3


def rank_products(products):
    return sorted(products, key=score, reverse=True)

# ---------- EXPLAIN AGENT ----------

# agents/explain_agent.py
import subprocess


def explain_choice(product, query):
    if not product:
        return "No product found"

    prompt = f"Why is this the best product for '{query}': {product}"

    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )

    return result.stdout

# ---------- SCRAPERS ----------

# scrapers/amazon.py
from playwright.sync_api import sync_playwright


def search_amazon(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.amazon.in/s?k={query}")

        items = page.query_selector_all(".s-result-item")
        results = []

        for item in items[:5]:
            try:
                title = item.query_selector("h2 span").inner_text()
                price = item.query_selector(".a-price-whole").inner_text()

                results.append({
                    "title": title,
                    "price": float(price.replace(',', '')),
                    "source": "amazon"
                })
            except:
                pass

        browser.close()
        return results

# scrapers/flipkart.py
from playwright.sync_api import sync_playwright


def search_flipkart(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.flipkart.com/search?q={query}")

        items = page.query_selector_all("._1AtVbE")
        results = []

        for item in items[:5]:
            try:
                title = item.query_selector("div._4rR01T").inner_text()
                price = item.query_selector("div._30jeq3").inner_text()

                results.append({
                    "title": title,
                    "price": float(price.replace('₹','').replace(',', '')),
                    "source": "flipkart"
                })
            except:
                pass

        browser.close()
        return results

# ---------- FRONTEND (React) ----------

# package.json
"""
{
  "name": "shopping-ai-ui",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
"""

# App.js
"""
import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);

  const search = async () => {
    const res = await fetch(`http://localhost:8000/search?q=${query}`);
    const data = await res.json();
    setResults(data.result);
  };

  return (
    <div style={{padding: 20}}>
      <h1>Shopping AI Agent</h1>

      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search product"
      />

      <button onClick={search}>Search</button>

      {results && (
        <div>
          <h2>Best Product</h2>
          <p>{results.best.title}</p>
          <p>₹{results.best.price}</p>

          <h3>Why?</h3>
          <p>{results.why}</p>

          <h2>All Results</h2>
          {results.all.map((p, i) => (
            <div key={i}>
              <p>{p.title} - ₹{p.price}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
"""

# ---------- RUN INSTRUCTIONS ----------

# Backend
# uvicorn main:app --reload

# Frontend
# npm install
# npm start

# Install Playwright browsers
# playwright install

# Run LLM
# ollama run llama3

# =============================
# DONE: FULL WORKING FREE AGENT
# =============================
