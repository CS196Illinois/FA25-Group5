import { useState } from "react";

// Dummy POST request function
const postRequest = async (url: string, data: any) => {
  console.log(`POST request to ${url} with data:`, data);
  // Simulate network delay
  return new Promise<{ results: string[] }>((resolve) =>
    setTimeout(() => resolve({ results: [`Result 1 for ${data.query}`, `Result 2 for ${data.query}`] }), 500)
  );
};

export default function CourseSearch() {
  const [subjectCode, setSubjectCode] = useState("");
  const [courseNumber, setCourseNumber] = useState("");
  const [searchResults, setSearchResults] = useState<string[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<string[]>([]);

  // Search by subject code
  const searchBySubjectCode = async () => {
    const response = await postRequest("/search/subject", { query: subjectCode });
    setSearchResults(response.results);
  };

  // Search by course number
  const searchByCourseNumber = async () => {
    const response = await postRequest("/search/number", { query: courseNumber });
    setSearchResults(response.results);
  };

  const addCourse = (course: string) => {
    if (!selectedCourses.includes(course)) {
      setSelectedCourses((prev) => [...prev, course]);
    }
  };

  return (
    <div style={{ width: "50%", padding: 24 }}>
      <div
        style={{
          backgroundColor: "#fff",
          borderRadius: 10,
          padding: 16,
          marginBottom: 20,
          boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
        }}
      >
        <h2 style={{ fontWeight: 700, fontSize: 20, marginBottom: 12 }}>Search Courses</h2>

        {/* Subject Code Search */}
        <div style={{ marginBottom: 16 }}>
          <label style={{ fontWeight: 600, display: "block", marginBottom: 6 }}>Subject Code</label>
          <input
            type="text"
            value={subjectCode}
            onChange={(e) => setSubjectCode(e.target.value)}
            style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #ccc" }}
          />
          <button
            onClick={searchBySubjectCode}
            style={{
              marginTop: 8,
              padding: "6px 12px",
              borderRadius: 6,
              backgroundColor: "#4f46e5",
              color: "#fff",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Search
          </button>
        </div>

        {/* Course Number Search */}
        <div style={{ marginBottom: 16 }}>
          <label style={{ fontWeight: 600, display: "block", marginBottom: 6 }}>Course Number</label>
          <input
            type="text"
            value={courseNumber}
            onChange={(e) => setCourseNumber(e.target.value)}
            style={{ width: "100%", padding: "8px 12px", borderRadius: 6, border: "1px solid #ccc" }}
          />
          <button
            onClick={searchByCourseNumber}
            style={{
              marginTop: 8,
              padding: "6px 12px",
              borderRadius: 6,
              backgroundColor: "#4f46e5",
              color: "#fff",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Search
          </button>
        </div>

        {/* Search Results */}
        <div style={{ marginTop: 16 }}>
          <h3 style={{ fontWeight: 600, marginBottom: 8 }}>Search Results</h3>
          {searchResults.length === 0 ? (
            <p style={{ fontStyle: "italic", color: "#666" }}>No results</p>
          ) : (
            <ul>
              {searchResults.map((course) => (
                <li key={course} style={{ marginBottom: 4 }}>
                  {course}{" "}
                  <button
                    onClick={() => addCourse(course)}
                    style={{
                      marginLeft: 8,
                      padding: "2px 6px",
                      borderRadius: 4,
                      fontSize: 12,
                      backgroundColor: "#4f46e5",
                      color: "#fff",
                      cursor: "pointer",
                    }}
                  >
                    Add
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>

      {/* Selected Courses */}
      <div
        style={{
          backgroundColor: "#fff",
          borderRadius: 10,
          padding: 16,
          boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
        }}
      >
        <h3 style={{ fontWeight: 700, fontSize: 18, marginBottom: 12 }}>Selected Courses</h3>
        {selectedCourses.length === 0 ? (
          <p style={{ fontStyle: "italic", color: "#666" }}>No courses selected</p>
        ) : (
          <ul>
            {selectedCourses.map((course) => (
              <li key={course}>{course}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
