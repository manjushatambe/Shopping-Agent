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
