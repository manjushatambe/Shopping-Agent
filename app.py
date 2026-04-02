import streamlit as st
import requests

# 🔗 Your Render backend URL
API_URL = "https://shopping-agent-a4rt.onrender.com//search"

st.markdown("""
<h1 style='margin-bottom: 0;'>ShopHopAI</h1>
<h4 style='margin-top: 0; color: gray;'>(Your Smart Shopping Assistant)</h4>
""", unsafe_allow_html=True)
st.write("Bored of scrolling multiple shopping sites? Get the best deals in one click! Powered by AI and web scraping magic. ✨")

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
                best_link = best.get("link", "#")
                st.markdown(f"""
                ### 🏆 [{best['title']}]({best_link})
                💰 **Price:** ₹{best['price']}  
                🏬 **Source:** {best['source']}
                [🔗 View Product]({best_link})
                """)
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