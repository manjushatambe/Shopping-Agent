import React from "react";

export default function ProductCard({ product }) {
  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "10px",
      padding: "10px",
      margin: "10px 0",
      background: "#fafafa"
    }}>
      <h4>{product.title}</h4>
      <p>💰 ₹{product.price}</p>
      {product.rating && <p>⭐ {product.rating}</p>}
      <p style={{ fontSize: "12px", color: "gray" }}>
        Source: {product.source}
      </p>

      {product.link && (
        <a href={product.link} target="_blank" rel="noreferrer">
          <button>Buy</button>
        </a>
      )}
    </div>
  );
}