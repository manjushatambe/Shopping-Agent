import streamlit as st
import requests

# 🔗 Your Render backend URL
API_URL = "https://shopping-agent-a4rt.onrender.com//search"

st.set_page_config(page_title="Shopping Agent", page_icon="🛒")

st.title("🛒 AI Shopping Agent")
st.write("Find the best product across multiple websites")

# 🔍 Search input
query = st.text_input("Enter product (e.g. iPhone, laptop, headphones)")

if st.button("Search") and query:

    with st.spinner("Searching across stores... 🔍"):
        try:
            response = requests.get(API_URL, params={"q": query})
            data = response.json()

            products = data.get("result", {})

            # ✅ Best product
            best = products.get("best")
            all_products = products.get("all", [])
            why = products.get("why", "")

            if best:
                st.subheader("🏆 Best Choice")
                st.success(f"{best['title']} — ₹{best['price']}")

                st.markdown("**Why this?**")
                st.info(why)

            # 🛍️ All products
            st.subheader("🛍️ All Results")

            if all_products:
                for p in all_products:
                    link = p.get("link", "#")
                    st.write(
                        f"• [{p['title']}]({link}) — ₹{p['price']} ({p['source']})"
                    )
                    #st.write(f"• {p['title']} — ₹{p['price']} ({p['source']})")
            else:
                st.warning("No products found")

        except Exception as e:
            st.error(f"Error: {e}")