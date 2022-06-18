from http.client import CannotSendRequest
from pickle import TRUE
from tracemalloc import start
from turtle import update
from unittest import result
from urllib.parse import _NetlocResultMixinStr
from pkg_resources import resource_listdir
import pymongo

# ---- connecting the mongoDB database
myclient = pymongo.MongoClient("mongodb+srv://mongo:bShxLstlQzls2QZO@cluster0.1f7n9.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["dynamic_designs"]
mycol = mydb["courses"]


class userInfo:
    def __init__(self, name, creditHr, courseList, summer, summerCreditHr, startSem):
        self.name = name
        self.creditHr = creditHr
        self.courseList = courseList
        self.summer = summer
        self.summerCreditHr = summerCreditHr
        self.startSem = startSem

class courseInfo:
    def setType(self, type):
        self.type = type
    def getType(self):
        return self.type
    def setTerm(self, term):
        self.term = term
    def getTerm(self):
        return self.term
    def setCourses(self, courses):
        self.courses = courses
    def getCourses(self):
        return self.courses

def create_Query(varTerm, varType):
    criteria1 = {}
    criteria2 = {}
    criteria1['term'] = varTerm
    criteria2['type'] = varType
    mylist = []
    mylist.append(criteria1)
    mylist.append(criteria2)
    filter = {"$and": "fall"}
    filter["$and"] = mylist
    return filter

def query_Class(myFilter, usrCourses):
    mydoc = mycol.find(myFilter)

    #store all queries in a dictionary 
    count = 1
    availCourses = {}
    for x in mydoc:
        #print(x)
        availCourses.update({count: x})
        count = count + 1

    #print("printing available documents.....\n")
    #print(availCourses)

    # removes all courses that has already been taken

    delete = []
    for items in availCourses:
        for x in usrCourses:
            if x in availCourses[items].values():
                delete.append(items)

    for i in delete:
        del availCourses[i]

    return availCourses

def updateCourse(list, var):
    list.append(var)
    return list

def updateResult(var):
    newlist = updateCourse(thisClass.getCourses(), var)
    thisClass.setCourses(newlist)

def printResult(printCourses):
    for x in printCourses:
        courseMatch = (printCourses[x]['_id'])
    print (courseMatch)
    updateResult(courseMatch)

def checkReqs(usrList):
    bool = False
    # ---- STEP1: remove elective courses from the user list
    electiveCourses = ['ET505', 'ET585', 'ET583', 'BCIS550', 'BCIS575', 'BCIS561', 'BCIS566', 'BCIS585', 'CS502', 'CS508', 'CS511', 'CS519', 'IE523', 'IE563', 'IE571']
    baseCourses = ['ET551', 'ET552', 'ET562', 'ET555', 'ET595', 'ET577', 'ET539']
    usrBase = usrList
    usrElective = []
    # separates elective courses from base courses
    # to check if requirements are met

    for ele in electiveCourses:
        count = 0
        for ele2 in usrBase:
            if ele == ele2:
                usrElective.append(ele)
                usrBase.pop(count)
            count = count + 1

    # ------ STEP 2: check if base courses are met

    baseCourses.sort()
    usrBase.sort()

    # ---- checking results)
    if usrBase == baseCourses:
        #print ("base courses are completed!")
        if (len(usrElective) >= 3):
            #print('electives are met')
            bool = True
        else:
            bool = False
            #print('core requirements are met but we need more electives')
    else:
        bool = False
        #print("no requirements are met")
    newlist = usrBase + usrElective
    thisClass.setCourses(newlist)
    return bool


def next_semester(curSem, summer):
    if curSem == 'fall':
        newSem = 'spring'
        # return startSem
    if curSem == 'spring':
        if summer == True:
            newSem = 'summer'
        else:
            newSem = 'fall'
    if curSem == 'summer':
        newSem = 'fall'
    thisClass.setTerm(newSem)

def calcCredits():
    if thisClass.getTerm() == 'summer':
        curCredit = user.summerCreditHr / 3
    else:        
        curCredit = user.creditHr / 3
    return curCredit
# myquery = create_Query(th)
# ---- user input from php form
user = userInfo('Evelyn', 6, ['ET551', 'ET552'], True, 3, 'spring')

# ---- grabs info for the script
thisClass = courseInfo()
thisClass.setCourses(user.courseList)
thisClass.setTerm(user.startSem)
thisClass.setType('base')


# ---- creates the filter for the query



# ---- runs a query and returns all the classes that are available

# ----- returns the list of all available courses

# prints the first available course for 

print("Hi " + user.name + ", here is your proposed degree plan\n")
while checkReqs(thisClass.getCourses()) == False:
    #print("this iteration is " + str(count))
    z = calcCredits()
    i = 0
    myQuery = create_Query(thisClass.getTerm(), thisClass.getType())
    print(thisClass.getTerm() + ": ")
    while i < z:
        results = query_Class(myQuery, thisClass.getCourses())
        printCourses = results
        if (len(printCourses)) >= 1:
            printResult(printCourses)
        else:
            newfilter = create_Query(thisClass.getTerm(), 'elective')
            resultsEle = query_Class(newfilter, thisClass.getCourses())
            printResult(resultsEle)
        i= i + 1
    next_semester(thisClass.getTerm(), user.summer)






