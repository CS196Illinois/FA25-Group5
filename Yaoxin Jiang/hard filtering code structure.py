#timespace: int[5][90] = {0} -> 5 days, 90 time slots (7:00-22:00, 10 min each)
#courses: [] -> integers representing the row of section
#endlist: [[]] -> list of list for course sections

def hardFilter_toTimespace(section): #unfinished
    #return the timespace for the course in format of bool[5][90]
    return 

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
def hardFilter_dfs(courses, timespace, coursesCopy, endlist):# unfinished need to make sure endlist works well
    #return if all section has no conflict
    if courses.size == 0:
        return [coursesCopy]

    for i in sectionsOf(courses[0]): #unfinished, require a function to get all sections of a course
        newTimespace = hardFilter_addTime(timespace, hardFilter_toTimespace(i))
        if not hardFilter_checkConflict(newTimespace):
            endlist += hardFilter_dfs(courses[1:], newTimespace, coursesCopy)

    return endlist





def hardFilter(inputTimespace, courses):
    #inputTimespace is the hard preference time constraint
    return hardFilter_dfs(courses, inputTimespace, courses, [])


#need to consider NaN situations