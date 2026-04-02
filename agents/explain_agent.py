import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_products(products):
    text = ""
    for i, p in enumerate(products, 1):
        text += f"{i}. {p['title']} | Price: {p.get('price')}\n"
    return text


def build_prompt(query, products):
    formatted_products = format_products(products[:10])  # limit

    prompt = f"""
You are a smart shopping assistant.

User query:
{query}

Available products:
{formatted_products}

Your task:
1. Understand user intent (budget, brand, category)
2. Filter irrelevant products
3. Compare based on price and value
4. Recommend top 3

Rules:
- Explain reasoning
- Prefer known brands
- Be concise

Output:
- Summary
- Top 3 picks
- Best budget option
"""
    return prompt


def ask_llm(query, products):
    try:
        prompt = build_prompt(query, products)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)

        # ✅ fallback (important)
        if products:
            best = products[0]
            return f"{best['title']} is a good option for '{query}'."
        return "No good products found."