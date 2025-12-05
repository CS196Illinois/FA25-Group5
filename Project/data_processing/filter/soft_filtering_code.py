import pandas as pd
import hard_filtering_code as hf
import numpy as np
from numpy import nan
import os
import ast
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
csv_path = os.path.join(script_dir, "../../datasets/11-7-2025-sp.csv")
df = pd.read_csv(csv_path)

#/////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////

prof_weight_excellent = 0.7
prof_weight_oustanding = 1.0

def prof_eo(index):
    if np.isnan(df.loc[index, 'Excellent']) or np.isnan(df.loc[index, 'Outstanding']):
        return -1
    value = df.loc[index, 'Excellent'] * prof_weight_excellent + df.loc[index, 'Outstanding'] * prof_weight_oustanding + 1
    result = np.log(value) / np.log(21)  # log base 21
    return result

def prof_RMP(index):
    if np.isnan(df.loc[index, 'RMP']):
        return -1
    return df.loc[index, 'RMP'] * 20

def prof_score(index, weight_eo, weight_RMP):
    weight = 0
    total = 0
    if prof_eo(index) != -1:
        weight += weight_eo * prof_eo(index)
        total += weight_eo
    if prof_RMP(index) != -1:
        weight += weight_RMP * prof_RMP(index)
        total += weight_RMP
    if total == 0:
        return -1
    return weight / total

#/////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////

gpa_map = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0, 'W': 0.0
}

def parse_grade_list(grades):
    """Convert CSV string to list of floats if needed."""
    if isinstance(grades, str):
        grades = ast.literal_eval(grades)
    return [float(x) for x in grades]

def avg_gpa_from_list(grades):
    """Calculate GPA from a grade list (last element = total students)."""
    grades = parse_grade_list(grades)
    total_students = grades[-1]
    grade_counts = grades[:-1]
    weighted_sum = sum(gpa * count for gpa, count in zip(gpa_map.values(), grade_counts))
    return weighted_sum / total_students if total_students > 0 else -1

def gpa_score(index, weight_prof, weight_class):
    """Return (professor + class GPA)  for a given CRN."""
    if df.loc[index, 'CRN'] == nan:
        return -1

    prof_grades = df.loc[index, "Mean Grade By Professor (A+..F,W,Students)"]
    class_grades = df.loc[index, "Mean Grade By Class (A+..F,W,Students)"]

    if prof_grades == nan and class_grades == nan:
        return -1
    elif prof_grades == nan:
        return avg_gpa_from_list(class_grades)
    elif class_grades == nan:
        return avg_gpa_from_list(prof_grades)
    else:
        return (avg_gpa_from_list(prof_grades) * weight_prof + avg_gpa_from_list(class_grades) * weight_class) / (weight_prof + weight_class)

def percent_ge_from_list(grades, threshold):
    """Calculate percentage of students with GPA >= threshold."""
    grades = parse_grade_list(grades)
    total_students = grades[-1]
    grade_counts = grades[:-1]
    above_count = sum(count for gpa, count in zip(gpa_map.values(), grade_counts) if gpa >= threshold)
    return (above_count / total_students) * 100 if total_students > 0 else -1

def percent_ge(index, threshold):
    if df.loc[index, 'Mean Grade By Professor (A+..F,W,Students)'] == nan and df.loc[index, 'Mean Grade By Class (A+..F,W,Students)'] == nan:
        return -1
    grades = df.loc[index, 'Mean Grade By Professor (A+..F,W,Students)'] if df.loc[index, 'Mean Grade By Professor (A+..F,W,Students)'] != nan else df.loc[index, 'Mean Grade By Class (A+..F,W,Students)']
    return percent_ge_from_list(grades, threshold)

def class_score(index, weight_prof, weight_class, weight_percentage, min_gpa):
    """Sum RMP sum + GPA score + %prof >= min_gpa1 + %class >= min_gpa2."""
    gpa_val = gpa_score(index, weight_prof, weight_class)
    percentage = percent_ge(index, min_gpa)
    weight = 0
    total = 0
    weight_average = (weight_prof + weight_class) / 2.0
    if gpa_val != -1:
        weight += weight_average * gpa_val
        total += weight_average
    if percentage != -1:
        weight += weight_percentage * percentage
        total += weight_percentage
    if total == 0:
        return -1
    return weight / total

#/////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////

def softbreak_time(timespace):
    number = 0
    for i in range(0, 5):
        for j in range(0, 90):
            if timespace[i][j] != 0:
                number += 1
    return number

def softbreak_conflict(index, timespace):
    number = 0
    newTimespace = hf.hardFilter_toTimespace(index)
    for i in range(0, 5):
        for j in range(0, 90):
            if timespace[i][j] != 0 and newTimespace[i][j] != 0:
                number += 1
    return number

def softbreak_score(indexList, timespace):
    totalTime = softbreak_time(timespace)
    if totalTime == 0:
        return 1.0
    countTime = 0
    for index in indexList:
        countTime += softbreak_conflict(index)
    return 1.0 - countTime * 1.0 / totalTime

#/////////////////////////////////////////////////////////////////////////////////////////////

#/////////////////////////////////////////////////////////////////////////////////////////////

def distance_score(index):
    return 1