from agents.search_agent import search_products
from agents.rank_agent import rank_products
from agents.explain_agent import ask_llm


def run_agent(query):
    products = search_products(query)
    ranked = rank_products(products)
    best = ranked[0] if ranked else None
    explanation = ask_llm(query, products)

    return {
        "best": best,
        "all": ranked,
        "why": explanation
    }