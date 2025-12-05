function Button({ children, onClick, style }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "10px 20px",
        backgroundColor: "#4CAF50",
        color: "#fff",
        border: "none",
        borderRadius: 6,
        cursor: "pointer",
        fontSize: 16,
        transition: "background-color 0.3s",
        ...style,
      }}
      onMouseEnter={(e) => (e.target.style.backgroundColor = "#45a049")}
      onMouseLeave={(e) => (e.target.style.backgroundColor = "#4CAF50")}
    >
      {children}
    </button>
  );
}

export default Button;
