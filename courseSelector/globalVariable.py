DEVICE=1
_globalVar={} # 全局变量, 为避免过多及混乱, 全部储存在一个字典里
_globalVar['device']=DEVICE # 本地电脑为1, 服务器为0, 该值不可在函数中修改
_globalVar['cookieWrongTimes']=0
# GetCourseHeader
_globalVar['gch']={
    "Host": "coursesel.umji.sjtu.edu.cn",
    "Connection": "keep-alive",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
    "sec-ch-ua-platform": "\"macOS\"",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://coursesel.umji.sjtu.edu.cn/welcome.action",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    #"Cookie": "_ga=GA1.3.1749969549.1634711853; JSESSIONID=8745FC6AB05D0CB11E5332024E3E04BE" # 这里的 Cookie 已失效
    "Cookie": "_ga=GA1.3.1749969549.1634711853; JSESSIONID="
}
# SelectCourseHeader
_globalVar['sch']={
    "Host": "coursesel.umji.sjtu.edu.cn",
    "Connection": "keep-alive",
    "Content-Length": "252", # 此项需根据实际长度修改
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"96\", \"Google Chrome\";v=\"96\"",
    "X-CSRF-TOKEN": "01bfe76b-74d8-4136-9ec5-bac2e7d991ac",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-platform": "\"macOS\"",
    "Origin": "https://coursesel.umji.sjtu.edu.cn",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://coursesel.umji.sjtu.edu.cn/welcome.action",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    #"Cookie": "_ga=GA1.3.1749969549.1634711853; JSESSIONID=8745FC6AB05D0CB11E5332024E3E04BE" # 这里的 Cookie 已失效
    "Cookie": "_ga=GA1.3.1749969549.1634711853; JSESSIONID="
}
# ElectTurnIdUrl
_globalVar['etiu']='https://coursesel.umji.sjtu.edu.cn/tpm/findStudentElectTurns_ElectTurn.action?_t='
# SelectCourseUrl
_globalVar['scu']="https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action?_t="
# GetCourseUrl
_globalVar['gcu1']="https://coursesel.umji.sjtu.edu.cn/tpm/findLessonTasks_ElectTurn.action?jsonString="
_globalVar['gcu2']='{"isToTheTime":true,"electTurnId":"'
_globalVar['gcu3']='","loadCourseGroup":true,"loadElectTurn":true,"loadCourseType":true,"loadCourseTypeCredit":true,"loadElectTurnResult":true,"loadStudentLessonTask":true,"loadPrerequisiteCourse":true,"lessonCalendarWeek":false,"loadLessonCalendarConflict":false,"loadTermCredit":true,"loadLessonTask":true,"loadDropApprove":true,"loadElectApprove":true}'

# ElectTurnId
_globalVar['eti']=''
_globalVar['mode']=''
_globalVar['electName']=''
_globalVar['startTime']=0
_globalVar['endTime']=0
_globalVar['newMsg']=False
_globalVar['allInfo']={}
_globalVar['failTimes']=0
_globalVar['IntFailTimes']=0
_globalVar['courses']=tuple()

# globalVar 中还有另外一种数据类型:
# key 为 courseId, value 为 [electTurnLessonTaskId,canSelect,description]

def getGlobalValue(key):
    global _globalVar
    return _globalVar[key]


def setGlobalValue(key,v):
    global _globalVar
    _globalVar[key]=v


def getAllGlobalVariables():
    global _globalVar
    return _globalVar

def getGlobalVariableNum():
    global _globalVar
    return len(_globalVar)

def clearGlobalVariable():
    global _globalVar
    _globalVar={}

def deleteGlobalVariable(key):
    global _globalVar
    try:
        _globalVar.pop(key)
    except:
        return -1
    return 0


def getAllKeys():
    global _globalVar
    l=[]
    for k in _globalVar:
        l.append(k)
    return l

def isGlobalVariableExist(key):
    global _globalVar
    return key in _globalVar


def addGlobalVariable(key,num=1):
    global _globalVar
    try:
        _globalVar[key]=_globalVar[key]+num
    except:
        return -1
    return 0

