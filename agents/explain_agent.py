import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_choice(best, query):
    try:
        if not best:
            return "No product found."

        prompt = f"""
        You are a smart shopping assistant.

        User query: {query}
        Selected product: {best['title']}
        Price: {best['price']}

        Explain in 2-3 lines why this is a good choice.
        """

        response = client.chat.completions.create(
            model="Llama-3.1-8B-Instruct",  # fast + free
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("Groq error:", e)

        # ✅ fallback (VERY IMPORTANT for production)
        return f"{best['title']} is a good option for '{query}' based on price and availability."