from typing import List, Dict, Any
import numpy as np

class CourseRecommender:
    """
    Course recommendation engine based on GPA and statistical data
    """
    
    def __init__(self, config):
        self.gpa_weight = config.GPA_WEIGHT
        self.workload_weight = config.WORKLOAD_WEIGHT
        self.rating_weight = config.RATING_WEIGHT
        self.professor_weight = config.PROFESSOR_WEIGHT
    
    def compute_gpa_score(self, course: Dict, user_target: float) -> float:
        """
        Score based on how course GPA aligns with user's target
        
        Args:
            course: Course dictionary with avg_gpa
            user_target: User's target GPA
            
        Returns:
            Score between 0 and 1
        """
        course_avg_gpa = course.get('avg_gpa', 3.0)
        
        # Prefer courses where avg GPA is close to target
        difference = abs(course_avg_gpa - user_target)
        score = max(0, 1 - (difference / 2.0))
        
        return score
    
    def compute_workload_score(self, course: Dict, user_max: float) -> float:
        """
        Score based on workload feasibility
        
        Args:
            course: Course dictionary with avg_workload_hours
            user_max: User's maximum workload hours
            
        Returns:
            Score between 0 and 1
        """
        course_workload = course.get('avg_workload_hours', 10)
        
        if course_workload > user_max:
            return 0.0
        
        # Prefer courses with reasonable workload
        score = 1 - (course_workload / (user_max * 1.5))
        return max(0, min(1, score))
    
    def compute_rating_score(self, course: Dict) -> float:
        """
        Normalize course rating to 0-1 scale
        
        Args:
            course: Course dictionary with avg_rating
            
        Returns:
            Normalized score between 0 and 1
        """
        rating = course.get('avg_rating', 3.0)
        return rating / 5.0
    
    def compute_professor_score(self, course: Dict, preferences: Dict) -> float:
        """
        Score based on professor preferences
        
        Args:
            course: Course dictionary with professor name
            preferences: User preferences with preferred/avoided professors
            
        Returns:
            Score between 0 and 1
        """
        professor = course.get('professor', '')
        
        preferred = preferences.get('preferred_professors', [])
        avoided = preferences.get('avoid_professors', [])
        
        if professor in avoided:
            return 0.0
        elif professor in preferred:
            return 1.0
        else:
            return 0.5
    
    def calculate_overall_score(self, 
                                course: Dict, 
                                user_profile: Dict) -> float:
        """
        Calculate weighted recommendation score
        
        Args:
            course: Course dictionary
            user_profile: User profile with preferences
            
        Returns:
            Overall score between 0 and 1
        """
        gpa_score = self.compute_gpa_score(course, user_profile['target_gpa'])
        workload_score = self.compute_workload_score(
            course, 
            user_profile['max_workload_hours']
        )
        rating_score = self.compute_rating_score(course)
        professor_score = self.compute_professor_score(course, user_profile)
        
        total_score = (
            self.gpa_weight * gpa_score +
            self.workload_weight * workload_score +
            self.rating_weight * rating_score +
            self.professor_weight * professor_score
        )
        
        return total_score
    
    def recommend(self, 
                  courses: List[Dict], 
                  user_profile: Dict,
                  top_n: int = 20) -> List[Dict]:
        """
        Generate top N course recommendations
        
        Args:
            courses: List of course dictionaries
            user_profile: User profile and preferences
            top_n: Number of top recommendations to return
            
        Returns:
            Sorted list of recommended courses with scores
        """
        scored_courses = []
        
        for course in courses:
            score = self.calculate_overall_score(course, user_profile)
            scored_courses.append({
                **course,
                'recommendation_score': round(score, 3),
                'score_breakdown': {
                    'gpa': round(self.compute_gpa_score(course, user_profile['target_gpa']), 3),
                    'workload': round(self.compute_workload_score(course, user_profile['max_workload_hours']), 3),
                    'rating': round(self.compute_rating_score(course), 3),
                    'professor': round(self.compute_professor_score(course, user_profile), 3)
                }
            })
        
        # Sort by score (descending)
        scored_courses.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return scored_courses[:top_n]
