from typing import List, Dict, Optional
from itertools import combinations
import numpy as np

class ScheduleGenerator:
    """
    Generate conflict-free course schedules
    """
    
    def __init__(self, min_courses: int = 3, max_courses: int = 6, max_credits: int = 18):
        self.min_courses = min_courses
        self.max_courses = max_courses
        self.max_credits = max_credits
    
    def parse_time(self, time_str: str) -> int:
        """Convert time string (HH:MM) to minutes since midnight"""
        try:
            h, m = map(int, time_str.split(':'))
            return h * 60 + m
        except:
            return 0
    
    def times_overlap(self, time1: Dict, time2: Dict) -> bool:
        """
        Check if two time slots overlap
        
        Args:
            time1, time2: Dictionaries with 'days', 'start', 'end'
            
        Returns:
            True if times overlap, False otherwise
        """
        # Check if days overlap
        days1 = set(time1.get('days', ''))
        days2 = set(time2.get('days', ''))
        
        if not days1 & days2:
            return False
        
        # Check if times overlap
        start1 = self.parse_time(time1['start'])
        end1 = self.parse_time(time1['end'])
        start2 = self.parse_time(time2['start'])
        end2 = self.parse_time(time2['end'])
        
        return not (end1 <= start2 or end2 <= start1)
    
    def has_conflict(self, course1: Dict, course2: Dict) -> bool:
        """
        Check if two courses have time conflicts
        
        Args:
            course1, course2: Course dictionaries with meeting_times
            
        Returns:
            True if courses conflict, False otherwise
        """
        times1 = course1.get('meeting_times', [])
        times2 = course2.get('meeting_times', [])
        
        for t1 in times1:
            for t2 in times2:
                if self.times_overlap(t1, t2):
                    return True
        
        return False
    
    def is_valid_schedule(self, courses: List[Dict]) -> bool:
        """
        Check if a schedule has no conflicts and meets constraints
        
        Args:
            courses: List of course dictionaries
            
        Returns:
            True if schedule is valid, False otherwise
        """
        # Check credit limit
        total_credits = sum(c.get('credits', 3) for c in courses)
        if total_credits > self.max_credits:
            return False
        
        # Check time conflicts
        for i in range(len(courses)):
            for j in range(i + 1, len(courses)):
                if self.has_conflict(courses[i], courses[j]):
                    return False
        
        return True
    
    def calculate_schedule_score(self, 
                                 courses: List[Dict], 
                                 user_profile: Dict) -> float:
        """
        Calculate overall quality score for a schedule
        
        Args:
            courses: List of courses in the schedule
            user_profile: User preferences and targets
            
        Returns:
            Overall schedule quality score (0-1)
        """
        if not courses:
            return 0.0
        
        # Average recommendation score
        avg_rec_score = np.mean([c.get('recommendation_score', 0) for c in courses])
        
        # GPA expectation
        avg_gpa = np.mean([c.get('avg_gpa', 3.0) for c in courses])
        gpa_match = 1 - abs(avg_gpa - user_profile.get('target_gpa', 3.0)) / 2.0
        gpa_match = max(0, min(1, gpa_match))
        
        # Workload balance
        total_workload = sum(c.get('avg_workload_hours', 10) for c in courses)
        target_workload = user_profile.get('max_workload_hours', 15) * len(courses)
        workload_diff = abs(total_workload - target_workload)
        workload_score = max(0, 1 - workload_diff / 50)
        
        # Combined score
        return 0.5 * avg_rec_score + 0.3 * gpa_match + 0.2 * workload_score
    
    def generate_schedules(self, 
                          courses: List[Dict], 
                          user_profile: Dict,
                          num_schedules: int = 5) -> List[Dict]:
        """
        Generate multiple valid schedule options
        
        Args:
            courses: List of recommended courses
            user_profile: User preferences
            num_schedules: Number of schedules to generate
            
        Returns:
            List of schedule dictionaries, each containing:
            - courses: List of course objects
            - total_credits: Total credits
            - expected_gpa: Expected average GPA
            - total_workload: Total workload hours
            - schedule_score: Overall quality score
        """
        valid_schedules = []
        
        # Try different numbers of courses
        for n in range(self.max_courses, self.min_courses - 1, -1):
            # Limit search space to top courses
            search_pool = courses[:min(25, len(courses))]
            
            # Generate combinations
            for combo in combinations(search_pool, n):
                if self.is_valid_schedule(list(combo)):
                    schedule = {
                        'courses': list(combo),
                        'total_credits': sum(c.get('credits', 3) for c in combo),
                        'expected_gpa': round(np.mean([c.get('avg_gpa', 3.0) for c in combo]), 2),
                        'total_workload': sum(c.get('avg_workload_hours', 10) for c in combo),
                        'schedule_score': 0
                    }
                    
                    schedule['schedule_score'] = round(
                        self.calculate_schedule_score(list(combo), user_profile), 3
                    )
                    
                    valid_schedules.append(schedule)
                    
                    # Stop if we have enough schedules
                    if len(valid_schedules) >= num_schedules * 3:
                        break
            
            # Stop if we have enough valid schedules
            if len(valid_schedules) >= num_schedules * 2:
                break
        
        # Sort by schedule score (descending)
        valid_schedules.sort(key=lambda x: x['schedule_score'], reverse=True)
        
        return valid_schedules[:num_schedules]
