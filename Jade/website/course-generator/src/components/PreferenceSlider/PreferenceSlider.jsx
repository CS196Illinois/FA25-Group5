import { useState } from 'react';
import './PreferenceSlider.css';

function PreferenceSlider({ onPreferencesChange }) {
  const [preferences, setPreferences] = useState({
    rmp_weight: 1.0,
    gpa_weight: 1.0,
    break_weight: 0.5,
    time_preference: 'compact', // 'early', 'late', 'compact'
  });

  const handleSliderChange = (field, value) => {
    const newPreferences = { ...preferences, [field]: parseFloat(value) };
    setPreferences(newPreferences);
    onPreferencesChange(newPreferences);
  };

  const handleTimePreferenceChange = (value) => {
    const newPreferences = { ...preferences, time_preference: value };
    setPreferences(newPreferences);
    onPreferencesChange(newPreferences);
  };

  return (
    <div className="preference-slider">
      <h3>Schedule Preferences</h3>
      <p className="preference-description">
        Adjust these sliders to prioritize what matters most to you in your schedule
      </p>

      <div className="preference-group">
        <div className="preference-item">
          <label htmlFor="rmp-weight">
            RateMyProfessor Score
            <span className="preference-value">{preferences.rmp_weight.toFixed(1)}</span>
          </label>
          <input
            id="rmp-weight"
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={preferences.rmp_weight}
            onChange={(e) => handleSliderChange('rmp_weight', e.target.value)}
          />
          <div className="preference-labels">
            <span>Less Important</span>
            <span>More Important</span>
          </div>
        </div>

        <div className="preference-item">
          <label htmlFor="gpa-weight">
            Average GPA
            <span className="preference-value">{preferences.gpa_weight.toFixed(1)}</span>
          </label>
          <input
            id="gpa-weight"
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={preferences.gpa_weight}
            onChange={(e) => handleSliderChange('gpa_weight', e.target.value)}
          />
          <div className="preference-labels">
            <span>Less Important</span>
            <span>More Important</span>
          </div>
        </div>

        <div className="preference-item">
          <label htmlFor="break-weight">
            Avoid Preferred Break Times
            <span className="preference-value">{preferences.break_weight.toFixed(1)}</span>
          </label>
          <input
            id="break-weight"
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={preferences.break_weight}
            onChange={(e) => handleSliderChange('break_weight', e.target.value)}
          />
          <div className="preference-labels">
            <span>Less Important</span>
            <span>More Important</span>
          </div>
        </div>
      </div>

      <div className="time-preference-group">
        <h4>Time Preference</h4>
        <div className="radio-group">
          <label className="radio-option">
            <input
              type="radio"
              name="time_preference"
              value="early"
              checked={preferences.time_preference === 'early'}
              onChange={(e) => handleTimePreferenceChange(e.target.value)}
            />
            <span>Early classes (morning)</span>
          </label>

          <label className="radio-option">
            <input
              type="radio"
              name="time_preference"
              value="late"
              checked={preferences.time_preference === 'late'}
              onChange={(e) => handleTimePreferenceChange(e.target.value)}
            />
            <span>Late classes (afternoon)</span>
          </label>

          <label className="radio-option">
            <input
              type="radio"
              name="time_preference"
              value="compact"
              checked={preferences.time_preference === 'compact'}
              onChange={(e) => handleTimePreferenceChange(e.target.value)}
            />
            <span>Compact schedule (classes close together)</span>
          </label>
        </div>
      </div>
    </div>
  );
}

export default PreferenceSlider;
