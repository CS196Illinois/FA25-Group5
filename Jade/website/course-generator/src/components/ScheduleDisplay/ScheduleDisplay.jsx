import { useState } from 'react';
import './ScheduleDisplay.css';

function ScheduleDisplay({ schedules }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  if (!schedules || schedules.length === 0) {
    return (
      <div className="schedule-display empty">
        <p>No schedules to display. Generate schedules to see results.</p>
      </div>
    );
  }

  const currentSchedule = schedules[currentIndex];
  const timeSlots = generateTimeSlots();
  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  const dayMap = { M: 0, T: 1, W: 2, R: 3, F: 4 };

  function generateTimeSlots() {
    const slots = [];
    for (let hour = 8; hour <= 20; hour++) {
      slots.push(`${hour.toString().padStart(2, '0')}:00`);
    }
    return slots;
  }

  function parseTime(timeStr) {
    if (!timeStr) return null;
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours + minutes / 60;
  }

  function getCoursePosition(course) {
    const startTime = parseTime(course['Start Time']);
    const endTime = parseTime(course['End Time']);

    if (!startTime || !endTime) return null;

    const startRow = Math.floor((startTime - 8) * 2) + 2; // +2 for header rows
    const duration = endTime - startTime;
    const rowSpan = Math.ceil(duration * 2);

    return { startRow, rowSpan };
  }

  function getCoursesByDay() {
    const coursesByDay = Array(5).fill(null).map(() => []);

    currentSchedule.schedule.forEach(course => {
      const daysStr = course['Days of Week'] || '';
      const position = getCoursePosition(course);

      if (!position) return;

      for (const dayChar of daysStr) {
        const dayIndex = dayMap[dayChar];
        if (dayIndex !== undefined) {
          coursesByDay[dayIndex].push({
            ...course,
            ...position,
          });
        }
      }
    });

    return coursesByDay;
  }

  const coursesByDay = getCoursesByDay();

  return (
    <div className="schedule-display">
      <div className="schedule-header">
        <h3>Generated Schedules</h3>
        <div className="schedule-navigation">
          <button
            onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))}
            disabled={currentIndex === 0}
          >
            Previous
          </button>
          <span className="schedule-counter">
            Schedule {currentIndex + 1} of {schedules.length}
          </span>
          <button
            onClick={() => setCurrentIndex(Math.min(schedules.length - 1, currentIndex + 1))}
            disabled={currentIndex === schedules.length - 1}
          >
            Next
          </button>
        </div>
        <div className="schedule-score">
          Score: {currentSchedule.score.toFixed(2)}
        </div>
      </div>

      <div className="schedule-grid-container">
        <div className="schedule-grid">
          <div className="time-column">
            <div className="grid-header">Time</div>
            {timeSlots.map(slot => (
              <div key={slot} className="time-slot">
                {slot}
              </div>
            ))}
          </div>

          {days.map((day, dayIndex) => (
            <div key={day} className="day-column">
              <div className="grid-header">{day}</div>
              <div className="day-content">
                {coursesByDay[dayIndex].map((course, idx) => (
                  <div
                    key={idx}
                    className="course-block"
                    style={{
                      gridRow: `${course.startRow} / span ${course.rowSpan}`,
                    }}
                  >
                    <div className="course-code">
                      {course.Code} {course.Number}
                    </div>
                    <div className="course-name">{course.Name}</div>
                    <div className="course-time">
                      {course['Start Time']} - {course['End Time']}
                    </div>
                    <div className="course-instructor">
                      {course['Primary Instructor (Concat)']}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="schedule-details">
        <h4>Course Details</h4>
        <div className="course-list">
          {currentSchedule.schedule.map((course, idx) => (
            <div key={idx} className="course-detail-item">
              <div className="course-detail-header">
                <strong>{course.Code} {course.Number}</strong> - {course.Name}
              </div>
              <div className="course-detail-info">
                <span>CRN: {course.CRN}</span>
                <span>Instructor: {course['Primary Instructor (Concat)']}</span>
                <span>Time: {course['Days of Week']} {course['Start Time']}-{course['End Time']}</span>
                {course.RMP && <span>RMP: {course.RMP}/5.0</span>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ScheduleDisplay;
