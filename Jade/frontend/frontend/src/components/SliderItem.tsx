import { useState } from "react";

type SliderProps = {
  id: string;
  label: string;
  min: number;
  max: number;
  step?: number;
  initial?: number;
  onChange?: (value: number) => void;
};

export default function SliderItem({ id, label, min, max, step = 1, initial = min, onChange }: SliderProps) {
  const [value, setValue] = useState<number>(initial);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVal = Number(e.target.value);
    setValue(newVal);
    if (onChange) onChange(newVal);
  };

  return (
    <div style={{ marginBottom: 20 }}>
      <label htmlFor={id} style={{ fontWeight: 600, fontSize: 16, display: "block", marginBottom: 6 }}>
        {label}
      </label>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={handleChange}
        style={{
          width: "100%",
          marginTop: 6,
          height: 8,
          borderRadius: 4,
          accentColor: "#4f46e5",
        }}
      />
      <div style={{ marginTop: 6, fontWeight: 500, color: "#333" }}>Value: {value}</div>
    </div>
  );
}
