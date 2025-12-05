function Header({ title, subtitle }) {
  return (
    <div style={{ textAlign: "center", marginBottom: 24 }}>
      <h1 style={{ fontSize: "2rem", margin: 0, color: "#333" }}>{title}</h1>
      <p style={{ fontSize: "1rem", color: "#666", marginTop: 8 }}>{subtitle}</p>
    </div>
  );
}

export default Header;