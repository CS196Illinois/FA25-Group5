import SliderItem from "./SliderItem";
import Dropdown from "./Dropdown";

type SliderItemType = {
  id: string;
  label: string;
  min?: number;
  max?: number;
  step?: number;
  initial?: number;
  type?: "slider" | "dropdown";
  options?: string[];
};

type CategoryConfig = {
  id: string;
  title: string;
  sliders: SliderItemType[];
};

type StepSliderProps = {
  categoriesLeft: CategoryConfig[];
  categoriesRight: CategoryConfig[];
};

export default function StepSlider({ categoriesLeft, categoriesRight }: StepSliderProps) {
  const renderCategory = (category: CategoryConfig) => (
    <div
      key={category.id}
      style={{
        backgroundColor: "#fff",
        borderRadius: 10,
        padding: 16,
        marginBottom: 20,
        boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
      }}
    >
      <div style={{ fontWeight: 700, fontSize: 20, marginBottom: 12 }}>{category.title}</div>

      {category.sliders.map((item) => {
        if (item.type === "dropdown") {
          return (
            <Dropdown
              key={item.id}
              id={item.id}
              label={item.label}
              options={item.options ?? []}
            />
          );
        }
        // default slider
        return (
          <SliderItem
            key={item.id}
            id={item.id}
            label={item.label}
            min={item.min ?? 1}
            max={item.max ?? 5}
            step={item.step ?? 1}
            initial={item.initial ?? item.min ?? 1}
          />
        );
      })}
    </div>
  );

  return (
    <div
      style={{
        display: "flex",
        gap: 20,
        width: "50%", // half-page
        padding: 24,
        boxSizing: "border-box",
      }}
    >
      <div style={{ flex: 1 }}>{categoriesLeft.map(renderCategory)}</div>
      <div style={{ flex: 1 }}>{categoriesRight.map(renderCategory)}</div>
    </div>
  );
}