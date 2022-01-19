from .myHttp import *
from .functions import *
from .globalVariable import *
import _thread as thread


def help():
    # 具体内容还没写
    print('欢迎使用本软件')






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
    
def waitEmptySpace(jsessionid:str,courses:list,threadNum:int=5):
    # 初始化部分
    if(threadNum<=0):
        print('线程数必须大于 0')
        os._exit(-1)
    check(jsessionid)
    if(getGlobalValue('mode').find('arly')==-1):
        print('本轮选课不是 Early Bird, 不适用本软件')
        os._exit(-1)
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
    for i in range(0,threadNum):
        thread.start_new_thread(getAllInformation,())
        time.sleep(1.4/threadNum)
    thread.start_new_thread(mainControl,())
    for i in cids:
        thread.start_new_thread(selectOneCourse,(i,))
    while True:
        time.sleep(10)
        isAllSelected=True
        for i in cids:
            if(not isSelected(i)):
                isAllSelected=False
        if(isAllSelected):
            print('要选课课程已经全部选择成功, 程序结束运行')
            os._exit(0)
        if(getTime()>getGlobalValue('endTime')+10000):
            print('选课已经结束, 程序结束运行')
            os._exit(0)




def fastSelect(jsessionid:str,courses:list,threadNum:int=10):
    # 初始化部分
    if(threadNum<=0):
        print('线程数必须大于 0')
        os._exit(-1)
    check(jsessionid)
    if(getGlobalValue('mode').find('arly')==-1):
        print('本轮选课不是 Early Bird, 不适用本软件')
        os._exit(-1)
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
                setGlobalValue(one['courseId'],[one['electTurnLessonTaskId'],True,c])
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
    for i in range(0,3):
        thread.start_new_thread(getAllInformation,())
    thread.start_new_thread(mainControl,())
    for i in cids:
        for j in range(0,threadNum):
            thread.start_new_thread(selectOneCourse,(i,))
    while True:
        time.sleep(10)
        isAllSelected=True
        for i in cids:
            if(not isSelected(i)):
                isAllSelected=False
        if(isAllSelected):
            print('要选课课程已经全部选择成功, 程序结束运行')
            os._exit(0)
        if(getTime()>getGlobalValue('endTime')+10000):
            print('选课已经结束, 程序结束运行')
            os._exit(0)


# 在 Lucky Draw 模式下选时间冲突的课程
def luckyDraw(jsessionid:str,courses:list):
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
                setGlobalValue(one['courseId'],[one['electTurnLessonTaskId'],True,c,one['lessonTaskId']])
                isFound=True
                break
        if(not isFound):
            isExit=True
            print('未找到该课程: '+c)
    if(isExit):
        print('存在未找到的课程, 程序已结束运行')
    cids=tuple(cids)
    setGlobalValue('courses',cids)
    for i in cids:
        thread.start_new_thread(selectOneCourseLucky,(i,))
    time.sleep(10)
    dic={True:'选课成功',False:'选课失败'}
    getAllInformationFirst()
    for i in cids:
        print(getGlobalValue(i)[2]+': '+dic[isSelected(i)])
    os._exit(0)





