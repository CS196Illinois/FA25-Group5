#timespace: int[5][90] = {0} -> 5 days, 90 time slots (7:00-22:00, 10 min each)
#courses: [] -> integers representing the row of section
#endlist: [[]] -> list of list for course sections
import pandas as pd


def timeToInt(timeString):
    hours = int(timeString.split(':')[0])
    minutes = int(timeString.split(':')[1])
    amPm = timeString.split(' ')[1]
    timeInt = hours * 6 + minutes // 10
    if amPm == 'pm':
        timeInt += 72
    return timeInt - 42 #7:00 is the start time

def hardFilter_toTimespace(section): #unfinished, need to get data from dataset
    timespace[5][90] = 0
    #return the timespace for the course in format of int[5][90]
    for i in range(timeToInt(startTime), timeToInt(endTime)):
        if week.contains('M'):
            timespace[0][i] = 1
        if week.contains('T'):
            timespace[1][i] = 1
        if week.contains('W'):
            timespace[2][i] = 1
        if week.contains('R'):
            timespace[3][i] = 1
        if week.contains('F'):
            timespace[4][i] = 1
    return timespace

def hardFilter_addTime(timespace1, timespace2): 
    #add two timespace together
    for i in range(5):
        for j in range(90):
            timespace1[i][j] = timespace1[i][j] + timespace2[i][j]
    return timespace1

def hardFilter_checkConflict(timespace):
    #check conflict in the timespace
    for i in range(5):
        for j in range(90):
            if timespace[i][j] > 1:
                return True
    return False

#make sure the section group has no conflict
def hardFilter_dfs(courses, timespace, sections, endlist):# unfinished need to make sure endlist works well
    #return if all section has no conflict

    df = pd.read_csv("modified-2025-sp")

    if courses.size == 0:
        return [sections]

    # only using time data from 2025
    for i in df[df['Subject'].str.contains(courses[0].split(' ')[0]) and df['Number'].str.contains(courses[0].split(' ')[1])]['Row']: #unfinished, check whether df is correct
        newTimespace = hardFilter_addTime(timespace, hardFilter_toTimespace(i))
        if not hardFilter_checkConflict(newTimespace):
            endlist += hardFilter_dfs(courses[1:], newTimespace, sections + i)

    return endlist





def hardFilter(inputTimespace, courses):
    #inputTimespace is the hard preference time constraint
    return hardFilter_dfs(courses, inputTimespace, [], [])


#need to consider NaN situations

print(timeToInt("8:30:00 am"))