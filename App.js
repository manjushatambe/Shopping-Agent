import React, { useState } from 'react';
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
      const why = data.result.why;

      const reply = `
🛍️ Best Product:
${best?.title}
💰 Price: ₹${best?.price}

🤖 Why:
${why}`;

      setMessages([...newMessages, { role: "assistant", content: reply }]);
    } catch (err) {
      setMessages([...newMessages, { role: "assistant", content: "Error fetching results." }]);
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h2>🧠 AI Shopping Agent</h2>

      <div style={{ border: "1px solid #ccc", padding: 10, height: 400, overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === "user" ? "right" : "left" }}>
            <p><b>{msg.role === "user" ? "You" : "AI"}:</b> {msg.content}</p>
          </div>
        ))}
        {loading && <p>AI is thinking...</p>}
      </div>

      <div style={{ marginTop: 10, display: "flex" }}>
        <input
          style={{ flex: 1, padding: 10 }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something like: best phone under 50000"
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
