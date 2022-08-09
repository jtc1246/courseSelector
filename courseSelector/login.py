from PIL import Image
from time import sleep
from selenium import webdriver # 版本确定为 3.11.0
from _thread import start_new_thread
import os,stat,shutil,platform,ddddocr,myBasics,pwinput
from phantomjs_packages import phantomjs_mac,phantomjs_windows,phantomjs_linux


_MAX_RETRY=5
_retries=0

_path=os.path.expanduser('~')
_system=''
_plat=platform.platform().lower()
if(_plat.find('windows')>=0):
    _system='windows'
if(_plat.find('macos')>=0):
    _system='macos'
if(_plat.find('linux')>=0):
    _system='linux'
_isWindows=((platform.platform().find('indows'))>=0)
_slash={True:'\\',False:'/'}[_isWindows]
_path=_path+_slash+'.CourseSelector'+_slash
_password=''
_username=''
_driver=None


def forceDelete(fileName:str):
    if(not os.path.exists(fileName)):
        return
    os.chmod(fileName,stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
    if(os.path.isdir(fileName)):
        shutil.rmtree(fileName)
        return
    os.remove(fileName)


def _getPassword():
    global _password
    print('本程序不会将您的密码发送给除 jaccount.sjtu.edu.cn 以外的任何网站或服务器, 也不会以任何形式在本地保存, 请放心输入。')
    try:
        i=pwinput.pwinput('请输入密码: ')
    except:
        print('\nWarning: Jupyter notebook 中输入密码时不能显示星号, 建议您在 终端/cmd 中使用本软件。')
        i=input('请输入密码: ')
    if(len(i)==0):
        i='1'
    _password=i


def _getPassword_retry():
    global _password
    try:
        i=pwinput.pwinput('密码错误, 请重新输入: ')
    except:
        print('\nWarning: Jupyter notebook 中输入密码时不能显示星号, 建议您在 终端/cmd 中使用本软件。')
        i=input('密码错误, 请重新输入: ')
    if(len(i)==0):
        i='1'
    _password=i


def login(username:str):
    global _username,_driver,_retries
    start_new_thread(_getPassword,())
    try:
        forceDelete(_path[:-1])
    except:
        print('本地无法写入数据, 不能使用 jAccount 登录, 请使用 Cookie 登录, 程序已结束运行')
        sleep(0.5)
        os._exit(-1)
    if _system=='macos' :
        browser=phantomjs_mac
    elif _system=='windows' :
        browser=phantomjs_windows
    elif _system=='linux' :
        browser=phantomjs_linux
    else:
        print('暂不支持当前系统, 请使用 Cookie 登录')
    browser=myBasics.base64ToBin(browser)
    try:
        os.mkdir(_path[:-1])
    except:
        print('本地无法写入数据, 不能使用 jAccount 登录, 请使用 Cookie 登录, 程序已结束运行')
        sleep(0.5)
        os._exit(-1)
    f=open(_path+'browser','wb')
    f.write(browser)
    f.close()
    os.chmod(_path+'browser',stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
    url='https://coursesel.umji.sjtu.edu.cn'
    driver = webdriver.PhantomJS(_path+'browser',service_args=['--webdriver-loglevel=NONE'],service_log_path=_path+'.ignore_this')
    # driver=webdriver.Firefox()
    driver.set_window_size(1440,900)
    driver.get(url)
    a=driver.find_element_by_name('user')
    b=driver.find_element_by_name('pass')
    c=driver.find_element_by_name('captcha')
    d=driver.find_element_by_id('captcha-img')
    e=driver.find_element_by_id('submit-button')
    driver.save_screenshot(_path+'whole.png') 
    loc=d.location
    size=d.size
    a.send_keys(username)
    rangle = (int(loc['x']), int(loc['y']), int(loc['x'] + size['width']),
            int(loc['y'] + size['height'])) 
    i = Image.open(_path+"whole.png") 
    ratio=i.size[0]/1440
    i=i.resize((1440,round(i.size[1]/ratio)))
    frame4 = i.crop(rangle)  
    frame4.save(_path+'save.png')
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(_path+'save.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    c.send_keys(res)
    # print(res)
    while(_password==''):
        sleep(0.001)
    b.send_keys(_password)
    e.click()
    cookies=driver.get_cookies()
    newUrl=driver.current_url
    if(newUrl.lower().find('coursesel.umji')<=10 and newUrl.lower().find('coursesel.umji')>=0):
        driver.quit()
        forceDelete(_path[:-1])
        return getJsessionid(cookies)
    _driver=driver
    _username=username
    warn=driver.find_element_by_id('div_warn')
    reason=warn.text
    if(reason.find('用户名和密码')>=0):
        _retries+=1
        return retry_password()
    elif(reason.find('验证码')>=0):
        _retries+=1
        return retry_captcha()
    else:
        driver.quit()
        forceDelete(_path[:-1])
        return ''

    


def getJsessionid(cookies:list):
    for cookie in cookies:
        try:
            dom=cookie['domain'].lower()
            name=cookie['name'].upper()
            value=cookie['value'].upper()
        except:
            continue
        if(dom=='coursesel.umji.sjtu.edu.cn' and name=='JSESSIONID'):
            return value
    return ''



def retry_password():
    global _retries,_driver,_password
    _password=''
    start_new_thread(_getPassword_retry,())
    driver=_driver
    a=driver.find_element_by_name('user')
    b=driver.find_element_by_name('pass')
    c=driver.find_element_by_name('captcha')
    d=driver.find_element_by_id('captcha-img')
    e=driver.find_element_by_id('submit-button')
    driver.save_screenshot(_path+'whole.png') 
    loc=d.location
    size=d.size
    a.send_keys(_username)
    rangle = (int(loc['x']), int(loc['y']), int(loc['x'] + size['width']),
            int(loc['y'] + size['height'])) 
    i = Image.open(_path+"whole.png") 
    ratio=i.size[0]/1440
    i=i.resize((1440,round(i.size[1]/ratio)))
    frame4 = i.crop(rangle)  
    frame4.save(_path+'save.png')
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(_path+'save.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    c.send_keys(res)
    while(_password==''):
        sleep(0.001)
    b.send_keys(_password)
    e.click()
    cookies=driver.get_cookies()
    newUrl=driver.current_url
    if(newUrl.lower().find('coursesel.umji')<=10 and newUrl.lower().find('coursesel.umji')>=0):
        driver.quit()
        forceDelete(_path[:-1])
        return getJsessionid(cookies)
    if(_retries>=_MAX_RETRY):
        driver.quit()
        forceDelete(_path[:-1])
        return ''
    warn=driver.find_element_by_id('div_warn')
    reason=warn.text
    if(reason.find('用户名和密码')>=0):
        _retries+=1
        return retry_password()
    elif(reason.find('验证码')>=0):
        _retries+=1
        return retry_captcha()
    else:
        driver.quit()
        forceDelete(_path[:-1])
        return ''



def retry_captcha():
    global _retries,_driver
    print('验证码错误, 正在重新尝试...')
    driver=_driver
    a=driver.find_element_by_name('user')
    b=driver.find_element_by_name('pass')
    c=driver.find_element_by_name('captcha')
    d=driver.find_element_by_id('captcha-img')
    e=driver.find_element_by_id('submit-button')
    driver.save_screenshot(_path+'whole.png') 
    loc=d.location
    size=d.size
    a.send_keys(_username)
    rangle = (int(loc['x']), int(loc['y']), int(loc['x'] + size['width']),
            int(loc['y'] + size['height'])) 
    i = Image.open(_path+"whole.png") 
    ratio=i.size[0]/1440
    i=i.resize((1440,round(i.size[1]/ratio)))
    frame4 = i.crop(rangle)  
    frame4.save(_path+'save.png')
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(_path+'save.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    c.send_keys(res)
    while(_password==''):
        sleep(0.001)
    b.send_keys(_password)
    sleep(1)
    e.click()
    cookies=driver.get_cookies()
    newUrl=driver.current_url
    if(newUrl.lower().find('coursesel.umji')<=10 and newUrl.lower().find('coursesel.umji')>=0):
        driver.quit()
        forceDelete(_path[:-1])
        return getJsessionid(cookies)
    if(_retries>=_MAX_RETRY):
        driver.quit()
        forceDelete(_path[:-1])
        return ''
    warn=driver.find_element_by_id('div_warn')
    reason=warn.text
    if(reason.find('用户名和密码')>=0):
        _retries+=1
        return retry_password()
    elif(reason.find('验证码')>=0):
        _retries+=1
        return retry_captcha()
    else:
        driver.quit()
        forceDelete(_path[:-1])
        return ''


