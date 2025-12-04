from typing import List, Dict, Any, Optional
import pickle
import os

class DataService:
    """
    Service to manage course data and call existing filtering modules
    """
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.courses = None
        
    def load_data(self) -> List[Dict]:
        """
        Load cleaned course data
        
        Returns:
            List of course dictionaries
        """
        # Check if cleaned data exists
        if os.path.exists(self.data_path):
            print(f"Loading cleaned data from {self.data_path}")
            with open(self.data_path, 'rb') as f:
                self.courses = pickle.load(f)
        else:
            print(f"⚠ Warning: Data file not found at {self.data_path}")
            print("  Using sample data for demonstration")
            # Create sample data for testing
            self.courses = self._create_sample_data()
            
        print(f"✓ Loaded {len(self.courses)} courses")
        return self.courses
    
    def _create_sample_data(self) -> List[Dict]:
        """Create sample course data for testing"""
        return [
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
            },
            {
                'id': 'CS374',
                'name': 'Algorithms',
                'credits': 4,
                'avg_gpa': 2.9,
                'avg_workload_hours': 15,
                'avg_rating': 4.2,
                'professor': 'Johnson',
                'meeting_times': [
                    {'days': 'TR', 'start': '11:00', 'end': '12:30'}
                ]
            },
            {
                'id': 'MATH241',
                'name': 'Calculus III',
                'credits': 3,
                'avg_gpa': 3.0,
                'avg_workload_hours': 10,
                'avg_rating': 3.8,
                'professor': 'Williams',
                'meeting_times': [
                    {'days': 'MWF', 'start': '13:00', 'end': '14:00'}
                ]
            }
        ]
    
    def apply_hard_filters(self, 
                          courses: List[Dict], 
                          constraints: Dict[str, Any]) -> List[Dict]:
        """
        Apply hard constraints (must-satisfy filters)
        
        Args:
            courses: List of course dictionaries
            constraints: Dictionary with keys like:
                - completed_courses: List of course IDs
                - required_courses: List of course IDs
                - time_blocks: List of blocked time slots
                - excluded_courses: List of course IDs to exclude
        
        Returns:
            Filtered list of courses
        """
        try:
            # Try to import your existing hard filter module
            from your_modules.hard_filter import apply_hard_filter
            print("✓ Using custom hard_filter module")
            return apply_hard_filter(courses, constraints)
        except ImportError:
            print("⚠ Using default hard filter implementation")
            # Default implementation
            filtered = courses.copy()
            
            # Exclude completed courses
            completed = constraints.get('completed_courses', [])
            if completed:
                filtered = [c for c in filtered if c['id'] not in completed]
            
            # Exclude specified courses
            excluded = constraints.get('excluded_courses', [])
            if excluded:
                filtered = [c for c in filtered if c['id'] not in excluded]
            
            return filtered
    
    def apply_soft_filters(self, 
                          courses: List[Dict], 
                          preferences: Dict[str, Any]) -> List[Dict]:
        """
        Apply soft preferences (ranking filters)
        
        Args:
            courses: List of course dictionaries
            preferences: Dictionary with keys like:
                - preferred_times: List of time preferences
                - preferred_days: List of day preferences
                - rating_threshold: Minimum rating
        
        Returns:
            Ranked list of courses
        """
        try:
            # Try to import your existing soft filter module
            from your_modules.soft_filter import apply_soft_filter
            print("✓ Using custom soft_filter module")
            return apply_soft_filter(courses, preferences)
        except ImportError:
            print("⚠ Using default soft filter implementation")
            # Default implementation - simple rating filter
            rating_threshold = preferences.get('rating_threshold', 0.0)
            filtered = [c for c in courses if c.get('avg_rating', 0) >= rating_threshold]
            
            # Sort by rating
            filtered.sort(key=lambda x: x.get('avg_rating', 0), reverse=True)
            return filtered
    
    def get_course_statistics(self, course_id: str) -> Optional[Dict]:
        """
        Get detailed statistics for a specific course
        
        Args:
            course_id: Course identifier
            
        Returns:
            Course dictionary or None if not found
        """
        if not self.courses:
            self.load_data()
        
        course = next((c for c in self.courses if c['id'] == course_id), None)
        return course
