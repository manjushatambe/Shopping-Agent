
import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);

  const search = async () => {
    const res = await fetch(`https://shopping-agent-eqkj.onrender.com/search?q=${query}`);
    const data = await res.json();
    setResults(data.result);
  };

  return (
    <div style={{padding: 20}}>
      <h1>Shopping AI Agent</h1>

      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Search product"
      />

      <button onClick={search}>Search</button>

      {results && (
        <div>
          <h2>Best Product</h2>
          <p>{results.best.title}</p>
          <p>₹{results.best.price}</p>

          <h3>Why?</h3>
          <p>{results.why}</p>

          <h2>All Results</h2>
          {results.all.map((p, i) => (
            <div key={i}>
              <p>{p.title} - ₹{p.price}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

