import os

class Config:
    """Application configuration"""
    
    # Base directories
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'cleaned_courses.pkl')
    
    # Recommendation algorithm weights
    GPA_WEIGHT = 0.35
    WORKLOAD_WEIGHT = 0.25
    RATING_WEIGHT = 0.25
    PROFESSOR_WEIGHT = 0.15
    
    # Schedule constraints
    MAX_COURSES_PER_SEMESTER = 6
    MIN_COURSES_PER_SEMESTER = 3
    MAX_CREDITS = 18
    
    # API settings
    PAGINATION_SIZE = 20
    MAX_SCHEDULE_VARIATIONS = 10
    
    # Flask settings
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
