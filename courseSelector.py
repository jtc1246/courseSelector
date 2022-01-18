from myHttp import *
from functions import *
from globalVariable import *
import _thread as thread


def help():
    # 具体内容还没写
    print('输出帮助信息')



def setCookie(jsessionid):
    functions_setCookie(jsessionid)



def check(jsessionid:str):
    setCookie(jsessionid)
    getElectTurnId()
    print('当前选课名称为: '+getGlobalValue('electName'))
    print('当前规则为: '+getGlobalValue('mode'))
    print('开始时间为: '+str(getGlobalValue('startTime')))
    print('结束时间为: '+str(getGlobalValue('endTime')))
    print('当前时间为: '+str(getTime()))


def printCourseList(jsessionid:str):
    check(jsessionid)
    getElectTurnId()
    all=getAllInformationFirst()
    all=all['data']["lessonTasks"]
    f=open('./courses.txt','w')
    f.write('课程名称      |      上课教师        |        课程描述\n')
    for one in all:
        print(one["courseId"])
        f.write(one["courseName"])
        f.write(' | ')
        try:
            f.write(one["lessonTaskTeam"])
        except:
            f.write('None')
        f.write(' | ')
        f.write(one["lessonClassName"])
        f.write('\n')
    f.close()
    print('获取课程列表成功, 请打开当前文件夹中的 course.txt 查看')
    
def waitEmptySpace(jsessionid:str,courses:list):
    # 初始化部分
    check(jsessionid)
    all=deepcopy(getAllInformationFirst())
    all=all['data']["lessonTasks"]
    cids=[]
    isExit=False
    isFound=False
    for c in courses:
        isFound=False
        for one in all:
            if(one["lessonClassName"].find(c)>=0):
                cids.append(one['courseId'])
                setGlobalValue(one['courseId'],[one['electTurnLessonTaskId'],False,c])
                isFound=True
                break
        if(not isFound):
            isExit=True
            print('未找到该课程: '+c)
    if(isExit):
        print('存在未找到的课程, 程序已结束运行')
    cids=tuple(cids)
    setGlobalValue('courses',cids)
    # 初始化结束
    thread.start_new_thread(testInternetConnection,())
    thread.start_new_thread(keepCookie,())
    currentTime=getTime()
    if(currentTime<getGlobalValue('startTime')-10000):
        time.sleep(0.001*(-currentTime+getGlobalValue('startTime')-10000))
    for i in range(0,5):
        thread.start_new_thread(getAllInformation,())
        time.sleep(0.3)
    thread.start_new_thread(mainControl,())
    for i in cids:
        thread.start_new_thread(selectOneCourse,(i,))
    while True:
        time.sleep(1)
        if(getTime()>getGlobalValue('endTime')+10000):
            print('选课已经结束, 程序结束运行')
            os._exit(0)




def fastSelect(jsessionid:str,courses:list):
    pass


# 在 Lucky Draw 模式下选时间冲突的课程
def luckyDraw():
    pass