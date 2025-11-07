import pandas as pd
from datetime import datetime, time

class ScheduleGenerator:
    """Generates and sorts course schedules based on preferences"""

    def __init__(self, courses_df):
        self.courses_df = courses_df

    def parse_time(self, time_str):
        """Parse time string to datetime.time object"""
        if pd.isna(time_str) or time_str == '':
            return None
        try:
            return datetime.strptime(time_str.strip(), '%H:%M').time()
        except:
            return None

    def check_time_conflict(self, course1, course2):
        """Check if two courses have time conflicts"""
        # If either course has no time info, no conflict
        if not course1.get('Start Time') or not course2.get('Start Time'):
            return False

        # Check if they share any days
        days1 = set(course1.get('Days of Week', ''))
        days2 = set(course2.get('Days of Week', ''))

        if not days1.intersection(days2):
            return False

        # Parse times
        start1 = self.parse_time(course1['Start Time'])
        end1 = self.parse_time(course1['End Time'])
        start2 = self.parse_time(course2['Start Time'])
        end2 = self.parse_time(course2['End Time'])

        if not all([start1, end1, start2, end2]):
            return False

        # Check for overlap
        return not (end1 <= start2 or end2 <= start1)

    def check_break_conflict(self, schedule, hard_breaks, soft_breaks):
        """
        Check if schedule conflicts with breaks

        Args:
            schedule: List of courses
            hard_breaks: List of time blocks that must be free
            soft_breaks: List of time blocks that are preferred to be free

        Returns:
            tuple: (has_hard_conflict, soft_conflict_count)
        """
        hard_conflict = False
        soft_conflict_count = 0

        for course in schedule:
            if not course.get('Start Time') or not course.get('Days of Week'):
                continue

            course_start = self.parse_time(course['Start Time'])
            course_end = self.parse_time(course['End Time'])
            course_days = set(course['Days of Week'])

            # Check hard breaks
            for break_block in hard_breaks:
                break_days = set(break_block.get('days', ''))
                if course_days.intersection(break_days):
                    break_start = self.parse_time(break_block['start'])
                    break_end = self.parse_time(break_block['end'])

                    if not (course_end <= break_start or course_start >= break_end):
                        hard_conflict = True
                        break

            # Check soft breaks
            for break_block in soft_breaks:
                break_days = set(break_block.get('days', ''))
                if course_days.intersection(break_days):
                    break_start = self.parse_time(break_block['start'])
                    break_end = self.parse_time(break_block['end'])

                    if not (course_end <= break_start or course_start >= break_end):
                        soft_conflict_count += 1

        return hard_conflict, soft_conflict_count

    def generate_schedules(self, selected_crns, hard_breaks=None, soft_breaks=None):
        """
        Generate valid schedules from selected CRNs

        Args:
            selected_crns: List of CRN lists (one list per course with multiple sections)
            hard_breaks: Time blocks that must be free
            soft_breaks: Time blocks preferred to be free

        Returns:
            list: Valid schedules (list of course combinations)
        """
        hard_breaks = hard_breaks or []
        soft_breaks = soft_breaks or []

        # Get all courses for the selected CRNs
        all_courses = []
        for crn_list in selected_crns:
            course_sections = []
            for crn in crn_list:
                course = self.courses_df[self.courses_df['CRN'] == int(crn)]
                if len(course) > 0:
                    course_sections.append(course.iloc[0].to_dict())
            all_courses.append(course_sections)

        # Generate all possible combinations
        def generate_combinations(courses_list, current_schedule=[]):
            if not courses_list:
                return [current_schedule]

            schedules = []
            for section in courses_list[0]:
                # Check for conflicts with current schedule
                has_conflict = False
                for existing_course in current_schedule:
                    if self.check_time_conflict(section, existing_course):
                        has_conflict = True
                        break

                if not has_conflict:
                    schedules.extend(
                        generate_combinations(courses_list[1:], current_schedule + [section])
                    )

            return schedules

        valid_schedules = generate_combinations(all_courses)

        # Filter by hard breaks
        schedules_without_hard_conflicts = []
        for schedule in valid_schedules:
            has_hard_conflict, _ = self.check_break_conflict(schedule, hard_breaks, soft_breaks)
            if not has_hard_conflict:
                schedules_without_hard_conflicts.append(schedule)

        return schedules_without_hard_conflicts

    def score_schedule(self, schedule, preferences, soft_breaks=None):
        """
        Score a schedule based on preferences

        Args:
            schedule: List of courses
            preferences: Dict with weights for different criteria
                - rmp_weight: Weight for RMP ratings
                - gpa_weight: Weight for GPA
                - time_preference: 'early', 'late', or 'compact'
                - break_weight: Weight for avoiding soft break conflicts

        Returns:
            float: Score (higher is better)
        """
        soft_breaks = soft_breaks or []
        score = 0

        # RMP scoring
        if preferences.get('rmp_weight', 0) > 0:
            rmp_scores = [c.get('RMP', 0) or 0 for c in schedule]
            avg_rmp = sum(rmp_scores) / len(rmp_scores) if rmp_scores else 0
            score += avg_rmp * preferences['rmp_weight']

        # GPA scoring (calculate from grade distribution)
        if preferences.get('gpa_weight', 0) > 0:
            gpa_scores = []
            for course in schedule:
                grade_dist = course.get('Mean Grade By Professor (A+..F,W,Students)')
                if grade_dist:
                    # Simple GPA calculation (A+ = 4.0, A = 4.0, etc.)
                    # This is a placeholder - adjust based on your actual data format
                    gpa_scores.append(3.5)  # placeholder
            avg_gpa = sum(gpa_scores) / len(gpa_scores) if gpa_scores else 0
            score += avg_gpa * preferences['gpa_weight']

        # Time preference scoring
        if preferences.get('time_preference'):
            pref = preferences['time_preference']
            times = [(self.parse_time(c.get('Start Time')), c) for c in schedule if c.get('Start Time')]

            if pref == 'early' and times:
                avg_start = sum([t[0].hour * 60 + t[0].minute for t in times]) / len(times)
                score += (1440 - avg_start) / 1440 * 10  # Normalize to 0-10

            elif pref == 'late' and times:
                avg_start = sum([t[0].hour * 60 + t[0].minute for t in times]) / len(times)
                score += avg_start / 1440 * 10

            elif pref == 'compact' and times:
                # Prefer courses close together
                sorted_times = sorted(times, key=lambda x: x[0])
                if len(sorted_times) > 1:
                    compactness = 0
                    for i in range(len(sorted_times) - 1):
                        time_diff = (sorted_times[i+1][0].hour * 60 + sorted_times[i+1][0].minute) - \
                                   (sorted_times[i][0].hour * 60 + sorted_times[i][0].minute)
                        compactness += max(0, 180 - time_diff) / 180  # Prefer within 3 hours
                    score += compactness / (len(sorted_times) - 1) * 10

        # Soft break penalty
        if preferences.get('break_weight', 0) > 0:
            _, soft_conflicts = self.check_break_conflict(schedule, [], soft_breaks)
            score -= soft_conflicts * preferences['break_weight']

        return score

    def sort_schedules(self, schedules, preferences, soft_breaks=None, limit=200):
        """
        Sort schedules by score and return top N

        Args:
            schedules: List of schedules
            preferences: Preference weights
            soft_breaks: Soft break time blocks
            limit: Maximum number of schedules to return

        Returns:
            list: Sorted schedules with scores
        """
        scored_schedules = []
        for schedule in schedules:
            score = self.score_schedule(schedule, preferences, soft_breaks)
            scored_schedules.append({
                'schedule': schedule,
                'score': score
            })

        # Sort by score (descending)
        scored_schedules.sort(key=lambda x: x['score'], reverse=True)

        return scored_schedules[:limit]
