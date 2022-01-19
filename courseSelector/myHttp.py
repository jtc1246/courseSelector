from .globalVariable import *
import urllib3 as _myHttp_urllib3
import urllib3.exceptions as _myHttp_urllib3_exceptions
import time,json
from urllib.parse import quote
def testInternet():
    http1=_myHttp_urllib3.PoolManager()
    try:
        r=http1.request("GET","https://www.baidu.com",timeout=1.5,retries=False)
    except:
        return -1
    return 0

def http(url:str,Method:str="GET",Header:dict={},Timeout:int=0,ToJSON:bool=True,BODY:str="",Decode:bool=True):
    # status:  -1: 无网络  -2: 超时  -3: 域名不存在  -4: 其它问题, 主要是代理服务器设置错误(服务器上无此问题)
    # status:  1: 不是 UTF-8 编码, text 返回空字符串  2: 不是json格式(在toJSON=True的前提下)
    # status:  3: 对方网站不支持https, 但是却使用了https连接, 这种情况会自动切换为http连接, 若此次status不为0, 返回该status, 若为0, 返回3
    backup=[url,Method,Header,Timeout,ToJSON,BODY,Decode]
    http1=_myHttp_urllib3.PoolManager()
    global globalVar
    if(Timeout==0):
        Timeout=500+500*getGlobalValue('device')
    r=0
    if(ToJSON):
        text={}
    else:
        text=""
    try:
        r=http1.request(Method,url,headers=Header,timeout=Timeout/1000,body=BODY,retries=False)
    except _myHttp_urllib3_exceptions.NewConnectionError as err: # 无网络/域名不存在
        if(testInternet()==-1): # 无网络
            return {'status':-1,'code':0,'text':text,'header':{},'extra':''}
        return {'status':-3,'code':0,'text':text,'header':{},'extra':''}
    except _myHttp_urllib3_exceptions.ConnectTimeoutError as err: # 无网络/超时
        if(testInternet()==-1): # 无网络
            return {'status':-1,'code':0,'text':text,'header':{},'extra':''}
        # 超时
        try:
            r=http1.request(Method,url,headers=Header,timeout=3*Timeout/1000,body=BODY,retries=False)
        except:
            return {'status':-2,'code':0,'text':text,'header':{},'extra':''}
    except _myHttp_urllib3_exceptions.ReadTimeoutError as err: # 无网络/超时
        if(testInternet()==-1): # 无网络
            return {'status':-1,'code':0,'text':text,'header':{},'extra':''}
        # 超时
        try:
            r=http1.request(Method,url,headers=Header,timeout=3*Timeout/1000,body=BODY,retries=False)
        except:
            return {'status':-2,'code':0,'text':text,'header':{},'extra':''}
    except _myHttp_urllib3_exceptions.SSLError: # 对方网站不支持https, 但是却使用了https连接
        n=backup[0].find('https://')
        newUrl='http://'+backup[0][n+8:]
        tryAgain=http(newUrl,Method=backup[1],Header=backup[2],Timeout=backup[3],ToJSON=backup[4],BODY=backup[5],Decode=backup[6])
        if(tryAgain['status']==0):
            tryAgain['status']=3
        return tryAgain
    except Exception as err: # 其它错误，主要为代理服务器设置错误，服务器上一般无此问题
        return {'status':-4,'code':0,'text':text,'header':{},'extra':''}
    # 以下是正常情况
    resp={}
    resp['status']=0
    resp['code']=r.status
    respHeader=dict(r.headers)
    resp['header']=respHeader
    resp['extra']=''
    text=r.data
    if(not Decode):
        resp['text']=text
        return resp
    deco=''
    try:
        deco=text.decode('utf-8')
    except:
        resp['text']=''
        resp['status']=1
        resp['extra']=text
        return resp
    if(not ToJSON):
        resp['text']=deco
        return resp
    js={}
    try:
        js=toJson(deco)
    except:
        resp['text']={}
        resp['status']=2
        resp['extra']=deco
        return resp
    resp['text']=js
    return resp

def getTime():
    global globalVar
    t = time.time()
    t = int(1000 * t)
    return t


def toJson(Text):
    text=Text
    i=0
    while text[0]==' ' or text[0]=='\n':
        text=text[1:]
    if text[0]=='[':
        text='{"1":'+text+'}'
        i=1
    text=json.loads(text,strict=False)
    if i==1:
        text=text['1']
    return text


# 格式示例: "2022-01-17 10:00"
def toUnix(timeStr):
    timeStr=timeStr+':00'
    b=time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')
    c=time.mktime(b)
    return int(c*1000)


