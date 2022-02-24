# CourseSelector v1.0.1

## 上海交通大学密西根学院自动选课软件

## 使用方式

### 1. 安装

    打开终端/cmd，输入 pip3 install courseSelector  (需要已安装 Python 3)
    如果需要升级, 则使用 pip3 install --upgrade courseSelector

### 2. 使用

    新建一个 .py 文件, import courseSelector
    本程序中有以下函数:
    help(): 输出帮助信息
    check(jsessionid:str): 获取选课信息
    printCourseList(jsessionid:str): 获取所有课程的信息
    waitEmptySpace(jsessionid:str,courses:list,threadNum:int=5): 在 Early Bird 且已选满的情况下，等有人取消时自动选择
    fastSelect(jsessionid:str,courses:list,threadNum:int=10): 在 Early Bird 开始时，发送大量请求快速选课
    luckyDraw(jsessionid:str,courses:list): 在 Lucky Draw 模式下，选择有时间冲突的课程
    courses 参数要求: 数组，里面的每一项为要选课的课程描述（就是printCourseList输出的课程描述）

### 3. 关于 Cookie：
    先在浏览器里登陆好，刷新一下，确定是已登陆状态，在浏览器的设置里复制 Cookie 中 JSESSIONID 这一项，粘贴到程序里

## 关于选课规则

    1. 可以选择有时间冲突的课程，因为时间是否冲突只在本地判断，服务器不会判断，但不建议在一个学期最终提交的版本中有时间冲突的课程。
    2. “同门课已选”的情况，具体会怎么样我也不知道（选课网站上显示很复杂，不同地方查看会有矛盾），强烈不建议选择这样的课，有可能导致原来选的课丢失。
    3. 超过学分上限，在选课过程中可以这样选。但在最终提交或选课结束时，请确保学分符合要求。
    4. 先修课不符，不能选

## 其它说明

    使用要求: Python 3, 必须保证您的设备时间准确
    License: GPL v2
    原理: 抓包分析 Http 请求，然后用 Python 模拟发送 Http 请求
    联系方式: 邮箱:jtc1246@outlook.com, 微信:15021805270, 手机号:15021805270

