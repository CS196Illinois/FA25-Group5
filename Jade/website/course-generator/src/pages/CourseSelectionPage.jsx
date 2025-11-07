import { useState } from 'react';
import CourseFilter from '../components/CourseFilter/CourseFilter';
import './CourseSelectionPage.css';

function CourseSelectionPage({ onContinue, selectedCourses, setSelectedCourses }) {
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [selectedSections, setSelectedSections] = useState(selectedCourses || {});

  const handleCoursesFiltered = (courses) => {
    setFilteredCourses(courses);
  };

  const handleCourseToggle = (course) => {
    const courseKey = `${course.Code}-${course.Number}`;

    setSelectedSections(prev => {
      const updated = { ...prev };

      if (!updated[courseKey]) {
        // First section of this course
        updated[courseKey] = {
          courseName: `${course.Code} ${course.Number} - ${course.Name}`,
          sections: [course.CRN],
        };
      } else {
        // Toggle section
        const sectionIndex = updated[courseKey].sections.indexOf(course.CRN);
        if (sectionIndex > -1) {
          updated[courseKey].sections.splice(sectionIndex, 1);
          // Remove course if no sections selected
          if (updated[courseKey].sections.length === 0) {
            delete updated[courseKey];
          }
        } else {
          updated[courseKey].sections.push(course.CRN);
        }
      }

      return updated;
    });
  };

  const isSectionSelected = (crn) => {
    return Object.values(selectedSections).some(course =>
      course.sections.includes(crn)
    );
  };

  const handleContinue = () => {
    setSelectedCourses(selectedSections);
    onContinue();
  };

  const groupedCourses = filteredCourses.reduce((acc, course) => {
    const key = `${course.Code}-${course.Number}`;
    if (!acc[key]) {
      acc[key] = {
        code: course.Code,
        number: course.Number,
        name: course.Name,
        sections: [],
      };
    }
    acc[key].sections.push(course);
    return acc;
  }, {});

  return (
    <div className="course-selection-page">
      <h1>Select Your Courses</h1>
      <p className="page-description">
        Search for courses and select the sections you want to include in your schedule.
        You can select multiple sections per course to see all possible schedule combinations.
      </p>

      <CourseFilter onCoursesFiltered={handleCoursesFiltered} />

      {Object.keys(selectedSections).length > 0 && (
        <div className="selected-summary">
          <h3>Selected Courses ({Object.keys(selectedSections).length})</h3>
          <div className="selected-list">
            {Object.entries(selectedSections).map(([key, course]) => (
              <div key={key} className="selected-item">
                <strong>{course.courseName}</strong>
                <span className="section-count">
                  {course.sections.length} section{course.sections.length > 1 ? 's' : ''}
                </span>
              </div>
            ))}
          </div>
          <button className="continue-btn" onClick={handleContinue}>
            Continue to Preferences
          </button>
        </div>
      )}

      <div className="courses-results">
        {filteredCourses.length > 0 ? (
          <>
            <h3>Search Results ({filteredCourses.length} sections)</h3>
            <div className="courses-grouped">
              {Object.entries(groupedCourses).map(([key, course]) => (
                <div key={key} className="course-group">
                  <div className="course-group-header">
                    <h4>{course.code} {course.number}</h4>
                    <p>{course.name}</p>
                  </div>
                  <div className="course-sections">
                    {course.sections.map(section => (
                      <div
                        key={section.CRN}
                        className={`course-section ${isSectionSelected(section.CRN) ? 'selected' : ''}`}
                        onClick={() => handleCourseToggle(section)}
                      >
                        <div className="section-info">
                          <span className="section-crn">CRN: {section.CRN}</span>
                          <span className="section-type">{section['Sched Type']}</span>
                          <span className="section-days">{section['Days of Week']}</span>
                          <span className="section-time">
                            {section['Start Time']} - {section['End Time']}
                          </span>
                        </div>
                        <div className="section-details">
                          <span className="section-instructor">
                            {section['Primary Instructor (Concat)']}
                          </span>
                          {section.RMP && (
                            <span className="section-rmp">RMP: {section.RMP}/5.0</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="no-results">
            <p>Use the filters above to search for courses</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default CourseSelectionPage;
