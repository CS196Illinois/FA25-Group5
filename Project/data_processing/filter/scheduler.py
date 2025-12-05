import hard_filtering_code as hf
import soft_filtering_code as sf
import pandas as pd
import numpy as np
from numpy import nan
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
csv_path = os.path.join(script_dir, "../../datasets/11-7-2025-sp.csv")
df = pd.read_csv(csv_path)

def find_courses(department):
    """
    Find all courses for a given department code (e.g., "CS")
    Returns a list of dictionaries with course number and name
    """
    # Filter dataframe for the given department
    dept_courses = df[df['Code'] == department.upper()]

    # Get unique courses (since there can be multiple sections of the same course)
    unique_courses = dept_courses.drop_duplicates(subset=['Number', 'Name'])

    # Create list of JSON objects with number and name
    course_list = []
    for _, row in unique_courses.iterrows():
        course_list.append({
            "number": str(row['Number']),
            "name": row['Name']
        })

    return course_list


def generate_schedule(course_list, CRN_list, time_breaks, soft_preferences):
    """
    generate and rank schedules
    return top 10 schedules
    """
    #hard break: 2, soft break: 1, empty: 0
    hard_breaks = np.where(time_breaks == 2, 5, 0)
    soft_breaks = np.where(time_breaks == 1, 1, 0)

    # generate all valid schedules based on hard preferences
    valid_schedules = hf.hardfilter(hard_breaks, course_list, CRN_list)
    

    # ccore each schedule based on soft preferences
    scored_schedules = score_schedules(valid_schedules, soft_preferences, soft_breaks)

    #return top 10
    top_schedules = sorted(scored_schedules, key=lambda x: x['score'], reverse=True)[:10]

    return top_schedules


# def generate_valid_schedules(course_list, CRN_list, hard_breaks):
#     """
#     Hard preferences
#     coure lists, CRN, hard breaks
#     """
#     # put my algo to generate schedules here
#     valid_schedules = []

#     #here call hardfilter


#     valid_schedules.append(example_schedule)

#     return valid_schedules


def score_schedules(schedules, soft_prefs, soft_breaks):
    """
    1. Soft preferences (importtance of 1-5 of how much the user cares about the below two)
    rate my professor score(1-5 of how much they care
    professor excellence and oustanding rating(1-5 of how much they care

    2. class difficulty(importtance of 1-5 of how much the user cares about the below two)
    professor average GPA ((1-5 of how much they care
    class average GPA ((1-5 of how much they care
    minimum acceptable GPA (A+ to F)

    3. Locations(importtance of 1-5 of how much the user cares about the below two)
     maximum late minues(0-30minutes)
    location selected as center(out of the optioins we provided on the website)
    promixity to center point(in km)

     Expected soft_prefs structure:
  {
      "professor_importance": int (1-5),
      "rmp_score_weight": int (1-5),
      "professor_excellence_weight": int (1-5),
      "difficulty_importance": int (1-5),
      "professor_gpa_weight": int (1-5),
      "class_gpa_weight": int (1-5),
      "acceptable_gpa_weight": int (1-5),
      "min_acceptable_gpa": str ("A+" to "F"),
      "softbreak_importance": int (1-5)
  }
    """
    scored = []

    for schedule in schedules:
        # NEED UPDATES HERE 
        prof_score = sf.prof_score(schedule, soft_prefs[1], soft_prefs[2])
        class_score = sf.class_score(schedule, soft_prefs[4], soft_prefs[5], soft_prefs[6], soft_prefs[7])
        softbreak_score = sf.softbreak_score(schedule, soft_breaks)
        # location_score = calculate_location_score(schedule, soft_prefs)

        #weights from soft preferences 

        # Calculate final weighted score 

        
        final_score = (
            prof_score * soft_prefs[0] +
            class_score * soft_prefs[3] +
            softbreak_score * soft_prefs[8]
        )

        #df.loc[section, '']

        returnSchedule = []
        for section in schedule:
            returnSchedule.append({
                "course": df.loc[section, 'Code'] + " " + df.loc[section, 'Number'],
                "name": df.loc[section, 'Name'],
                "description": df.loc[section, 'Description'],
                "credit": df.loc[section, 'Credit Hours'],
                "degree": df.loc[section, 'Degree Attributes'],
                "CRN": int(df.loc[section, 'CRN']),
                "section": df.loc[section, 'Section'],
                "term": df.loc[section, 'Part of Term'],
                "type": df.loc[section, 'Type'],
                "start": df.loc[section, 'Start Time'],
                "end": df.loc[section, 'End Time'],
                "days": df.loc[section, 'Days of Week'],
                "location": (df.loc[section, 'Building'] + " " + df.loc[section, 'Room']).strip(),
                "instructors": df.loc[section, 'Instructors']
            })

        scored.append({
            "score": final_score,
            "schedule": returnSchedule
        })

    return scored

