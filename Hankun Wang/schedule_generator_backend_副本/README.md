# Schedule Generator Backend

A Flask-based REST API for generating course schedules based on user preferences, GPA targets, and statistical data.

## 📁 Project Structure

```
schedule_generator_backend/
├── app.py                      # Main application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── test_api.py                # API test script
├── README.md                   # This file
│
├── api/                        # API endpoints
│   ├── __init__.py
│   └── routes.py              # Route definitions
│
├── services/                   # Business logic
│   ├── __init__.py
│   ├── data_service.py        # Data loading and filtering
│   ├── recommender.py         # Recommendation engine
│   └── scheduler.py           # Schedule generation
│
├── models/                     # Data models (optional)
│   └── __init__.py
│
├── utils/                      # Utility functions
│   └── __init__.py
│
├── your_modules/              # Your existing modules
│   ├── __init__.py
│   ├── data_cleaning.py       # Replace with your module
│   ├── hard_filter.py         # Replace with your module
│   └── soft_filter.py         # Replace with your module
│
└── data/                       # Data directory
    └── cleaned_courses.pkl     # Your cleaned data file
```

## 🚀 Quick Start

### Step 1: Install Python

Make sure you have Python 3.8+ installed:

```bash
python --version
# or
python3 --version
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd schedule_generator_backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Add Your Modules

Replace the placeholder files in `your_modules/` with your actual implementations:

1. **data_cleaning.py** - Your data cleaning module
2. **hard_filter.py** - Your hard filtering module  
3. **soft_filter.py** - Your soft filtering module

Or keep the placeholders to use the default implementations.

### Step 5: Add Your Data

Place your cleaned course data in the `data/` directory:

```bash
# Create data directory if it doesn't exist
mkdir -p data

# Copy your cleaned data file
# Expected format: pickle file with list of course dictionaries
cp /path/to/your/cleaned_courses.pkl data/
```

**Course Data Format:**

Each course should be a dictionary with these fields:
```python
{
    'id': 'CS225',
    'name': 'Data Structures',
    'credits': 4,
    'avg_gpa': 3.2,
    'avg_workload_hours': 12,
    'avg_rating': 4.5,
    'professor': 'Smith',
    'meeting_times': [
        {'days': 'MWF', 'start': '09:00', 'end': '10:00'}
    ]
}
```

### Step 6: Start the Server

```bash
python app.py
```

You should see:

```
==================================================
🚀 Schedule Generator Backend Starting...
==================================================
📍 Server URL: http://localhost:5000
📍 Health Check: http://localhost:5000/health
📍 API Base URL: http://localhost:5000/api/v1
==================================================

Available Endpoints:
  POST /api/v1/generate-schedule  - Generate course schedules
  POST /api/v1/recommend          - Get course recommendations
  GET  /api/v1/courses/search     - Search courses
  GET  /api/v1/courses/<id>       - Get course details

==================================================
Press CTRL+C to stop the server
==================================================

 * Running on http://127.0.0.1:5000
```

### Step 7: Test the API

Open a new terminal (keep the server running) and run:

```bash
python test_api.py
```

Or test with curl:

```bash
# Test health check
curl http://localhost:5000/health

# Test API
curl http://localhost:5000/api/v1/test
```

## 📡 API Endpoints

### 1. Generate Schedule

**Endpoint:** `POST /api/v1/generate-schedule`

**Request Body:**
```json
{
  "user_profile": {
    "target_gpa": 3.5,
    "max_workload_hours": 15,
    "current_gpa": 3.3,
    "preferred_professors": ["Smith"],
    "avoid_professors": []
  },
  "hard_constraints": {
    "completed_courses": ["CS101", "MATH220"],
    "required_courses": ["CS225"],
    "time_blocks": [],
    "excluded_courses": []
  },
  "soft_preferences": {
    "preferred_times": ["morning"],
    "preferred_days": ["MWF"],
    "rating_threshold": 4.0
  },
  "num_schedules": 5
}
```

**Example using curl:**
```bash
curl -X POST http://localhost:5000/api/v1/generate-schedule \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "target_gpa": 3.5,
      "max_workload_hours": 15,
      "current_gpa": 3.3,
      "preferred_professors": [],
      "avoid_professors": []
    },
    "hard_constraints": {},
    "soft_preferences": {},
    "num_schedules": 3
  }'
```

### 2. Get Recommendations

**Endpoint:** `POST /api/v1/recommend`

Returns recommended courses without generating full schedules.

### 3. Search Courses

**Endpoint:** `GET /api/v1/courses/search?q=<query>`

**Example:**
```bash
curl http://localhost:5000/api/v1/courses/search?q=CS225
```

### 4. Get Course Details

**Endpoint:** `GET /api/v1/courses/<course_id>`

**Example:**
```bash
curl http://localhost:5000/api/v1/courses/CS225
```

## 🔧 Configuration

Edit `config.py` to customize settings:

```python
# Recommendation weights
GPA_WEIGHT = 0.35
WORKLOAD_WEIGHT = 0.25
RATING_WEIGHT = 0.25
PROFESSOR_WEIGHT = 0.15

# Schedule constraints
MAX_COURSES_PER_SEMESTER = 6
MIN_COURSES_PER_SEMESTER = 3
MAX_CREDITS = 18

# Server settings
PORT = 5000
DEBUG = True
```

## 🐛 Troubleshooting

### Port Already in Use

If port 5000 is already in use:

1. Change the port in `config.py`:
   ```python
   PORT = 8000
   ```

2. Or find and kill the process using port 5000:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Mac/Linux
   lsof -i :5000
   kill -9 <PID>
   ```

### Module Not Found Errors

Make sure you're in the project directory and virtual environment is activated:

```bash
cd schedule_generator_backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Data File Not Found

The server will use sample data if your data file is missing. To use your own data:

```bash
# Make sure data directory exists
mkdir -p data

# Copy your data file
cp /path/to/cleaned_courses.pkl data/
```

### Connection Refused

Make sure the server is running:

```bash
# In one terminal
python app.py

# In another terminal
curl http://localhost:5000/health
```

## 🧪 Testing

### Run All Tests
```bash
python test_api.py
```

### Manual Testing with curl

```bash
# Health check
curl http://localhost:5000/health

# Generate schedule
curl -X POST http://localhost:5000/api/v1/generate-schedule \
  -H "Content-Type: application/json" \
  -d @test_payload.json
```

### Using Python requests

```python
import requests

response = requests.post(
    'http://localhost:5000/api/v1/generate-schedule',
    json={
        "user_profile": {
            "target_gpa": 3.5,
            "max_workload_hours": 15,
            "current_gpa": 3.3,
            "preferred_professors": [],
            "avoid_professors": []
        },
        "num_schedules": 3
    }
)

print(response.json())
```

## 📦 Production Deployment

For production, use Gunicorn:

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 🔑 Key Features

- ✅ Integrates with your existing data cleaning and filtering modules
- ✅ GPA-based course recommendations
- ✅ Workload balancing
- ✅ Professor preferences
- ✅ Time conflict detection
- ✅ Multiple schedule generation
- ✅ RESTful API design
- ✅ CORS enabled for frontend integration

## 📝 Next Steps

1. Replace placeholder modules with your actual implementations
2. Add your cleaned course data
3. Test the API endpoints
4. Integrate with your frontend
5. Add authentication if needed
6. Deploy to production server

## 💡 Tips

- Use the sample data to test before adding your own data
- Check server logs for debugging information
- Use `test_api.py` to verify all endpoints work
- Adjust recommendation weights in `config.py` for better results

## 📧 Support

If you encounter issues:
1. Check the server logs in the terminal
2. Verify your data format matches the expected structure
3. Ensure all dependencies are installed
4. Test with the sample data first

---

**Happy Scheduling! 🎓**
