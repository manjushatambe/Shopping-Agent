import React, { useState } from "react";
import ProductCard from "./ProductCard";

function App() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi 👋 I’m your AI shopping assistant. What are you looking for?" }
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`https://shopping-agent-eqkj.onrender.com/search?q=${input}`);
      const data = await res.json();

      const best = data.result.best;
      const all = data.result.all || [];
      const why = data.result.why;

      // 🧠 Assistant response with products
      setMessages([
        ...newMessages,
        {
          role: "assistant",
          content: why || "Here are the best options I found:",
          products: all,
          best: best
        }
      ]);

    } catch (err) {
      setMessages([
        ...newMessages,
        { role: "assistant", content: "❌ Error fetching results." }
      ]);
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 700, margin: "auto", padding: 20 }}>
      <h2>🧠 AI Shopping Agent</h2>

      {/* Chat box */}
      <div style={{
        border: "1px solid #ccc",
        padding: 10,
        height: 400,
        overflowY: "auto",
        borderRadius: 10
      }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.role === "user" ? "right" : "left",
              marginBottom: 10
            }}
          >
            <p><b>{msg.role === "user" ? "You" : "AI"}:</b></p>

            {/* Text message */}
            {msg.content && <p>{msg.content}</p>}

            {/* 🔥 Product widgets */}
            {msg.products && msg.products.map((p, idx) => (
              <div
                key={idx}
                style={{
                  border: p.title === msg.best?.title
                    ? "2px solid green"
                    : "none"
                }}
              >
                <ProductCard product={p} />
              </div>
            ))}
          </div>
        ))}

        {loading && <p>🤖 AI is thinking...</p>}
      </div>

      {/* Input */}
      <div style={{ marginTop: 10, display: "flex" }}>
        <input
          style={{ flex: 1, padding: 10, borderRadius: 6 }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask: best phone under 50000"
        />

        <button
          onClick={sendMessage}
          style={{
            marginLeft: 10,
            padding: "10px 15px",
            borderRadius: 6,
            cursor: "pointer"
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;