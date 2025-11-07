import pandas as pd
import os

class DataLoader:
    """Handles loading and caching course data"""

    def __init__(self):
        self.df = None
        # Use absolute path to datasets folder
        self.data_path = '/Users/jadewu/Documents/GitHub/FA25-Group5/datasets/2025-sp-modified.csv'

    def load_data(self):
        """Load course data from CSV"""
        if self.df is None:
            print(f"Loading data from: {self.data_path}")
            self.df = pd.read_csv(self.data_path)
            print(f"Loaded {len(self.df)} courses")
        return self.df

    def get_courses(self, filters=None):
        """
        Get courses with optional filters

        Args:
            filters (dict): Dictionary of filters to apply
                - subject: Subject code (e.g., 'CS')
                - number: Course number
                - crn: Course CRN
                - instructor: Instructor name
                - days: Days of week
                - credit_hours: Credit hours

        Returns:
            list: List of course dictionaries
        """
        df = self.load_data()

        if filters:
            if 'subject' in filters and filters['subject']:
                df = df[df['Code'] == filters['subject']]

            if 'number' in filters and filters['number']:
                df = df[df['Number'] == str(filters['number'])]

            if 'crn' in filters and filters['crn']:
                df = df[df['CRN'] == int(filters['crn'])]

            if 'instructor' in filters and filters['instructor']:
                df = df[df['Primary Instructor (Concat)'].str.contains(filters['instructor'], case=False, na=False)]

            if 'days' in filters and filters['days']:
                df = df[df['Days of Week'].str.contains(filters['days'], case=False, na=False)]

        return df.to_dict('records')

    def get_course_by_crn(self, crn):
        """Get specific course by CRN"""
        df = self.load_data()
        course = df[df['CRN'] == int(crn)]
        if len(course) > 0:
            return course.iloc[0].to_dict()
        return None

    def get_unique_subjects(self):
        """Get list of unique subjects"""
        df = self.load_data()
        return sorted(df['Code'].unique().tolist())

    def get_courses_by_subject(self, subject):
        """Get all courses for a specific subject"""
        df = self.load_data()
        courses = df[df['Code'] == subject]
        return courses[['Number', 'Name', 'CRN']].drop_duplicates().to_dict('records')

# Singleton instance
data_loader = DataLoader()
