#timespace: int[5][90] = {0} -> 5 days, 90 time slots (7:00-22:00, 10 min each)
#courses: [] -> integers representing the row of section
#endlist: [[]] -> list of list for course sections
from numpy._core.numeric import nan
import pandas as pd
import numpy as np
df = pd.read_csv(r'C:\Users\kenny\Desktop\CS 124 H\1101-modified+RMP-2025-sp.csv')
#need to change directory to the location of the csv file

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

def hardFilter_addSectionDfs(courses, timespace, sectionIndexes, newSectionIndex):
    newTimespace = timespace + hardFilter_toTimespace(newSectionIndex)
    if not np.any(newTimespace > 1):
        return hardFilter_dfs(courses, newTimespace, sectionIndexes + [newSectionIndex])
    else:
        return []

def hardFilter_ParseLinkedSection(currentLinkedSectionList, courses, timespace, sectionIndexes):
    if len(currentLinkedSectionList) == 0:
        return []
    if len(currentLinkedSectionList) == 1:
        return hardFilter_addSectionDfs(courses, timespace, sectionIndexes, currentLinkedSectionList[0])

    returnList = []

    if (len(df.loc[currentLinkedSectionList[0], "Section"]) == 1) or (df.loc[currentLinkedSectionList[0], "Section"][1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
         for tempIndex in currentLinkedSectionList:
            returnList += hardFilter_addSectionDfs(courses, timespace, sectionIndexes, tempIndex)
         return returnList
    
    currentClassType = df.loc[currentLinkedSectionList[0], "Section"][1]
    currentClassTypeList = []
    currentIndex = 0
    
    while df.loc[currentLinkedSectionList[currentIndex], "Section"][1] == currentClassType:
        currentClassTypeList += [currentLinkedSectionList[currentIndex]]
        currentIndex += 1
        if currentIndex == len(currentLinkedSectionList):
            break
    
    if currentIndex < len(currentLinkedSectionList):
        for tempIndex in currentClassTypeList:
            newTimespace = timespace + hardFilter_toTimespace(tempIndex)
            if not np.any(newTimespace > 1):
                returnList += hardFilter_ParseLinkedSection(currentLinkedSectionList[currentIndex:], courses, newTimespace, sectionIndexes + [tempIndex])
    else:
        for tempIndex in currentClassTypeList:
            returnList += hardFilter_addSectionDfs(courses, timespace, sectionIndexes, tempIndex)
    
    return returnList

def hardFilter_parseSection(sectionListIndex, courses, timespace, sectionIndexes):
    returnList = []
    if (df.loc[sectionListIndex[0], "Section"] is nan):
        for tempIndex in sectionListIndex:
            returnList += hardFilter_addSectionDfs(courses, timespace, sectionIndexes, tempIndex)
        return returnList
    currentLinkedSection = df.loc[sectionListIndex[0], "Section"][0]
    currentIndex = 0
    while (currentIndex < len(sectionListIndex)):
        currentLinkedSectionList = []

        while (df.loc[sectionListIndex[currentIndex], "Section"][0] == currentLinkedSection):
            currentLinkedSectionList += [sectionListIndex[currentIndex]]
            currentIndex += 1
            if currentIndex == len(sectionListIndex):
                break
        returnList += hardFilter_ParseLinkedSection(currentLinkedSectionList, courses, timespace, sectionIndexes)

        if currentIndex == len(sectionListIndex):
            break
        currentLinkedSection = df.loc[sectionListIndex[currentIndex], "Section"][0]

    return returnList

def hardFilter_printSchedule(sectionIndexes):
    print("Found valid schedule: ", end = " ")
    for i in sectionIndexes:
        print(addSpace(df.loc[i, 'Code'], 5) + " " + str(df.loc[i, 'Number']) + " " + addSpace(str(df.loc[i, 'Section']), 3), end = " | ")
    print()
    return

#make sure the section group has no conflict
def hardFilter_dfs(courses, timespace, sectionIndexes):# unfinished need to make sure endlist works well
    #return if all section has no conflict
    if len(courses) == 0:
        #hardFilter_printSchedule(sectionIndexes)
        return [sectionIndexes]

    endlist = []
    # only using time data from 2025
    #v1.0 has code: for i in df.index(df['Subject'] == courses[0].split(' ')[0] & df['Number'] == courses[0].split(' ')[1]):

    #v1.1 for this part, I changed it to the following:
    matchClass = ( (df['Code'] == courses[0].split(' ')[0]) & (df['Number'] == int(courses[0].split(' ')[1])) )

    if not df.loc[matchClass].empty: #check if there is any section for the course
        endlist += hardFilter_parseSection(df.loc[matchClass].index, courses[1:], timespace, sectionIndexes)
        #for i in df.loc[matchClass].index:
        #    endlist += hardFilter_addSectionDfs(courses[1:], timespace, sectionIndexes, i)
    else:
        endlist += hardFilter_dfs(courses[1:], timespace, sectionIndexes) #if there is no section for the course, skip it

    return endlist

def hardFilter_crnToIndex(crn):
    matchClass = (df['CRN'] == crn)
    if not df.loc[matchClass].empty:
        return df.loc[matchClass].index[0]
    else:
        return -1 #invalid CRN



def hardFilter(inputTimespace, courses, CRNs):
    #inputTimespace is the hard preference time constraint
    #will skip invalid course names & CRNs
    for crn in CRNs:
        if hardFilter_crnToIndex(crn) != -1:
            if not np.any(inputTimespace + hardFilter_toTimespace(hardFilter_crnToIndex(crn)) > 1):
                inputTimespace += hardFilter_toTimespace(hardFilter_crnToIndex(crn))
    return hardFilter_dfs(courses, inputTimespace, [])

#need to consider NaN situations
    #Actually we don't have to because for every course ther will definitely be a time range
    #only need to consider when there is no section available
        #done considering this situation

#test code
def addSpace(s, num):
    while len(s) < num:
        s += " "
    return s

def checkCode(result):
    for sections in result:
        for i in sections:
            print(addSpace(df.loc[i, 'Code'], 5) + " " + str(df.loc[i, 'Number']) + " " + addSpace(str(df.loc[i, 'Section']), 3), end = " | ")
        print()

inputTimespace = np.zeros((5, 90), dtype=int)
#example timespace preference: free on all times
courses = ["CHEM 103", "MATH 241", "ECE 120"]
#example classes
hardFilter(inputTimespace, courses, [])