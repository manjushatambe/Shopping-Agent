from agents.search_agent import search_products
from agents.rank_agent import rank_products
from agents.explain_agent import build_prompt


def run_agent(query):
    products = search_products(query)
    ranked = rank_products(products)
    best = ranked[0] if ranked else None
    explanation = build_prompt(query,products)

    return {
        "best": best,
        "all": ranked,
        "why": explanation
    }