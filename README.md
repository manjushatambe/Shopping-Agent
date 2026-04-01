# 🛒 AI Shopping Agent

An intelligent shopping assistant that scrapes multiple e-commerce platforms, ranks products, and recommends the best option based on price and relevance.

---

## 🚀 Features

* 🔍 Search products across multiple platforms (Amazon, Flipkart, etc.)
* 🤖 AI-powered product ranking
* ⚡ FastAPI backend with modular agents
* 🌐 Streamlit frontend (optional)
* 🛡️ Fallback system when scrapers fail
* 🧠 Scalable agent-based architecture

---

## 🏗️ Architecture

```
User Query
   ↓
Search Agent
   ↓
Scrapers (Amazon, Flipkart, etc.)
   ↓
Data Aggregation
   ↓
Rank Agent
   ↓
Best Product Recommendation
```

---

## 📁 Project Structure

```
Shopping-Agent/
├── agents/
│   ├── controller.py
│   ├── search_agent.py
│   ├── rank_agent.py
│   └── fallback.py
├── scrapers/
│   ├── runner.py
│   ├── amazon.py
│   ├── flipkart.py
│   └── other scrapers...
├── main.py
├── app.py (Streamlit UI)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone https://github.com/manjushatambe/Shopping-Agent.git
cd Shopping-Agent
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Install Playwright browsers (for scraping)

```
playwright install
```

---

### 4️⃣ Run backend (FastAPI)

```
uvicorn main:app --reload
```

API will be available at:

```
http://127.0.0.1:8000
```

---

### 5️⃣ Test API

```
http://127.0.0.1:8000/search?q=iphone
```

---

### 6️⃣ Run frontend (Streamlit)

```
streamlit run app.py
```

---

## 🌍 Deployment

### Backend (Render)

* Deploy FastAPI using:

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Streamlit Cloud)

* Connect GitHub repo
* Deploy `app.py`

---

## ⚠️ Notes

* Some websites may block scraping (Flipkart, Amazon in cloud environments)
* Fallback data is used when scraping fails
* For best results, run locally or on Docker-based platforms (Render, Fly.io)

---

## 🧠 Future Improvements

* Add product images
* Integrate more e-commerce platforms
* Use LLM for smarter recommendations
* Add filters (price, rating, brand)
* Cache results for faster responses

---

## 🤝 Contributing

Feel free to fork the repo and submit pull requests!

---

## 📄 License

This project is for educational and portfolio purposes.

---

## 👨‍💻 Author

**Manjusha Tambe**

---

⭐ If you found this project useful, give it a star!
