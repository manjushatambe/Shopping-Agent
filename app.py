import streamlit as st
from agents.search_agent import search_products

st.title("🛒 Shopping Agent Demo")
query = st.text_input("Search for a product:", "iPhone")

if st.button("Search"):
    with st.spinner("Fetching products..."):
        products = search_products(query)

        # Ensure products["all"] exists
        all_products = products.get("all", [])
        if not all_products:
            st.warning("No products found, showing fallback data.")

        # Display all products
        for prod in all_products:
            st.write(f"**{prod['title']}** ({prod['source']}) — ₹{prod['price']}")

        st.markdown("### Why this product?")
        st.info(products.get("why", "No explanation available."))