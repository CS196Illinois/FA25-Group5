import { useState } from 'react';
import './BreakScheduler.css';

function BreakScheduler({ onBreaksChange }) {
  const [hardBreaks, setHardBreaks] = useState([]);
  const [softBreaks, setSoftBreaks] = useState([]);
  const [showAddBreak, setShowAddBreak] = useState(false);
  const [breakType, setBreakType] = useState('hard');
  const [newBreak, setNewBreak] = useState({
    days: '',
    start: '',
    end: '',
  });

  const daysOptions = [
    { value: 'M', label: 'Monday' },
    { value: 'T', label: 'Tuesday' },
    { value: 'W', label: 'Wednesday' },
    { value: 'R', label: 'Thursday' },
    { value: 'F', label: 'Friday' },
  ];

  const handleAddBreak = () => {
    if (!newBreak.days || !newBreak.start || !newBreak.end) {
      alert('Please fill in all fields');
      return;
    }

    const breakToAdd = { ...newBreak };

    if (breakType === 'hard') {
      setHardBreaks([...hardBreaks, breakToAdd]);
    } else {
      setSoftBreaks([...softBreaks, breakToAdd]);
    }

    // Update parent component
    onBreaksChange(
      breakType === 'hard' ? [...hardBreaks, breakToAdd] : hardBreaks,
      breakType === 'soft' ? [...softBreaks, breakToAdd] : softBreaks
    );

    // Reset form
    setNewBreak({ days: '', start: '', end: '' });
    setShowAddBreak(false);
  };

  const handleRemoveBreak = (type, index) => {
    if (type === 'hard') {
      const updated = hardBreaks.filter((_, i) => i !== index);
      setHardBreaks(updated);
      onBreaksChange(updated, softBreaks);
    } else {
      const updated = softBreaks.filter((_, i) => i !== index);
      setSoftBreaks(updated);
      onBreaksChange(hardBreaks, updated);
    }
  };

  const handleDayToggle = (day) => {
    const days = newBreak.days.split('');
    if (days.includes(day)) {
      setNewBreak({
        ...newBreak,
        days: days.filter(d => d !== day).join(''),
      });
    } else {
      setNewBreak({
        ...newBreak,
        days: [...days, day].sort((a, b) => {
          const order = ['M', 'T', 'W', 'R', 'F'];
          return order.indexOf(a) - order.indexOf(b);
        }).join(''),
      });
    }
  };

  const formatBreakTime = (breakItem) => {
    return `${breakItem.days} ${breakItem.start}-${breakItem.end}`;
  };

  return (
    <div className="break-scheduler">
      <h3>Schedule Breaks</h3>
      <p className="break-description">
        Add time blocks when you prefer not to have classes
      </p>

      <div className="break-types">
        <div className="break-type-section">
          <h4>Hard Breaks (Must be free)</h4>
          <div className="break-list">
            {hardBreaks.length === 0 ? (
              <p className="no-breaks">No hard breaks set</p>
            ) : (
              hardBreaks.map((breakItem, index) => (
                <div key={index} className="break-item hard">
                  <span>{formatBreakTime(breakItem)}</span>
                  <button onClick={() => handleRemoveBreak('hard', index)}>
                    Remove
                  </button>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="break-type-section">
          <h4>Soft Breaks (Prefer to be free)</h4>
          <div className="break-list">
            {softBreaks.length === 0 ? (
              <p className="no-breaks">No soft breaks set</p>
            ) : (
              softBreaks.map((breakItem, index) => (
                <div key={index} className="break-item soft">
                  <span>{formatBreakTime(breakItem)}</span>
                  <button onClick={() => handleRemoveBreak('soft', index)}>
                    Remove
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {!showAddBreak ? (
        <button className="add-break-btn" onClick={() => setShowAddBreak(true)}>
          + Add Break
        </button>
      ) : (
        <div className="add-break-form">
          <h4>Add New Break</h4>

          <div className="form-group">
            <label>Break Type</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  value="hard"
                  checked={breakType === 'hard'}
                  onChange={(e) => setBreakType(e.target.value)}
                />
                Hard Break (must be free)
              </label>
              <label>
                <input
                  type="radio"
                  value="soft"
                  checked={breakType === 'soft'}
                  onChange={(e) => setBreakType(e.target.value)}
                />
                Soft Break (prefer to be free)
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Days</label>
            <div className="day-selector">
              {daysOptions.map(day => (
                <button
                  key={day.value}
                  type="button"
                  className={`day-btn ${newBreak.days.includes(day.value) ? 'selected' : ''}`}
                  onClick={() => handleDayToggle(day.value)}
                >
                  {day.value}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group time-inputs">
            <div>
              <label htmlFor="start-time">Start Time</label>
              <input
                id="start-time"
                type="time"
                value={newBreak.start}
                onChange={(e) => setNewBreak({ ...newBreak, start: e.target.value })}
              />
            </div>
            <div>
              <label htmlFor="end-time">End Time</label>
              <input
                id="end-time"
                type="time"
                value={newBreak.end}
                onChange={(e) => setNewBreak({ ...newBreak, end: e.target.value })}
              />
            </div>
          </div>

          <div className="form-actions">
            <button className="save-btn" onClick={handleAddBreak}>
              Save Break
            </button>
            <button className="cancel-btn" onClick={() => {
              setShowAddBreak(false);
              setNewBreak({ days: '', start: '', end: '' });
            }}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default BreakScheduler;
