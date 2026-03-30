def score(p):
    price = float(p.get("price", 999999))
    rating = float(p.get("rating", 3))

    return (1/price)*0.7 + rating*0.3


def rank_products(products):
    return sorted(products, key=score, reverse=True)