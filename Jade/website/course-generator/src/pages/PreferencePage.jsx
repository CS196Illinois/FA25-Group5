import { useState } from 'react';
import PreferenceSlider from '../components/PreferenceSlider/PreferenceSlider';
import BreakScheduler from '../components/BreakScheduler/BreakScheduler';
import './PreferencePage.css';

function PreferencePage({ onBack, onGenerate, selectedCourses }) {
  const [preferences, setPreferences] = useState({
    rmp_weight: 1.0,
    gpa_weight: 1.0,
    break_weight: 0.5,
    time_preference: 'compact',
  });
  const [hardBreaks, setHardBreaks] = useState([]);
  const [softBreaks, setSoftBreaks] = useState([]);

  const handlePreferencesChange = (newPreferences) => {
    setPreferences(newPreferences);
  };

  const handleBreaksChange = (newHardBreaks, newSoftBreaks) => {
    setHardBreaks(newHardBreaks);
    setSoftBreaks(newSoftBreaks);
  };

  const handleGenerate = () => {
    onGenerate({
      preferences,
      hardBreaks,
      softBreaks,
    });
  };

  return (
    <div className="preference-page">
      <div className="page-header">
        <button className="back-btn" onClick={onBack}>
          ← Back to Course Selection
        </button>
        <h1>Set Your Preferences</h1>
        <p className="page-description">
          Customize your schedule generation preferences and add any time blocks you want free
        </p>
      </div>

      <div className="selected-courses-summary">
        <h3>Selected Courses</h3>
        <div className="courses-list">
          {Object.entries(selectedCourses).map(([key, course]) => (
            <div key={key} className="course-item">
              {course.courseName}
              <span className="badge">{course.sections.length} section(s)</span>
            </div>
          ))}
        </div>
      </div>

      <PreferenceSlider onPreferencesChange={handlePreferencesChange} />

      <BreakScheduler onBreaksChange={handleBreaksChange} />

      <div className="generate-section">
        <button className="generate-btn" onClick={handleGenerate}>
          Generate Schedules
        </button>
        <p className="generate-note">
          This will generate up to 200 possible schedules ranked by your preferences
        </p>
      </div>
    </div>
  );
}

export default PreferencePage;
