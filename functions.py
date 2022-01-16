from globalVariable import globalVar
import time

def getJsonString(electTurnId,electTurnLessonTaskId,lessonTaskId):
    return "{\"electTurnId\":\""+electTurnId+"\",\"lessonTasks\":[{\"electTurnLessonTaskId\":\""+electTurnLessonTaskId+"\",\"lessonTaskId\":\""+lessonTaskId+"\"}]}"


# {"electTurnId":"158C59EB-C733-4C3A-8E78-C314DCEC70BF","autoElect":true,"lessonTasks":["A57528CC-AECA-4266-874E-039386315A2A"]}
# 在 Early Bird 中格式为 getJsonString2 的结果
def getJsonString2(electTurnId,electTurnLessonTaskId):
    return '{"electTurnId":"'+electTurnId+'","autoElect":true,"lessonTasks":["'+electTurnLessonTaskId+'"]}'



def isSuccessful(courseList,courseId):
    try:
        a=courseList['data']["electTurnResult"]
    except:
        return 0
    for cour in a:
        if(cour['courseId']==courseId):
            return 1
    return 0

# "studiedStudentNum": 97, "studentNum": 154, "electedStudentNum": 57,
# 在 Early Bird 中以 studentNum 为准
def getNum(courseList,name):
    global globalVar
    try:
        a=courseList['data']["lessonTasks"]
    except:
        print('Cookie 错误')
        globalVar['cookieWrongTimes']=globalVar['cookieWrongTimes']+1
        if(globalVar['cookieWrongTimes']==3):
            print('Cookie 错误次数过多, 请重新登陆并切换 Cookie')
            time.sleep(1000000)
        return 100
    globalVar['cookieWrongTimes']=0
    for cour in a:
        if(cour["courseName"].find(name)>=0):
            return int(cour['studentNum'])

