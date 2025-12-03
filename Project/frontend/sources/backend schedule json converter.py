import json
import scheduleGrading
from numpy._core.numeric import nan
import pandas as pd
import numpy as np
df = pd.read_csv(r'C:\Users\kenny\Desktop\CS 124 H\1101-modified+RMP-2025-sp.csv')
returnList = []
def convertScheduleListToJson(scheduleList):
    for schedule in scheduleList:
        scheduleList = []
        for sectionIndex in schedule:
            sectionDict = {
                "course": df.loc[sectionIndex, 'Code'] + " " + df.loc[sectionIndex, 'Number'],
                "name": df.loc[sectionIndex, 'Name'],
                "description": df.loc[sectionIndex, 'Description'],
                "credit": df.loc[sectionIndex, 'Credit Hours'],
                "degree": df.loc[sectionIndex, 'Degree Attributes'],
                "CRN": df.loc[sectionIndex, 'CRN'],
                "section": df.loc[sectionIndex, 'Section'],
                "term": df.loc[sectionIndex, 'Part of Term'],
                "type": df.loc[sectionIndex, 'Type'],
                "start": df.loc[sectionIndex, 'Start Time'],
                "end": df.loc[sectionIndex, 'End Time'],
                "days": df.loc[sectionIndex, 'Days of Week'],
                "building": df.loc[sectionIndex, 'Building'],
                "room": str(df.loc[sectionIndex, 'Room']),
                "location": df.loc[sectionIndex, 'Bulding'] + " " + str(df.loc[sectionIndex, 'Room']),
                "instructors": df.loc[sectionIndex, 'Instructors']
            }
            scheduleList.append(sectionDict)
        returnList.append([scheduleGrading.grade(schedule),scheduleList])
    return json.dumps(returnList, indent=4)

sampleCourseDict = {
    "course": "CS 124",
    "name": "Introduction to Computer Science I",
    "description": "Basic concepts in computing and fundamental techniques for solving computational problems. Intended as a first course for computer science majors and others with a deep interest in computing. Credit is not given for both CS 124 and CS 125. Prerequisite: Three years of high school mathematics or MATH 112.",
    "credit": "3 hours.",
    "degree": "Quantitative Reasoning I course.",
    "CRN": 71578,
    "section": "AYF",
    "term": "1",
    "type": "Discussion/Recitation",
    "start": "11:00:00 am",
    "end": "11:50:00 am",
    "days": "11:50:00 am",
    "building": "Campus Instructional Facility",
    "room": "4029",
    "location": "Campus Instructional Facility 4029",
    "instructors": "Challen, G"
}
#if the section is an online one, the end, days, location will be null, while start will be "ARRANGED"