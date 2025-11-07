from flask import Blueprint, jsonify, request
from services.data_loader import data_loader
from services.schedule_generator import ScheduleGenerator

schedules_bp = Blueprint('schedules', __name__)

@schedules_bp.route('/generate', methods=['POST'])
def generate_schedules():
    """
    Generate schedules from selected courses

    Request body:
    {
        "courses": [[crn1, crn2], [crn3, crn4]],  // List of CRN lists (sections for each course)
        "hard_breaks": [{"days": "MWF", "start": "12:00", "end": "13:00"}],
        "soft_breaks": [{"days": "TR", "start": "14:00", "end": "15:00"}],
        "preferences": {
            "rmp_weight": 1.0,
            "gpa_weight": 1.0,
            "time_preference": "early",  // "early", "late", or "compact"
            "break_weight": 0.5
        },
        "limit": 200
    }
    """
    try:
        data = request.get_json()

        if not data or 'courses' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: courses'
            }), 400

        selected_crns = data['courses']
        hard_breaks = data.get('hard_breaks', [])
        soft_breaks = data.get('soft_breaks', [])
        preferences = data.get('preferences', {})
        limit = data.get('limit', 200)

        # Load course data
        df = data_loader.load_data()
        generator = ScheduleGenerator(df)

        # Generate valid schedules
        schedules = generator.generate_schedules(
            selected_crns,
            hard_breaks,
            soft_breaks
        )

        # Sort by preferences
        sorted_schedules = generator.sort_schedules(
            schedules,
            preferences,
            soft_breaks,
            limit
        )

        return jsonify({
            'success': True,
            'count': len(sorted_schedules),
            'schedules': sorted_schedules
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@schedules_bp.route('/validate', methods=['POST'])
def validate_schedule():
    """
    Check if a specific schedule has time conflicts

    Request body:
    {
        "crns": [12345, 67890, 11111],
        "hard_breaks": [...]
    }
    """
    try:
        data = request.get_json()

        if not data or 'crns' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: crns'
            }), 400

        crns = data['crns']
        hard_breaks = data.get('hard_breaks', [])

        # Load courses
        df = data_loader.load_data()
        generator = ScheduleGenerator(df)

        courses = []
        for crn in crns:
            course = df[df['CRN'] == int(crn)]
            if len(course) > 0:
                courses.append(course.iloc[0].to_dict())

        # Check for conflicts
        has_conflict = False
        conflicts = []

        # Check time conflicts between courses
        for i, course1 in enumerate(courses):
            for j, course2 in enumerate(courses[i+1:], i+1):
                if generator.check_time_conflict(course1, course2):
                    has_conflict = True
                    conflicts.append({
                        'type': 'time_conflict',
                        'course1': course1['CRN'],
                        'course2': course2['CRN']
                    })

        # Check hard break conflicts
        has_hard_conflict, _ = generator.check_break_conflict(courses, hard_breaks, [])
        if has_hard_conflict:
            has_conflict = True
            conflicts.append({
                'type': 'hard_break_conflict'
            })

        return jsonify({
            'success': True,
            'valid': not has_conflict,
            'conflicts': conflicts
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
