import StepSlider from "./components/StepSlider";
import Button from "./components/Button";
import CourseSearch from "./components/CourseSearch";
import Header from "./components/Header"; // New header component
import { useNavigate } from "react-router-dom"; // Assuming you are using react-router

function App() {
  const navigate = useNavigate();

  const goToNextPage = () => {
    navigate("/next"); // Adjust route as needed
  };

  return (
    <div
      style={{
        padding: 24,
        fontFamily: "Arial, sans-serif",
        backgroundColor: "#f5f5f5",
        minHeight: "100vh",
      }}
    >
      {/* Header */}
      <Header
        title="Course Planning Dashboard"
        subtitle="Customize your preferences and search courses"
      />

      {/* Main content */}
      <div style={{ display: "flex", gap: 24, marginTop: 24 }}>
        {/* Left-hand StepSlider */}
        <div
          style={{
            flex: 1,
            backgroundColor: "#fff",
            padding: 24,
            borderRadius: 12,
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          }}
        >
          <Button onClick={goToNextPage} style={{ marginBottom: 16 }}>
            Next Page
          </Button>
          <StepSlider
            categoriesLeft={[
              {
                id: "professor",
                title: "Professor",
                sliders: [
                  {
                    id: "prof_main",
                    label: "Professor Overall",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "rate_my_prof",
                    label: "Rate My Professor Rating",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "excellent_rating",
                    label: "Excellent Rating",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "outstanding_rating",
                    label: "Outstanding Rating",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                ],
              },
              {
                id: "class_difficulty",
                title: "Class Difficulty",
                sliders: [
                  {
                    id: "class_diff",
                    label: "Class Difficulty",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "prof_avg_gpa",
                    label: "Professor Average GPA",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "class_avg_gpa",
                    label: "Class Average GPA",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "min_grade",
                    label: "Minimum Acceptable Grade",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "grade_dropdown",
                    label: "Select Grade",
                    type: "dropdown",
                    options: [
                      "A+",
                      "A",
                      "A-",
                      "B+",
                      "B",
                      "B-",
                      "C+",
                      "C",
                      "C-",
                      "D+",
                      "D",
                      "D-",
                      "F",
                    ],
                  },
                ],
              },
            ]}
            categoriesRight={[
              {
                id: "passing_period",
                title: "Passing Period",
                sliders: [
                  {
                    id: "passing_period_main",
                    label: "Passing Period",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                  {
                    id: "late_tolerance",
                    label: "How Long Are You Willing to Be Late (min)",
                    min: 0,
                    max: 30,
                    initial: 10,
                  },
                ],
              },
              {
                id: "general_location",
                title: "General Location",
                sliders: [
                  {
                    id: "preferred_area",
                    label: "Preferred General Area",
                    type: "dropdown",
                    options: ["A", "B", "C", "D", "E", "F", "G"],
                  },
                  {
                    id: "num_blocks",
                    label: "Number of Blocks",
                    min: 1,
                    max: 10,
                    initial: 5,
                  },
                ],
              },
              {
                id: "soft_breaks",
                title: "Soft Breaks",
                sliders: [
                  {
                    id: "soft_breaks_main",
                    label: "Soft Breaks",
                    min: 1,
                    max: 5,
                    initial: 3,
                  },
                ],
              },
            ]}
          />
        </div>

        {/* Right-hand Course Search */}
        <div
          style={{
            flex: 1,
            backgroundColor: "#fff",
            padding: 24,
            borderRadius: 12,
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          }}
        >
          <CourseSearch />
        </div>
      </div>
    </div>
  );
}

export default App;
