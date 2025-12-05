import { useState } from "react";

type DropdownProps = {
  id: string;
  label: string;
  options: string[];
  initial?: string;
  onChange?: (value: string) => void;
};

export default function Dropdown({ id, label, options, initial, onChange }: DropdownProps) {
  const [selected, setSelected] = useState<string>(initial ?? options[0]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelected(e.target.value);
    if (onChange) onChange(e.target.value);
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <label
        htmlFor={id}
        style={{ display: "block", fontWeight: 600, fontSize: 16, marginBottom: 6 }}
      >
        {label}
      </label>
      <select
        id={id}
        value={selected}
        onChange={handleChange}
        style={{
          width: "100%",
          padding: "8px 12px",
          borderRadius: 6,
          border: "1px solid #ccc",
          fontSize: 16,
          backgroundColor: "#fff",
        }}
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
      <div style={{ marginTop: 6, fontWeight: 500, color: "#333" }}>Selected: {selected}</div>
    </div>
  );
}
