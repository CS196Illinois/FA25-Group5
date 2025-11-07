const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

class API {
  // Course endpoints
  async getCourses(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/courses?${params}`);
    return response.json();
  }

  async getCourseByCRN(crn) {
    const response = await fetch(`${API_BASE_URL}/courses/${crn}`);
    return response.json();
  }

  async getSubjects() {
    const response = await fetch(`${API_BASE_URL}/courses/subjects`);
    return response.json();
  }

  async getCoursesBySubject(subject) {
    const response = await fetch(`${API_BASE_URL}/courses/subjects/${subject}`);
    return response.json();
  }

  // Schedule endpoints
  async generateSchedules(data) {
    const response = await fetch(`${API_BASE_URL}/schedules/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  async validateSchedule(crns, hardBreaks = []) {
    const response = await fetch(`${API_BASE_URL}/schedules/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ crns, hard_breaks: hardBreaks }),
    });
    return response.json();
  }

  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.json();
  }
}

export default new API();
