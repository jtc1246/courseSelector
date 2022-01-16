from myHttp import *
from functions import *
from globalVariable import globalVar

courseid="77287167-782D-4E8F-8AF5-D071ADB513B0"
getCourseHeader={
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
    "Cookie": "_ga=GA1.3.1749969549.1634711853; JSESSIONID=8745FC6AB05D0CB11E5332024E3E04BE" # 这里的 Cookie 已失效
}


selectCourseHeader={
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
    "Cookie": "_ga=GA1.3.1749969549.1634711853; JSESSIONID=8745FC6AB05D0CB11E5332024E3E04BE" # 这里的 Cookie 已失效
}

getCourseUrl="https://coursesel.umji.sjtu.edu.cn/tpm/findLessonTasks_ElectTurn.action?jsonString=%7B%22isToTheTime%22%3Afalse%2C%22electTurnId%22%3A%22A9E7F742-68FC-4E69-BBE3-E7B599C8FBE9%22%2C%22loadCourseGroup%22%3Atrue%2C%22loadElectTurn%22%3Atrue%2C%22loadCourseType%22%3Atrue%2C%22loadCourseTypeCredit%22%3Atrue%2C%22loadElectTurnResult%22%3Atrue%2C%22loadStudentLessonTask%22%3Atrue%2C%22loadPrerequisiteCourse%22%3Atrue%2C%22lessonCalendarWeek%22%3Afalse%2C%22loadLessonCalendarConflict%22%3Afalse%2C%22loadTermCredit%22%3Atrue%2C%22loadLessonTask%22%3Atrue%2C%22loadDropApprove%22%3Atrue%2C%22loadElectApprove%22%3Atrue%7D"

selectCourseUrl="https://coursesel.umji.sjtu.edu.cn/tpm/doElect_ElectTurn.action?_t="



selectCourseBody="jsonString="
text=getJsonString('A9E7F742-68FC-4E69-BBE3-E7B599C8FBE9',"520E2B92-4A14-4021-99C8-B299E33509DC","EE865A31-79F1-4858-AB78-9F4899284362")
text2=getJsonString2('A9E7F742-68FC-4E69-BBE3-E7B599C8FBE9',"520E2B92-4A14-4021-99C8-B299E33509DC")
selectCourseBody=selectCourseBody+quote(text2,encoding='utf-8')

# t1=getTime()
# resp=http(getCourseUrl,Header=getCourseHeader,Timeout=3000)
# print(resp['status'])
# print(resp['extra'])
# print(getTime()-t1)
# print(getNum(resp['text'],'离散数学'))


# print(resp['status'])
# print(isSuccessful(resp['text'],"CD9C55F0-A726-4B94-BC38-7465F56EDD81"))



selectCourseHeader['Content-Length']=str(len(selectCourseBody))
# selectCourseUrl=selectCourseUrl+str(getTime())
# resp=http(selectCourseUrl,Method='POST',Header=selectCourseHeader,Timeout=3000,BODY=selectCourseBody)
# print(resp['status'])
# print(resp['text'])

allTimes=0
failedTimes=0

while True:
    if(failedTimes>=3):
        print('错误次数过多, 请检查问题')
    allTimes=allTimes+1
    resp=http(getCourseUrl,Header=getCourseHeader,Timeout=3000)
    if(resp['status']!=0):
        failedTimes=failedTimes+1
        print('连接失败 status: '+str(resp['status'])+' code: '+str(resp['code']))
        continue
    if(resp['status']==0):
        failedTimes=0
    num=getNum(resp['text'],'离散数学')
    if(allTimes%5==0):
        print(str(allTimes)+': '+str(num))
    if(num<=119):
        print("发现空位")
        selectCourseUrl=selectCourseUrl+str(getTime())
        resp=http(selectCourseUrl,Method='POST',Header=selectCourseHeader,Timeout=3000,BODY=selectCourseBody)
        if(resp['status']!=0):
            print('选课失败，再次尝试')
            selectCourseUrl=selectCourseUrl+str(getTime())
            resp=http(selectCourseUrl,Method='POST',Header=selectCourseHeader,Timeout=3000,BODY=selectCourseBody)
        loc=str(resp['text']).find('rue')
        if(loc>=0):
            print('返回值校验成功')
        else:
            print('返回值校验失败')
        resp=http(getCourseUrl,Header=getCourseHeader,Timeout=3000)
        if(isSuccessful(resp['text'],courseid)==1):
            print('课程列表校验成功')
            if(loc>=0):
                time.sleep(1000000)
        else:
            print('课程列表校验失败')



