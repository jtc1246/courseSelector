from .globalVariable import *
import time,json
from copy import deepcopy
from .myHttp import *
import os
from time import sleep
from random import randint

# 格式:
# {"electTurnId":"158C59EB-C733-4C3A-8E78-C314DCEC70BF","autoElect":true,"lessonTasks":["A57528CC-AECA-4266-874E-039386315A2A"]}
def getJsonString(electTurnId,electTurnLessonTaskId):
    return '{"electTurnId":"'+electTurnId+'","autoElect":true,"lessonTasks":["'+electTurnLessonTaskId+'"]}'


def getJsonStringLucky(electTurnId,electTurnLessonTaskId,lessonTaskId):
    return "{\"electTurnId\":\""+electTurnId+"\",\"lessonTasks\":[{\"electTurnLessonTaskId\":\""+electTurnLessonTaskId+"\",\"lessonTaskId\":\""+lessonTaskId+"\"}]}"



def getElectTurnId():
    url=getGlobalValue('etiu')+str(getTime())
    header=getGlobalValue('gch')
    r=http(url,Header=header,Timeout=1500)
    while(r['status']==-2):
        print('连接服务器失败, 正在重新尝试...')
        r=http(url,Header=header,Timeout=1500)
    if(r['status']==-1):
        print('无网络连接, 程序已结束运行')
        sleep(0.5)
        os._exit(-1)
    if(r['status']==-2):
        print('连接服务器超时, 程序已结束运行')
        sleep(0.5)
        os._exit(-1)
    if(r['code']==302):
        print("Cookie 无效, 程序已结束运行")
        sleep(0.5)
        os._exit(-1)
    if(len(r['text'])==0):
        print('无正在进行的选课，程序结束运行')
        sleep(0.5)
        os._exit(0)
    eti=r['text'][0]["electTurnId"]
    mode=r['text'][0]["electModeName"]
    name=r['text'][0]["electTurnName"]
    setGlobalValue('eti',eti)
    setGlobalValue('mode',mode)
    setGlobalValue('electName',name)
    startTime=toUnix(r['text'][0]["beginTime"])
    endTime=toUnix(r['text'][0]["endTime"])
    setGlobalValue('startTime',startTime)
    setGlobalValue('endTime',endTime)




def setCookie(jsessionid):
    gch=getGlobalValue('gch')
    sch=getGlobalValue('sch')
    gch=deepcopy(gch)
    sch=deepcopy(sch)
    gch['Cookie']=gch['Cookie']+jsessionid
    sch['Cookie']=sch['Cookie']+jsessionid
    setGlobalValue('gch',gch)
    setGlobalValue('sch',sch)


def getAllInformationFirst(): # 第一次获取信息时调用这个函数, 出现异常直接结束运行
    gcu1=getGlobalValue('gcu1')
    gcu2=getGlobalValue('gcu2')
    if(getTime()>=getGlobalValue('startTime')):
        gcu2=getGlobalValue('gcu22')
    gcu3=getGlobalValue('gcu3')
    eti=getGlobalValue('eti')
    url=quote(gcu2+eti+gcu3,encoding='utf-8')
    url=gcu1+url
    header=getGlobalValue('gch')
    r=http(url,Header=header,Timeout=3000)
    while(r['status']==-2):
        print('连接服务器失败, 正在重新尝试...')
        r=http(url,Header=header,Timeout=3000)
    if(r['status']==-1):
        print('无网络连接, 程序已结束运行')
        sleep(0.5)
        os._exit(-1)
    if(r['status']==-2):
        print('连接服务器超时, 程序已结束运行')
        sleep(0.5)
        os._exit(-1)
    if(r['code']==302):
        print("Cookie 失效, 请重新设置 Cookie, 程序已结束运行")
        sleep(0.5)
        os._exit(-1)
    setGlobalValue('allInfo',r['text'])
    setGlobalValue('newMsg',True)
    return r['text']


def getAllInformation(): # 后续循环时调用这个函数, 出现异常直接忽略
    # 这里先不设置循环, 后面将这个函数包在另一个函数里, 在那里设置循环
    sleep(0.5)
    gcu1=getGlobalValue('gcu1')
    gcu2=getGlobalValue('gcu2')
    if(getTime()>=getGlobalValue('startTime')):
        gcu2=getGlobalValue('gcu22')
    gcu3=getGlobalValue('gcu3')
    eti=getGlobalValue('eti')
    url=quote(gcu2+eti+gcu3,encoding='utf-8')
    url=gcu1+url
    header=getGlobalValue('gch')
    r=http(url,Header=header,Timeout=10000)
    # print(r)
    if(r['code']==302):
        print(str(getTime())+": Cookie 失效, 请重新设置 Cookie, 程序已结束运行")
        sleep(0.5)
        os._exit(-1)
    if(r['status']!=0 and r['status']!=3):
        return -1
    try:
        re=r['text']['data']["electTurnResult"]
        re=r['text']['data']["lessonTasks"]
    except:
        t=str(getTime())
        print(t+': 选课网站连接成功，但返回了错误信息')
        try:
            f=open('./错误记录.txt','a+')
            f.write("\n\n\n\n"+t+"")
            f.write(json.dumps(r['text'],ensure_ascii=False))
            f.close()
        except:
            try:
                print(json.dumps(r['text'],ensure_ascii=False))
            except:
                print(r['extra'])
        return -1
    return r['text']


def getSelectedCourses(AllInformation):
    # f=open('./testt.txt','w')
    # f.write(json.dumps(AllInformation))
    # f.close()
    all=AllInformation['data']["electTurnResult"]
    electTurnId=getGlobalValue('eti')
    l=[]
    for one in all:
        if(electTurnId==one["electTurnId"] and str(one["electStatus"]) in ['4','0']):
            l.append(one["lessonTaskId"])
    # print(l)
    return l

def selectOneCourse(lessonTaskId):
    while True:
        status=getGlobalValue(lessonTaskId)
        if(not status[1]):
            time.sleep(0.01)
            continue
        # 以下是要选的情况
        electTurnLessonTaskId=status[0]
        eti=getGlobalValue('eti')
        jss=getJsonString(eti,electTurnLessonTaskId)
        header=getGlobalValue('sch')
        header=deepcopy(header)
        body="jsonString="+quote(jss,encoding='utf-8')
        header['Content-Length']=str(len(body))
        url=getGlobalValue('scu')+str(getTime())
        print('正在发送选课指令')
        r=http(url,Method='POST',Header=header,Timeout=2000,BODY=body)
        print(r)



def selectOneCourseLucky(lessonTaskId):
    status=getGlobalValue(lessonTaskId)
    # 以下是要选的情况
    electTurnLessonTaskId=status[0]
    lessonTaskId=status[3]
    eti=getGlobalValue('eti')
    jss=getJsonStringLucky(eti,electTurnLessonTaskId,lessonTaskId)
    header=getGlobalValue('sch')
    header=deepcopy(header)
    body="jsonString="+quote(jss,encoding='utf-8')
    header['Content-Length']=str(len(body))
    url=getGlobalValue('scul')+str(getTime())
    r=http(url,Method='POST',Header=header,Timeout=1000,BODY=body)
    # print(r)


def testInternetConnection():
    setGlobalValue('IntFailTimes',0)
    while True:
        re=testInternet()
        if(re==-1):
            addGlobalVariable('IntFailTimes')
        if(re==0):
            setGlobalValue('IntFailTimes',0)
        if(getGlobalValue('IntFailTimes')%10==3):
            print(str(getTime())+': 无法连接到互联网, 请检查网络连接')
        time.sleep(0.5)


def keepCookie():
    header=getGlobalValue('gch')
    url='https://coursesel.umji.sjtu.edu.cn/welcome.action'
    while True:
        r=http(url,Header=header,ToJSON=False)
        if(r['code']==302):
            print(str(getTime())+": Cookie 失效, 请重新设置 Cookie, 程序已结束运行")
            sleep(0.5)
            os._exit(-1)
        time.sleep(30)


def isSelected(lessonTaskId):
    allInfo=getGlobalValue('allInfo')
    selectedCourses=getSelectedCourses(allInfo)
    # print(selectedCourses)
    return lessonTaskId in selectedCourses


def hasSpace(lessonTaskId):
    allInfo=deepcopy(getGlobalValue('allInfo'))
    allInfo=allInfo['data']["lessonTasks"]
    for one in allInfo:
        if(one["lessonTaskId"]==lessonTaskId):
            maxNum=int(one["maxNum"])
            stuNum=int(one["studentNum"])
            return stuNum<maxNum
    return False

def getInfoMain():
    while True:
        if(getGlobalValue('failTimes')%20==19):
            print(str(getTime())+': 选课网站连接错误次数过多, 请检查原因, 如果当前是选课高峰期, 可忽略此问题')
        t=getAllInformation()
        if(t==-1):
            addGlobalVariable('failTimes')
            continue
        setGlobalValue('allInfo',t)
        setGlobalValue('newMsg',True)
        setGlobalValue('failTimes',0)
        sleep(randint(5,8)/100)




def mainControl():
    while True:
        if(not getGlobalValue('newMsg')):
            time.sleep(0.01)
            continue
        courses=getGlobalValue('courses') # courses 是 lessonTaskId 的数组 
        setGlobalValue('newMsg',False)
        for ltid in courses:
            if(getGlobalValue(ltid)[1]):
                # canSelect=True, 人数满、已选成功 满足任意一个即停止
                if(isSelected(ltid)):
                    info=getGlobalValue(ltid)
                    info=deepcopy(info)
                    print(str(getTime())+': '+info[2]+' 选课成功')
                    info[1]=False
                    setGlobalValue(ltid,info)
                    continue
                if((not hasSpace(ltid)) and getGlobalValue('force-selecting')==False):
                    info=getGlobalValue(ltid)
                    info=deepcopy(info)
                    print(str(getTime())+': '+info[2]+' 选课失败')
                    info[1]=False
                    setGlobalValue(ltid,info)
                    continue
            if(not getGlobalValue(ltid)[1]):
                # canSelect=False, 未选择、有空位 两者同时满足才开始
                if( (not isSelected(ltid)) and hasSpace(ltid)):
                    info=getGlobalValue(ltid)
                    info=deepcopy(info)
                    print(str(getTime())+': '+info[2]+' 发现空位')
                    info[1]=True
                    setGlobalValue(ltid,info)
                    continue

