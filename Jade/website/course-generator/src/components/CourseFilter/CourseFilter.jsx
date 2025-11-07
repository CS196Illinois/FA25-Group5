import { useState, useEffect } from 'react';
import api from '../../services/api';
import './CourseFilter.css';

function CourseFilter({ onCoursesFiltered }) {
  const [subjects, setSubjects] = useState([]);
  const [filters, setFilters] = useState({
    subject: '',
    number: '',
    instructor: '',
    days: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSubjects();
  }, []);

  const loadSubjects = async () => {
    try {
      const result = await api.getSubjects();
      if (result.success) {
        setSubjects(result.subjects);
      }
    } catch (err) {
      setError('Failed to load subjects');
      console.error(err);
    }
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const activeFilters = Object.entries(filters).reduce((acc, [key, value]) => {
        if (value) acc[key] = value;
        return acc;
      }, {});

      const result = await api.getCourses(activeFilters);

      if (result.success) {
        onCoursesFiltered(result.courses);
      } else {
        setError(result.error || 'Failed to fetch courses');
      }
    } catch (err) {
      setError('Failed to fetch courses');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFilters({
      subject: '',
      number: '',
      instructor: '',
      days: '',
    });
    onCoursesFiltered([]);
  };

  return (
    <div className="course-filter">
      <h2>Filter Courses</h2>

      <form onSubmit={handleSearch}>
        <div className="filter-row">
          <div className="filter-field">
            <label htmlFor="subject">Subject</label>
            <select
              id="subject"
              value={filters.subject}
              onChange={(e) => handleFilterChange('subject', e.target.value)}
            >
              <option value="">All Subjects</option>
              {subjects.map(subject => (
                <option key={subject} value={subject}>
                  {subject}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-field">
            <label htmlFor="number">Course Number</label>
            <input
              id="number"
              type="text"
              placeholder="e.g., 225"
              value={filters.number}
              onChange={(e) => handleFilterChange('number', e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label htmlFor="instructor">Instructor</label>
            <input
              id="instructor"
              type="text"
              placeholder="Last name or initial"
              value={filters.instructor}
              onChange={(e) => handleFilterChange('instructor', e.target.value)}
            />
          </div>

          <div className="filter-field">
            <label htmlFor="days">Days</label>
            <input
              id="days"
              type="text"
              placeholder="e.g., MWF"
              value={filters.days}
              onChange={(e) => handleFilterChange('days', e.target.value)}
            />
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="filter-actions">
          <button type="submit" disabled={loading}>
            {loading ? 'Searching...' : 'Search Courses'}
          </button>
          <button type="button" onClick={handleReset}>
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}

export default CourseFilter;
