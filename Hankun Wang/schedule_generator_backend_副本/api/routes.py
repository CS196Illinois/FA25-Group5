from flask import Blueprint, request, jsonify
from services.data_service import DataService
from services.recommender import CourseRecommender
from services.scheduler import ScheduleGenerator
from config import Config

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Initialize services
data_service = DataService(Config.CLEANED_DATA_PATH)
recommender = CourseRecommender(Config)
scheduler = ScheduleGenerator(
    Config.MIN_COURSES_PER_SEMESTER,
    Config.MAX_COURSES_PER_SEMESTER,
    Config.MAX_CREDITS
)


@api_bp.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    """
    Main endpoint to generate recommended schedules
    
    Request Body Example:
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
    """
    try:
        data = request.json
        
        # Validate required fields
        if 'user_profile' not in data:
            return jsonify({'error': 'Missing user_profile'}), 400
        
        # Load course data
        print("\n" + "="*50)
        print("Processing schedule generation request...")
        all_courses = data_service.load_data()
        
        # Apply hard filters
        print("Applying hard constraints...")
        filtered_courses = data_service.apply_hard_filters(
            all_courses,
            data.get('hard_constraints', {})
        )
        
        if not filtered_courses:
            return jsonify({
                'error': 'No courses match your hard constraints',
                'schedules': []
            }), 200
        
        print(f"  {len(filtered_courses)} courses after hard filtering")
        
        # Apply soft filters
        print("Applying soft preferences...")
        ranked_courses = data_service.apply_soft_filters(
            filtered_courses,
            data.get('soft_preferences', {})
        )
        
        print(f"  {len(ranked_courses)} courses after soft filtering")
        
        # Get recommendations
        print("Generating recommendations...")
        recommended_courses = recommender.recommend(
            ranked_courses,
            data['user_profile'],
            top_n=25
        )
        
        print(f"  Top {len(recommended_courses)} courses recommended")
        
        # Generate schedules
        print("Creating schedules...")
        schedules = scheduler.generate_schedules(
            recommended_courses,
            data['user_profile'],
            num_schedules=data.get('num_schedules', 5)
        )
        
        print(f"  Generated {len(schedules)} valid schedules")
        print("="*50 + "\n")
        
        return jsonify({
            'success': True,
            'schedules': schedules,
            'num_schedules': len(schedules),
            'top_recommended_courses': recommended_courses[:10]
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@api_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    """
    Get course recommendations without schedule generation
    
    Request Body Example:
    {
        "user_profile": {
            "target_gpa": 3.5,
            "max_workload_hours": 15,
            "current_gpa": 3.3,
            "preferred_professors": [],
            "avoid_professors": []
        },
        "hard_constraints": {...},
        "soft_preferences": {...},
        "top_n": 20
    }
    """
    try:
        data = request.json
        
        if 'user_profile' not in data:
            return jsonify({'error': 'Missing user_profile'}), 400
        
        # Load and filter data
        all_courses = data_service.load_data()
        
        filtered = data_service.apply_hard_filters(
            all_courses,
            data.get('hard_constraints', {})
        )
        
        ranked = data_service.apply_soft_filters(
            filtered,
            data.get('soft_preferences', {})
        )
        
        # Get recommendations
        recommendations = recommender.recommend(
            ranked,
            data['user_profile'],
            top_n=data.get('top_n', 20)
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/courses/search', methods=['GET'])
def search_courses():
    """
    Search for courses by query string
    
    Query Parameters:
        q: Search query (searches in course ID and name)
        
    Example: /api/v1/courses/search?q=CS225
    """
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'error': 'Missing query parameter "q"'}), 400
    
    try:
        all_courses = data_service.load_data()
        
        # Search in course name and ID
        results = [
            c for c in all_courses
            if query in c.get('name', '').lower() or
               query in c.get('id', '').lower()
        ]
        
        return jsonify({
            'success': True,
            'results': results[:20],
            'total': len(results),
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/courses/<course_id>', methods=['GET'])
def get_course_details(course_id):
    """
    Get detailed statistics for a specific course
    
    Example: /api/v1/courses/CS225
    """
    try:
        course = data_service.get_course_statistics(course_id)
        
        if not course:
            return jsonify({
                'error': f'Course {course_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'course': course
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        'status': 'success',
        'message': 'API is working correctly!',
        'available_endpoints': [
            'POST /api/v1/generate-schedule',
            'POST /api/v1/recommend',
            'GET /api/v1/courses/search?q=<query>',
            'GET /api/v1/courses/<course_id>'
        ]
    }), 200
