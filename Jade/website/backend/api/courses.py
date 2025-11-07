from flask import Blueprint, jsonify, request
from services.data_loader import data_loader

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
def get_courses():
    """
    Get courses with optional filters
    Query params: subject, number, crn, instructor, days
    """
    try:
        filters = {
            'subject': request.args.get('subject'),
            'number': request.args.get('number'),
            'crn': request.args.get('crn'),
            'instructor': request.args.get('instructor'),
            'days': request.args.get('days')
        }

        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}

        courses = data_loader.get_courses(filters)
        return jsonify({
            'success': True,
            'count': len(courses),
            'courses': courses
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@courses_bp.route('/<int:crn>', methods=['GET'])
def get_course(crn):
    """Get specific course by CRN"""
    try:
        course = data_loader.get_course_by_crn(crn)

        if course:
            return jsonify({
                'success': True,
                'course': course
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Course not found'
            }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@courses_bp.route('/subjects', methods=['GET'])
def get_subjects():
    """Get list of all unique subjects"""
    try:
        subjects = data_loader.get_unique_subjects()
        return jsonify({
            'success': True,
            'subjects': subjects
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@courses_bp.route('/subjects/<subject>', methods=['GET'])
def get_courses_by_subject(subject):
    """Get all courses for a specific subject"""
    try:
        courses = data_loader.get_courses_by_subject(subject)
        return jsonify({
            'success': True,
            'count': len(courses),
            'courses': courses
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
