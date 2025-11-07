import { useState, useEffect } from 'react';
import ScheduleDisplay from '../components/ScheduleDisplay/ScheduleDisplay';
import api from '../services/api';
import './ResultsPage.css';

function ResultsPage({ onBack, selectedCourses, preferences, hardBreaks, softBreaks }) {
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    generateSchedules();
  }, []);

  const generateSchedules = async () => {
    setLoading(true);
    setError(null);

    try {
      // Convert selectedCourses to the format expected by API
      const courseCRNs = Object.values(selectedCourses).map(course => course.sections);

      const result = await api.generateSchedules({
        courses: courseCRNs,
        hard_breaks: hardBreaks,
        soft_breaks: softBreaks,
        preferences: preferences,
        limit: 200,
      });

      if (result.success) {
        setSchedules(result.schedules);
        if (result.schedules.length === 0) {
          setError('No valid schedules found with the given constraints. Try adjusting your break times or course selections.');
        }
      } else {
        setError(result.error || 'Failed to generate schedules');
      }
    } catch (err) {
      setError('Failed to generate schedules. Please check your backend connection.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="results-page">
      <div className="page-header">
        <button className="back-btn" onClick={onBack}>
          ← Back to Course Selection
        </button>
        <h1>Your Generated Schedules</h1>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Generating optimal schedules...</p>
          <p className="loading-detail">
            Analyzing {Object.keys(selectedCourses).length} courses and checking for conflicts
          </p>
        </div>
      )}

      {error && (
        <div className="error-container">
          <h3>Error</h3>
          <p>{error}</p>
          <button onClick={onBack}>Go Back</button>
        </div>
      )}

      {!loading && !error && schedules.length > 0 && (
        <>
          <div className="results-summary">
            <div className="summary-card">
              <div className="summary-label">Total Schedules</div>
              <div className="summary-value">{schedules.length}</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Best Score</div>
              <div className="summary-value">{schedules[0]?.score.toFixed(2)}</div>
            </div>
            <div className="summary-card">
              <div className="summary-label">Courses</div>
              <div className="summary-value">{Object.keys(selectedCourses).length}</div>
            </div>
          </div>

          <ScheduleDisplay schedules={schedules} />

          <div className="action-buttons">
            <button className="secondary-btn" onClick={onBack}>
              Modify Preferences
            </button>
            <button className="primary-btn" onClick={generateSchedules}>
              Regenerate Schedules
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default ResultsPage;
