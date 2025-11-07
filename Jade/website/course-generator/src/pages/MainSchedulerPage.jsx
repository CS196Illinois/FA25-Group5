import { useState } from 'react';
import CourseFilter from '../components/CourseFilter/CourseFilter';
import PreferenceSlider from '../components/PreferenceSlider/PreferenceSlider';
import BreakScheduler from '../components/BreakScheduler/BreakScheduler';
import './MainSchedulerPage.css';

function MainSchedulerPage({ onGenerate, selectedCourses, setSelectedCourses }) {
  const [filteredCourses, setFilteredCourses] = useState([]);
  const [selectedSections, setSelectedSections] = useState(selectedCourses || {});
  const [preferences, setPreferences] = useState({
    rmp_weight: 1.0,
    gpa_weight: 1.0,
    break_weight: 0.5,
    time_preference: 'compact',
  });
  const [hardBreaks, setHardBreaks] = useState([]);
  const [softBreaks, setSoftBreaks] = useState([]);

  const handleCoursesFiltered = (courses) => {
    setFilteredCourses(courses);
  };

  const handleCourseToggle = (course) => {
    const courseKey = `${course.Code}-${course.Number}`;

    setSelectedSections(prev => {
      const updated = { ...prev };

      if (!updated[courseKey]) {
        updated[courseKey] = {
          courseName: `${course.Code} ${course.Number} - ${course.Name}`,
          sections: [course.CRN],
        };
      } else {
        const sectionIndex = updated[courseKey].sections.indexOf(course.CRN);
        if (sectionIndex > -1) {
          updated[courseKey].sections.splice(sectionIndex, 1);
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

  const handlePreferencesChange = (newPreferences) => {
    setPreferences(newPreferences);
  };

  const handleBreaksChange = (newHardBreaks, newSoftBreaks) => {
    setHardBreaks(newHardBreaks);
    setSoftBreaks(newSoftBreaks);
  };

  const handleGenerate = () => {
    if (Object.keys(selectedSections).length === 0) {
      alert('Please select at least one course before generating schedules');
      return;
    }

    setSelectedCourses(selectedSections);
    onGenerate({
      preferences,
      hardBreaks,
      softBreaks,
    });
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
    <div className="main-scheduler-page">
      <h1>Course Schedule Generator</h1>
      <p className="page-description">
        Select your courses and set your preferences to generate optimal schedules
      </p>

      <div className="scheduler-layout">
        {/* Left side - Course Selection */}
        <div className="left-panel">
          <h2>1. Select Courses</h2>

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

        {/* Right side - Preferences */}
        <div className="right-panel">
          <h2>2. Set Preferences</h2>

          <PreferenceSlider onPreferencesChange={handlePreferencesChange} />

          <BreakScheduler onBreaksChange={handleBreaksChange} />

          <div className="generate-section">
            <button
              className="generate-btn"
              onClick={handleGenerate}
              disabled={Object.keys(selectedSections).length === 0}
            >
              Generate Schedules
            </button>
            <p className="generate-note">
              {Object.keys(selectedSections).length === 0
                ? 'Select courses to generate schedules'
                : `Generate up to 200 schedules for ${Object.keys(selectedSections).length} course(s)`
              }
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MainSchedulerPage;
