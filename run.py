#!python2
from flask import Flask
from flask import request
from flaskext.mysql import MySQL
from ast import literal_eval as make_tuple
import json
import os

app = Flask(__name__)

mysql = MySQL()


mysql.init_app(app)
#
# app.config['MYSQL_DATABASE_USER'] = os.getenv('USER')
# app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('PASSWORD')
# app.config['MYSQL_DATABASE_DB'] = os.getenv('DATABASE')
# app.config['MYSQL_DATABASE_HOST'] = os.getenv('HOST')


app.config['MYSQL_DATABASE_USER'] = 'nssolutions'
app.config['MYSQL_DATABASE_PASSWORD'] = 'rateyoursemester'
app.config['MYSQL_DATABASE_DB'] = 'RateMySemesterDatabase'
app.config['MYSQL_DATABASE_HOST'] = 'ratemysemesterdatabase.c1ouwu6k5kti.us-east-1.rds.amazonaws.com'

conn = mysql.connect()
conn.text_factory = str
cur = conn.cursor()


port = int(os.environ.get("PORT", 5000))






@app.route("/RMS/courseInfo")
def getCourseInfo():

    course = request.args.get('course')
    professor = request.args.get('professor')

    result = None
    returnList = None
    if course == None and professor == None:
        cur.execute('SELECT * from CourseInfo;')
        result = cur.fetchall()

        returnList = "[ "
        count = 0
        for item in result:
            count += 1
            courseData = {}
            courseData["course"] = item[0]
            courseData["professor"] = item[1]
            courseData["gpa"] = float(item[2])
            courseData["credits"] = item[3]
            courseData["major"] = item[4]
            returnList += (json.dumps(courseData))
            if count != len(result):
                returnList += ", "

        returnList += " ]"

    elif course != None and professor == None:
        cur.execute('SELECT * from CourseGPA where courseName = ' + course + ';')
        result = cur.fetchall()
        cur.execute('SELECT AVG(Difficulty), AVG(Workload), AVG(Interest), AVG(Overall) from Semester where CName = ' + course + ';')
        courseResult = cur.fetchall()

        returnList = "[ "
        courseData = {}
        courseData["major"] = result[0][0]
        courseData["course"] = result[0][1]
        courseData["professor"] = ""
        courseData["gpa"] = float(result[0][2])
        for x in courseResult:
            courseData["courseDifficulty"] = str(x[0])
            courseData["courseWorkload"] = str(x[1])
            courseData["courseInterest"] = str(x[2])
            courseData["courseOverall"] = str(x[3])
        returnList += (json.dumps(courseData))
        returnList += " ]"

    elif course != None and professor != None:
        cur.execute('SELECT * from CourseInfo where professor = ' + professor + ' and course = ' + course + ';')
        result = cur.fetchall()
        cur.execute('SELECT AVG(Difficulty), AVG(Workload), AVG(Interest), AVG(Overall) from Semester where CProfessor = ' + professor + ' and CName = ' + course + ';')
        profResult = cur.fetchall()
        cur.execute('SELECT AVG(Difficulty), AVG(Workload), AVG(Interest), AVG(Overall) from Semester where CName = ' + course + ';')
        courseResult = cur.fetchall()


        returnList = "[ "
        count = 0
        for item in result:
            count += 1
            courseData = {}
            courseData["course"] = item[0]
            courseData["professor"] = item[1]
            courseData["gpa"] = float(item[2])
            courseData["credits"] = item[3]
            courseData["major"] = item[4]
            for x in profResult:
                courseData["courseAndProfessorDifficulty"] = str(x[0])
                courseData["courseAndProfessorWorkload"] = str(x[1])
                courseData["courseAndProfessorInterest"] = str(x[2])
                courseData["courseAndProfessorOverall"] = str(x[3])
            for x in courseResult:
                courseData["courseDifficulty"] = str(x[0])
                courseData["courseWorkload"] = str(x[1])
                courseData["courseInterest"] = str(x[2])
                courseData["courseOverall"] = str(x[3])
            returnList += (json.dumps(courseData))
            if count != len(result):
                returnList += ", "
        returnList += " ]"

    return returnList

@app.route("/RMS/courseInfo/majors")
def getMajors():

    cur.execute('SELECT distinct Major from CourseInfo;')
    result = cur.fetchall()
    returnList = "[ "
    count = 0
    for item in result:
        count += 1
        returnList += '"' + (item[0]) + '"'
        #returnList += (json.dumps(courseData))
        if count != len(result):
            returnList += ", "

    returnList += " ]"
    return returnList


@app.route("/RMS/courseInfo/courses")
def getCourses():

    major = request.args.get('major')

    result = None
    if major == None:
        cur.execute('SELECT Course, Major from CourseInfo;')
        result = cur.fetchall()
    if major != None:
        cur.execute('SELECT distinct Course from CourseInfo where Major = ' + major + ';')
        result = cur.fetchall()


    returnList = "[ "

    if major != None:
        count = 0
        for item in result:
            count += 1
            returnList += '"' + (item[0]) + '"'
            #returnList += (json.dumps(courseData))
            if count != len(result):
                returnList += ", "

    else:
        count = 0
        for item in result:
            count += 1
            courseData = {}
            courseData["course"] = item[0]
            courseData["major"] = item[1]
            returnList += (json.dumps(courseData))
            if count != len(result):
                returnList += ", "

    returnList += " ]"
    return returnList

@app.route("/RMS/courseInfo/majorGPAs")
def getCourses2():

    major = request.args.get('major')

    result = None
    if major == None:
        return '[]';

    cur.execute('SELECT Major,GPA from CourseInfo where Major = ' + major + ';')
    result = cur.fetchall()
    if not result: return '[]'

    returnList = "[ "
    data = {}
    data["major"] = result[0][0]
    allGPAs = []
    for item in result:
        allGPAs.append(float(item[1]))
    data["gpas"] = allGPAs
    returnList += (json.dumps(courseData))
    returnList += " ]"
    return returnList

@app.route("/RMS/profile/name")
def getProfileName():

    email = request.args.get('email')
    cur.execute('SELECT First, Last from User where email = ' + email + ';')
    demail = cur.fetchall()
    return demail[0][0] + ' ' + demail[0][1]

@app.route("/RMS/profile/semester/namesAndRatings")
def getSemesterNamesAndRatings():

    email = request.args.get('email')
    cur.execute('SELECT SName, ORating, URating from Rating where email = ' + email + ';')
    data = cur.fetchall()

    noneString = '"' + 'none' + '"'


    returnList = "[ "
    count = 0
    for x in data:
            count += 1

            if str(x[2]) == "None":
                returnList += '{"name": ' + '"' + x[0]+ '", "rating": ' + str(x[1]) + ', "userRating": ' + noneString + '}'
            else:
                returnList += '{"name": ' + '"' + x[0]+ '", "rating": ' + str(x[1]) + ', "userRating": ' + str(x[2]) + '}'
            if count != len(data):
                returnList += ", "

    returnList += " ]"
    return returnList

@app.route("/RMS/profile/confirm")
def getPassword():

    email = request.args.get('email')
    cur.execute('SELECT Password from User where email = ' + email + ';')
    demail = cur.fetchall()
    return demail[0][0]

@app.route("/RMS/profile/register", methods = ['POST'])
def registerUser():

    first = request.form['firstName']
    last = request.form['lastName']
    email = request.form['email']
    passw = request.form['password']
    cur.execute('INSERT INTO User values (' + '"' + first + '"' + ', ' + '"' + last + '"' + ', ' + '"' + email + '"' + ', ' + '"' + passw + '"' + ')')
    conn.commit()
    return 'Ok'

@app.route("/RMS/profile/semester", methods = ['POST'])
def updateSemesterWithFeedback():

    sname = request.form['semesterName']
    courses = request.form['courses']
    email1 = request.form['email']
    urating = request.form['userRating']


    courses = make_tuple(courses)


    for x in courses:
        if (x[3] == None):
            cur.execute('UPDATE Semester SET CGrade = ' + '"' + x[0] + '"' + ', CComments = ' + '"' + x[1] + '"' + ', Difficulty = ' + x[4] + ', Workload = ' + x[5] + ', Interest = ' + x[6] + ', Overall = ' + x[7]
                + ' WHERE SName = ' + '"' + sname + '"' + ' AND CName = ' + '"' + x[2] + '"' + ' AND email = ' + '"' + email1 + '"')
            conn.commit()
        else:
            cur.execute('UPDATE Semester SET CGrade = ' + '"' + x[0] + '"' + ', CComments = ' + '"' + x[1] + '"' + ', Difficulty = ' + x[4] + ', Workload = ' + x[5] + ', Interest = ' + x[6] + ', Overall = ' + x[7]
                + ' WHERE SName = ' + '"' + sname + '"' + ' AND CName = ' + '"' + x[2] + '"' + ' AND CProfessor = ' + '"' + x[3] + '"' + ' AND email = ' + '"' + email1 + '"')
            conn.commit()

    cur.execute('UPDATE Rating SET URating = ' + urating + ' WHERE SName = ' + '"' + sname + '"' + ' AND email = ' + '"' + email1 + '"')
    conn.commit()

    return 'Ok'

@app.route("/RMS/profile/savesemester", methods = ['POST'])
def insertSemester():

    sname = request.form['semesterName']
    courses = request.form['courses']
    email1 = request.form['email']
    orating = request.form['ourRating']

    cur.execute('INSERT INTO Rating (SName, email, ORating) values (' + '"' + sname + '"' + ', ' + '"' + email1 + '"' + ', ' + orating + ')')
    conn.commit()

    courses = make_tuple(courses)

    for x in courses:
        if (x[1] == None):
            cur.execute('INSERT INTO Semester (SName, CName, email) values (' + '"' + sname + '"' + ', ' + '"' + x[0] + '"' + ', ' + '"' + email1 + '"' + ')')
            conn.commit()
        else:
            cur.execute('INSERT INTO Semester (SName, CName, CProfessor, email) values (' + '"' + sname + '"' + ', ' + '"' + x[0] + '"' + ', ' + '"' + x[1] + '"' + ', ' + '"' + email1 + '"' + ')')
            conn.commit()
    return 'Ok'

@app.route("/RMS/profile/getsemester")
def getSemesterWithFeedback():

    sname = request.args.get('semesterName')
    email = request.args.get('email')
    cur.execute('SELECT CName, CProfessor, CGrade, CComments, Difficulty, Workload, Interest, Overall from Semester where email = ' + '"' + email + '"' + ' AND SName = ' + '"' + sname + '"' + ';')
    data = cur.fetchall()

    cur.execute('SELECT ORating, URating from Rating where email = ' + '"' + email + '"' + ' AND SName = ' + '"' + sname + '"' + ';')
    data2 = cur.fetchall()

    noneString = '' + 'none' + ''
    if (str(data2[0][1]) == "None"):
        returnList = '{"ourrating": ' + str(data2[0][0]) + ', "theirrating": ' + '"' + noneString + '"' + ', "courses": ['
    if (str(data2[0][1]) != "None"):
        returnList = '{"ourrating": ' + str(data2[0][0]) + ', "theirrating": ' + str(data2[0][1]) + ', "courses": ['

    count = 0
    for x in data:
            professor = str(x[1])
            if (professor == "None"):
                professor = noneString
            Grade = str(x[2])
            if (Grade == "None"):
                Grade = noneString
            comments = str(x[3])
            if (comments == "None"):
                comments = noneString
            Difficulty = str(x[4])
            if (Difficulty == "None"):
                Difficulty = noneString
            Workload = str(x[5])
            if (Workload == "None"):
                Workload = noneString
            Interest = str(x[6])
            if (Interest == "None"):
                Interest = noneString
            Overall = str(x[7])
            if (Overall == "None"):
                Overall = noneString
            count += 1
            returnList += '{"name": ' + '"' + str(x[0]) + '", "professor": ' + '"' + professor + '", "theirgrade": ' + '"' + Grade + '", "comments": ' + '"' + comments + '"' + ', "Difficulty": ' + '"' + Difficulty + '"' + ', "Workload": ' + '"' + Workload + '"' + ', "Interest": ' + '"' + Interest + '"' +', "Overall": ' + '"' + Overall + '"' + '}'
            if count != len(data):
                returnList += ", "

    returnList += "] }"
    return returnList

@app.route("/RMS/profile/deletesemester")
def deleteSemester():

    sname = request.args.get('semesterName')
    email = request.args.get('email')

    cur.execute('DELETE FROM Semester where email = ' + '"' + email + '"' + ' AND SName = ' + '"' + sname + '"' + ';')
    conn.commit()

    cur.execute('DELETE FROM Rating where email = ' + '"' + email + '"' + ' AND SName = ' + '"' + sname + '"' + ';')
    conn.commit()
    return 'Ok'

@app.route("/RMS/profile/courseinfo")
def getCourseComments():

    cname = request.args.get('courseName')
    professor = request.args.get('professor')

    returnList = "["

    count = 0
    count2 = 0

    if (professor == None):
        cur.execute('SELECT CComments FROM Semester where CName = ' + '"' + cname + '"' + ';')
        data = cur.fetchall()
        for x in data:
            count += 1
            if (str(x[0]) != "None"):
                returnList += " " + '"' + str(x[0]) + '"'
            if count != len(data) and count != 1:
                returnList += ", "

    if (professor != None):
        cur.execute('SELECT CComments FROM Semester where CName = ' + '"' + cname + '"' + ' AND CProfessor = ' + '"' + professor + '"' + ';')
        data2 = cur.fetchall()
        for y in data2:
            count2 += 1
            if (str(y[0]) != "None"):
                returnList += " " + '"' + str(y[0]) + '"'
            if count2 != len(data2) and count2 != 1:
                returnList += ", "

    returnList += "]"

    return returnList

@app.route("/RMS/courseInfo/GPA")
def getCourseGPA():

    course = request.args.get('course')

    cur.execute('SELECT AverageGPA from CourseGPA where CourseName = ' + '"' + course + '"' + ';')
    data = cur.fetchall()

    finalReturn = "[" + str(data[0][0]) + "]"

    return finalReturn;

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
