# Course Scheduler

A full-stack web application for generating optimal class schedules for UIUC students. Built with React (frontend) and Flask (backend).

## Features

- **Course Search & Selection**: Filter courses by subject, number, instructor, and days
- **Multiple Section Selection**: Choose multiple sections per course to see all possible combinations
- **Break Scheduling**: Set hard breaks (must be free) and soft breaks (prefer to be free)
- **Preference Weights**: Customize schedule generation based on:
  - RateMyProfessor scores
  - Average GPA
  - Time preferences (early, late, or compact)
  - Break conflicts
- **Visual Schedule Display**: Interactive calendar view of generated schedules
- **Smart Ranking**: Generates up to 200 schedules ranked by your preferences

## Project Structure

```
website/
├── backend/                    # Flask API
│   ├── api/                   # API endpoints
│   │   ├── courses.py        # Course filtering endpoints
│   │   └── schedules.py      # Schedule generation endpoints
│   ├── services/              # Business logic
│   │   ├── data_loader.py    # Course data loading
│   │   └── schedule_generator.py  # Schedule algorithm
│   ├── app.py                # Flask app entry point
│   └── requirements.txt      # Python dependencies
│
└── course-generator/          # React frontend
    ├── src/
    │   ├── components/       # React components
    │   │   ├── CourseFilter/
    │   │   ├── ScheduleDisplay/
    │   │   ├── PreferenceSlider/
    │   │   └── BreakScheduler/
    │   ├── pages/            # Page components
    │   │   ├── CourseSelectionPage.jsx
    │   │   ├── PreferencePage.jsx
    │   │   └── ResultsPage.jsx
    │   ├── services/         # API client
    │   │   └── api.js
    │   ├── App.jsx           # Main app component
    │   └── main.jsx          # Entry point
    └── package.json
```

## Setup Instructions

### Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- Course data CSV file at `../../datasets/2025-sp-modified.csv`

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (optional):
   ```bash
   cp .env.example .env
   # Edit .env to customize DATA_PATH if needed
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd course-generator
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file (optional):
   ```bash
   cp .env.example .env
   # Edit if backend is running on a different port
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## Usage

1. **Select Courses**:
   - Use filters to search for courses
   - Click on sections to select them
   - You can select multiple sections per course
   - Click "Continue to Preferences" when done

2. **Set Preferences**:
   - Adjust sliders to prioritize what matters to you
   - Add hard breaks (must be free) or soft breaks (prefer to be free)
   - Select time preference (early, late, or compact)
   - Click "Generate Schedules"

3. **View Results**:
   - Browse through generated schedules
   - View visual calendar representation
   - See course details including RMP scores
   - Navigate between schedules using Previous/Next buttons

## API Endpoints

### Courses

- `GET /api/courses` - Get courses with optional filters
  - Query params: `subject`, `number`, `crn`, `instructor`, `days`
- `GET /api/courses/:crn` - Get specific course by CRN
- `GET /api/courses/subjects` - Get list of all subjects
- `GET /api/courses/subjects/:subject` - Get courses for a subject

### Schedules

- `POST /api/schedules/generate` - Generate schedules
  - Body: `{ courses, hard_breaks, soft_breaks, preferences, limit }`
- `POST /api/schedules/validate` - Validate a schedule for conflicts
  - Body: `{ crns, hard_breaks }`

### Health

- `GET /api/health` - Health check endpoint

## Data Format

The application expects course data in CSV format with the following columns:

- `CRN`: Course Reference Number
- `Code`: Subject code (e.g., "CS")
- `Number`: Course number
- `Name`: Course name
- `Sched Type`: Schedule type (LEC, DIS, LAB, etc.)
- `Days of Week`: Days (e.g., "MWF")
- `Start Time`: HH:MM format
- `End Time`: HH:MM format
- `Primary Instructor (Concat)`: Instructor name
- `RMP`: RateMyProfessor score (optional)
- `Mean Grade By Professor (A+..F,W,Students)`: Grade distribution (optional)

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `backend/api/` and business logic in `backend/services/`
2. **Frontend**: Create components in `src/components/` and pages in `src/pages/`
3. **API Client**: Update `src/services/api.js` with new endpoints

### Building for Production

**Frontend:**
```bash
cd course-generator
npm run build
```

**Backend:**
```bash
# Set FLASK_ENV=production in .env
# Use a production WSGI server like gunicorn
pip install gunicorn
gunicorn app:app
```

## Troubleshooting

### Backend issues:

- **"No module named 'flask'"**: Install dependencies with `pip install -r requirements.txt`
- **"File not found" for CSV**: Check `DATA_PATH` in `.env` or hardcoded path in `data_loader.py`
- **CORS errors**: Ensure `flask-cors` is installed and CORS is enabled in `app.py`

### Frontend issues:

- **"Cannot connect to backend"**: Ensure Flask is running on port 5000
- **Blank page**: Check browser console for errors, ensure `.env` has correct API URL
- **Build errors**: Delete `node_modules` and run `npm install` again

## Task Checklist

Based on your original requirements:

### Completed:
- [x] Create filter and output all courses fulfilling criteria (CourseFilter component)
- [x] Display courses on website (CourseSelectionPage)
- [x] Buttons for every section (Course section selection UI)
- [x] Send specific code, class and CRN (API integration)
- [x] Break scheduling architecture (BreakScheduler component with hard/soft breaks)
- [x] Display preference sliders (PreferenceSlider component)
- [x] Return preferences in correct order format (API handles this)
- [x] Schedule sorter, returns top 200 sorted (schedule_generator.py)
- [x] Display schedules (ScheduleDisplay component with calendar UI)
- [x] Display select course info (Course details in schedule view)
- [x] Extract necessary information from each schedule (Formatted in ResultsPage)

### To Implement (Your tasks):
- [ ] Connect your Python course generation algorithm to the backend
- [ ] Test with real course data
- [ ] Customize the GPA calculation in `schedule_generator.py` based on your grade distribution format
- [ ] Add any additional filtering logic specific to your algorithm
- [ ] Consider integrating your RMP fetching code if needed

## Contributing

This project is part of the CS196 FA25 Group 5 course project at UIUC.

## License

MIT License - feel free to use and modify for your needs.
