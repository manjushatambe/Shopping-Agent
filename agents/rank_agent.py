def score(p):
    try:
        price = float(p.get("price", 999999))
        rating = float(p.get("rating", 3))
        return (1/price)*0.7 + rating*0.3
    except:
        return -999999

def rank_products(products):
    # ✅ filter bad data
    products = [p for p in products if isinstance(p, dict)]

    return sorted(products, key=score, reverse=True)