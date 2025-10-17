#timespace: int[5][90] = {0} -> 5 days, 90 time slots (7:00-22:00, 10 min each)
#courses: [] -> integers representing the row of section
#endlist: [[]] -> list of list for course sections
import pandas as pd
import numpy as np
df = pd.read_csv(r'C:\Users\kenny\source\repos\FA25-Group5\Yaoxin Jiang\modified-2025-sp (with RMP).csv')


def timeToInt(timeString):
    hours = int(timeString.split(':')[0])
    minutes = int(timeString.split(':')[1].split(' ')[0])
    amPm = timeString.split(' ')[1]
    timeInt = hours * 6 + minutes // 10
    if (amPm == 'pm') & (hours != 12): #12:00 pm is 12:00, not 24:00 and there is no 12:00 am in the data
        timeInt += 72
    return timeInt - 42 #7:00 is the start time

def hardFilter_toTimespace(sectionIndex):
    timespace = np.zeros((5, 90), dtype=int) # 2D Int Array representing 5 days, 90 time slots (7:00-22:00, 10 min each)
    if df.loc[sectionIndex, 'Start Time'] == "ARRANGED":
        return timespace

    #if there is no weekday, the start time will be arranged, no need to consider this situation
    #return the timespace for the course in format of int[5][90]
    dayMap = {'M': 0, 'T': 1, 'W': 2, 'R': 3, 'F': 4}
    for i in range(timeToInt(df.loc[sectionIndex, 'Start Time']), timeToInt(df.loc[sectionIndex, 'End Time'])):
        for day in df.loc[sectionIndex, 'Days of Week']:
            timespace[dayMap[day]][i] = 1
    return timespace

#deleted hardFilter_addTime and hardFilter_checkConflict methods, merged them into hardFilter_dfs method

#make sure the section group has no conflict
def hardFilter_dfs(courses, timespace, sectionIndexes):# unfinished need to make sure endlist works well
    #return if all section has no conflict

    
    if len(courses) == 0:
        return [sectionIndexes]

    endlist = []
    # only using time data from 2025
    #v1.0 has code: for i in df.index(df['Subject'] == courses[0].split(' ')[0] & df['Number'] == courses[0].split(' ')[1]):

    #v1.1 for this part, I changed it to the following:
    matchClass = ( (df['Subject'] == courses[0].split(' ')[0]) & (df['Number'] == int(courses[0].split(' ')[1])) )

    if not df.loc[matchClass].empty: #check if there is any section for the course
        for i in df.loc[matchClass].index:
            newTimespace = timespace + hardFilter_toTimespace(i) #add the timespace of the new section to the existing timespace
            if not np.any(newTimespace > 1):
                endlist += hardFilter_dfs(courses[1:], newTimespace, sectionIndexes + [i])
    else:
        endlist += hardFilter_dfs(courses[1:], timespace, sectionIndexes) #if there is no section for the course, just skip it

    return endlist





def hardFilter(inputTimespace, courses):
    #inputTimespace is the hard preference time constraint
    return hardFilter_dfs(courses, inputTimespace, [])

#need to consider NaN situations
    #Actually we don't have to because for every course ther will definitely be a time range
    #only need to consider when there is no section available
        #done considering this situation

#test code
inputTimespace = np.zeros((5, 90), dtype=int)
courses = ["CHEM 103", "MATH 241", "TE 200", "LAS 100", "LAS 101"]
print(hardFilter(inputTimespace, courses))