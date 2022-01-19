# 上海交通大学密西根学院自动选课软件

## 此版本只支持监视是否有空位，在有空位时自动选择。暂不支持在开始时快速选课，以后可能会支持该模式。

### 关于 Cookie：

    先在浏览器里登陆好，刷新一下，确定是已登陆状态，在浏览器的设置里复制 Cookie，粘贴到程序里

### 关于 courseId, electTurnLessonTaskId, lessonTaskId, electTurnId 等：

    用 getCourseUrl 那个链接把数据下载下来，转成 Json 格式，在那里面就可以看到了

### 原理：
    抓包分析 Http 请求，然后用 Python 模拟发送 Http 请求

### 使用要求：
    Python 3，且安装了 urllib3

### 其它说明：
    此版本未经过充分测试，请谨慎使用
    GPL v2 开源协议

### 联系方式：
    微信：15021805270，
    邮箱：jtc1246@outlook.com
