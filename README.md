# xicidaili.com
# python3 爬虫 xicidaili.com 实战

[原文出自本人CSDN](http://blog.csdn.net/hunter_wyh/article/details/78410637)

## 第一步 分析网站

打开链接 http://www.xicidaili.com/nn/1
这就是我们今天要爬虫的网站
目的是把从nn/1到nn/最大页数的数据给趴下来，保存为excel

源代码分析后，我们可以得到类似html_doc


## 第二步 导包

```python
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup
```
首先这是Python3 标准，所以导入的是urllib.request
os用来获取本地文件
openpyxl，如果没有的话'pip install openpyxl',excel插件
这里用BeautifulSoup解析HTML，本来考虑过使用正则表达式不过发现这个可能更容易实现

## 第三步 访问测试

我们先访问http://www.xicidaili.com/nn/1，看看能不能get到HTML
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_html(url):
    html = request.urlopen(url).read().decode('utf-8')
    print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)
```

失败。控制台输出：
```python
Traceback (most recent call last):
  ...
urllib.error.HTTPError: HTTP Error 503: Service Temporarily Unavailable
```
请看下一步解决方法。

## 第四步 伪装好人之模拟浏览器访问

上面报错503 服务器猜测访问者是坏人，所以拒绝了。那我们加个header，这是模拟浏览器访问该页面的作用。让自己像个好人。
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    response = request.Request(url=url, headers=headers)
    html = request.urlopen(response).read().decode('utf-8')
    print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)

```
控制台输出了HTML文件。成功！自此，我们可以与网站通信了。

## 第五步 完善之出错重传

访问网站的时候，如果网络不好，那就访问不到对不对。这可以通过返回的状态码判断。我们这里处理500+状态码。让他可以再次尝试访问。这里我们参考《用Python写网络爬虫》原文的方法：
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        response = request.Request(url=url, headers=headers)
        html = request.urlopen(response).read().decode('utf-8')
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)
    print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)
```

## 第六步 解析页面数据

为了防止网络问题和服务器问题给我们带来不便，我们这里暂时使用本地的HTML文本来模拟该解析过程，我也建议大家和我一样。别慌，最后我们再使用http请求。这里使用的本地html文本即上文提到的html_doc，请复制并且把换行去掉，放入代码中。
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

# 请填入html_doc
html_doc = 

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        # response = request.Request(url=url, headers=headers)
        # html = request.urlopen(response).read().decode('utf-8')
        html = html_doc
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)
    print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)
```
测试过，没问题。那我们开始解析。
```
soup = BeautifulSoup(html, 'html.parser')
```
我们的数据在Table的每个<tr>中，所以我们：
首先要获取到所有的tr节点(对应代码trs):
```
trs = soup.find_all('tr')
```
输出trs形如：[<tr>...</tr><tr>...</tr>...]
然后我们迭代每一个tr节点(对应代码中trs[i])，且每一个tr有多个td(对应代码中tds)。（据分析，该hmlt每个td内td数量为10）。接着我们数据各td节点内容。
```python
for i in range(1,len(trs)):
	tds = trs[i].find_all("td")
	if len(tds)==10:
		print("国家:" + tds[0].img["alt"])
		print("IP地址:" + tds[1].get_text())
		print("端口:" + tds[2].get_text())
		print("服务器地址:" + tds[3].get_text())
		print("是否匿名:" + tds[4].get_text())
		print("类型:" + tds[5].get_text())
		print("速度:" + tds[6].div["title"])
		print("连接时间:" + tds[7].div["title"])
		print("存活时间:" + tds[8].get_text())
		print("验证时间:" + tds[9].get_text())
```
具体代码如下：
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

html_doc = 

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        # response = request.Request(url=url, headers=headers)
        # html = request.urlopen(response).read().decode('utf-8')
        html = html_doc
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            if len(tds) == 10:
                print("国家:" + tds[0].img["alt"])
                print("IP地址:" + tds[1].get_text())
                print("端口:" + tds[2].get_text())
                print("服务器地址:" + tds[3].get_text())
                print("是否匿名:" + tds[4].get_text())
                print("类型:" + tds[5].get_text())
                print("速度:" + tds[6].div["title"])
                print("连接时间:" + tds[7].div["title"])
                print("存活时间:" + tds[8].get_text())
                print("验证时间:" + tds[9].get_text())
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)
    # print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)
```
控制台输出：
```python
国家:Cn
IP地址:27.40.140.40
端口:61234
服务器地址: 广东湛江 
是否匿名:高匿
类型:HTTP
速度:0.248秒
连接时间:0.049秒
存活时间:1分钟
验证时间:17-10-31 09:01
国家:Cn
IP地址:222.184.177.6
端口:23735
服务器地址: 江苏南通 
是否匿名:高匿
类型:HTTPS
速度:0.248秒
连接时间:0.049秒
存活时间:16分钟
验证时间:17-10-31 09:00

进程已结束,退出代码0
```
然后我们测试一下可不可以使用http请求：
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        response = request.Request(url=url, headers=headers)
        html = request.urlopen(response).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        for i in range(1, len(trs)):
            tds = trs[i].find_all("td")
            if len(tds) == 10:
                print("---")
                print("国家:" + tds[0].img["alt"])
                print("IP地址:" + tds[1].get_text())
                print("端口:" + tds[2].get_text())
                print("服务器地址:" + tds[3].get_text())
                print("是否匿名:" + tds[4].get_text())
                print("类型:" + tds[5].get_text())
                print("速度:" + tds[6].div["title"])
                print("连接时间:" + tds[7].div["title"])
                print("存活时间:" + tds[8].get_text())
                print("验证时间:" + tds[9].get_text())
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)
    # print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)
```
发现控制台报错：
```python
Traceback (most recent call last):
  File "E:/pythonworkplace/com/xicidaili.com/teach.py", line 43, in <module>
    get_html(url)
  File "E:/pythonworkplace/com/xicidaili.com/teach.py", line 22, in get_html
    print("国家:" + tds[0].img["alt"])
TypeError: 'NoneType' object is not subscriptable
```
分析HTML代码
```xml
<tr class="odd">
      <td class="country"></td>
      <td>120.78.73.169</td>
      <td>808</td>
      ...
```
原来第一个td[0]节点没有子节点img。然后我仔细看了看，原来不只这个数据，其他数据也有缺胳膊少腿的。像我这样追求完美的人，这些数据我就去噪了呀。(哈哈，如果你要的话就加一个判断，if else。)
```python
for i in range(1, len(trs)):
	try:
		tds = trs[i].find_all("td")
		if len(tds) == 10:
			print("---")
			print("国家:" + tds[0].img["alt"])
			print("IP地址:" + tds[1].get_text())
			print("端口:" + tds[2].get_text())
			print("服务器地址:" + tds[3].get_text())
			print("是否匿名:" + tds[4].get_text())
			print("类型:" + tds[5].get_text())
			print("速度:" + tds[6].div["title"])
			print("连接时间:" + tds[7].div["title"])
			print("存活时间:" + tds[8].get_text())
			print("验证时间:" + tds[9].get_text())
	except TypeError as e:
		print('get_html_td TypeError:' + e.__str__())
		continue
```
你是可以这样子的：
```python
try:
	tds = trs[i].find_all("td")
	if len(tds) == 10:
		print("---")
		if tds[0].img:print("国家:" + tds[0].img["alt"])
		else:print("国家:")
		print("IP地址:" + tds[1].get_text())
		print("端口:" + tds[2].get_text())
		print("服务器地址:" + tds[3].get_text())
		print("是否匿名:" + tds[4].get_text())
		print("类型:" + tds[5].get_text())
		if tds[6].div:print("速度:" + tds[6].div["title"])
		else:print("速度:")
		if tds[7].div:print("连接时间:" + tds[7].div["title"])
		else:print("连接时间:")
		print("存活时间:" + tds[8].get_text())
		print("验证时间:" + tds[9].get_text())
except TypeError as e:
	print('get_html_td TypeError:' + e.__str__())
	continue
```
当然，我又发现，有些值输出例如
```
服务器地址:     江苏南通 
```
发现了没？服务器地址有空格！追求完美，容不得一丝马虎，必须去掉空格。
python去掉字符串中空格的方法：

1. strip()：把头和尾的空格去掉
2. lstrip()：把左边的空格去掉
3. rstrip()：把右边的空格去掉
4. replace('c1','c2')：把字符串里的c1替换成c2。故可以用replace(' ','')来去掉字符串里的所有空格
5. split()：通过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串
6. 使用正则表达式


最后版本：
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        response = request.Request(url=url, headers=headers)
        html = request.urlopen(response).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                if len(tds) == 10:
                    print("---")
                    if tds[0].img:print("国家:" + tds[0].img["alt"])
                    else:print("国家:")
                    print("IP地址:" + tds[1].get_text())
                    print("端口:" + tds[2].get_text())
                    print("服务器地址:" + tds[3].get_text().strip())
                    print("是否匿名:" + tds[4].get_text())
                    print("类型:" + tds[5].get_text())
                    if tds[6].div:print("速度:" + tds[6].div["title"])
                    else:print("速度:")
                    if tds[7].div:print("连接时间:" + tds[7].div["title"])
                    else:print("连接时间:")
                    print("存活时间:" + tds[8].get_text())
                    print("验证时间:" + tds[9].get_text())
            except TypeError as e:
                print('get_html_td TypeError:' + e.__str__())
                continue
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)
    # print(html)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)
```
控制台结果：正常输出，把该页面所有我们需要的数据都数出来了，完美！

## 第七步 数据保存为excel

pyhon 操作excel 有很多工具，这里我们使用的是openpyxl，所以请确保您已经安装了excel。

来，看代码
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

# html_doc = "<html><head><title></title></head><body><table><tr><th>国家</th><th>IP地址</th><th>端口</th><th>服务器地址</th><th>是否匿名</th><th>类型</th><th>速度</th><th>连接时间</th><th>存活时间</th><th>验证时间</th></tr><tr><td><img src='http://fs.xicidaili.com/images/flag/cn.png' alt='Cn' /></td><td>27.40.140.40</td><td>61234</td><td><a>广东湛江</a></td><td>高匿</td><td>HTTP</td><td class='country'><div title='0.248秒' class='bar'><div class='bar_inner fast' style='width:92%'></div></div></td><td class='country'><div title='0.049秒' class='bar'><div class='bar_inner fast' style='width:99%'></div></div></td><td>1分钟</td><td>17-10-31 09:01</td></tr><tr><td><img src='http://fs.xicidaili.com/images/flag/cn.png' alt='Cn' /></td><td>222.184.177.6</td><td>23735</td><td><a>江苏南通</a></td><td>高匿</td><td>HTTPS</td><td class='country'><div title='0.248秒' class='bar'><div class='bar_inner fast' style='width:92%'></div></div></td><td class='country'><div title='0.049秒' class='bar'><div class='bar_inner fast' style='width:99%'></div></div></td><td>16分钟</td><td>17-10-31 09:00</td></tr>		<tr class='odd'><td class='country'></td><td>120.78.73.169</td><td>808</td><td>长城宽带</td><td class='country'>高匿</td><td>HTTPS</td><td class='country'><div title='0.16秒' class='bar'><div class='bar_inner fast' style='width:88%'></div></div></td><td class='country'><div title='0.032秒' class='bar'><div class='bar_inner fast' style='width:95%'></div></div></td><td>4天</td><td>17-10-31 11:11</td></tr>		<tr><td><img src='http://fs.xicidaili.com/images/flag/cn.png' alt='Cn' /></td><td>222.184.177.6</td><td>23735</td><td><a>江苏大大</a></td><td>高匿</td><td>HTTPS</td><td class='country'><div title='0.248秒' class='bar'><div class='bar_inner fast' style='width:92%'></div></div></td><td class='country'><div title='0.049秒' class='bar'><div class='bar_inner fast' style='width:99%'></div></div></td><td>16分钟</td><td>17-10-31 09:00</td></tr></table></body></html>"

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        response = request.Request(url=url, headers=headers)
        html = request.urlopen(response).read().decode('utf-8')
        # html = html_doc
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        items = []
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                tds0,tds6,tds7 = '','',''
                if len(tds) == 10:
                    if tds[0].img: tds0 = tds[0].img["alt"]
                    if tds[6].div:tds6 = tds[6].div["title"]
                    if tds[7].div:tds7 = tds[7].div["title"]
                    item = (tds0,tds[1].get_text(),tds[2].get_text(),
                             tds[3].get_text().strip(),tds[4].get_text(),
                             tds[5].get_text(),tds6,tds7,tds[8].get_text(),
                             tds[9].get_text())
                    items.append(item)
            except TypeError as e:
                print('get_html_td TypeError:' + e.__str__())
                continue
        print("--page--")
        write_excel(items)
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)
    # print(html)

def write_excel(items):
    # 将要保存的excel文件位置
    excel_file = r'E:\xicidaili.xlsx'
    # 如果尚未创建该excel文件
    if not os.path.exists(excel_file):
        # 新建一个excel工作簿
        wb = openpyxl.Workbook()
        # 新建一个sheet
        ws = wb.active
        # 修改sheet名称
        ws.title = u'国内高匿代理IP'
        # 设置表格头
        ws.append(['国家', 'IP地址', '端口', '服务器地址', '是否匿名', '类型',
                   '速度', '连接时间', '存活时间', '验证时间'])
        # 把items添加至sheet
        for item in items:
            ws.append(item)
    else:
        # 如果该excel文件已经存在，即打开该文件
        wb = openpyxl.load_workbook(excel_file)
        # 选中该sheet
        ws = wb.get_sheet_by_name(u'国内高匿代理IP')
        # 把items添加至sheet
        for item in items:
            ws.append(item)
    # 保存文件
    wb.save(excel_file)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/1'
    get_html(url)

```
代码比较丑，见谅啊。
这我们多了一个方法write_excel，该方法用于向excel保存items ,items形如[('a','b'),('c','d'),('e','f')...]
所以我们从get_html获取items 用于传给write_excel
好了，我运行结果成功！E盘生成了一个大小12KB的excel文件，有100行数据。完美。

## 第八步 抓取所有页面

上面已经实现了爬取http://www.xicidaili.com/nn/1 一页的100条数据，且保存于excel中。
可是该目录下有2488页，好嘞，让我们来实现抓取这么多页面且保存为excel。
这里就删除html_doc了。
看代码：
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_htmls(url,num):
    for i in range(1, num+1):
        print(url % i)
        get_html(url%i)

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        response = request.Request(url=url, headers=headers)
        html = request.urlopen(response).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        items = []
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                tds0,tds6,tds7 = '','',''
                if len(tds) == 10:
                    if tds[0].img: tds0 = tds[0].img["alt"]
                    if tds[6].div:tds6 = tds[6].div["title"]
                    if tds[7].div:tds7 = tds[7].div["title"]
                    item = (tds0,tds[1].get_text(),tds[2].get_text(),
                             tds[3].get_text().strip(),tds[4].get_text(),
                             tds[5].get_text(),tds6,tds7,tds[8].get_text(),
                             tds[9].get_text())
                    items.append(item)
            except TypeError as e:
                print('get_html_td TypeError:' + e.__str__())
                continue
        write_excel(items)
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)

def write_excel(items):
    excel_file = r'E:\xicidaili.xlsx'
    if not os.path.exists(excel_file):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = u'国内高匿代理IP'
        ws.append(['国家', 'IP地址', '端口', '服务器地址', '是否匿名', '类型',
                   '速度', '连接时间', '存活时间', '验证时间'])
        for item in items:
            ws.append(item)
    else:
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.get_sheet_by_name(u'国内高匿代理IP')
        for item in items:
            ws.append(item)
    wb.save(excel_file)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/%s'
    get_htmls(url,2488)
```
很忐忑呀！看着excel文件从0KB慢慢增长，有时候还会突然变成0字节，真的吓人。

我的天，笔者运行到50页的时候突然电脑没电关机了。大家务必保证，网络通畅，电源充足，耐心惊人。


## 第九步 优化效率之用内存来换IO

笔者测试的时候从15:50开始，到...

耗时极长，越到后面，速度读写速度越慢。该如何改善呢。我的第一想法是，减少IO读写次数。

确实，在大数据处理中的瓶颈是IO，而不是哪种语言。


看了看自己的任务管理器，当我爬到136页的时候，时间到了16:07。**我决定用内存来换IO**

请看总结再运行代码
```python
# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_html(url,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    items = []
    for page in range(1, 2489):
        try:
            response = request.Request(url=url%page, headers=headers)
            html = request.urlopen(response).read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            trs = soup.find_all('tr')
            for i in range(1, len(trs)):
                try:
                    tds = trs[i].find_all("td")
                    tds0,tds6,tds7 = '','',''
                    if len(tds) == 10:
                        if tds[0].img: tds0 = tds[0].img["alt"]
                        if tds[6].div:tds6 = tds[6].div["title"]
                        if tds[7].div:tds7 = tds[7].div["title"]
                        item = (tds0,tds[1].get_text(),tds[2].get_text(),
                                 tds[3].get_text().strip(),tds[4].get_text(),
                                 tds[5].get_text(),tds6,tds7,tds[8].get_text(),
                                 tds[9].get_text())
                        items.append(item)
                except TypeError as e:
                    print('get_html_td TypeError:' + e.__str__())
                    continue
            print(url % page)
        except request.URLError as e:
            print('get_html Error:'+e.reason)
            html = None
            if num_retries>0:
                if hasattr(e,'code') and 500<=e.code<600:
                    # recursively retry 5xx HTTP errors
                    return get_html(url,num_retries-1)
        if page%50==0 or page==2488:
            write_excel(items)
            items = []
            print("---finish "+page.__str__()+"pages---")



def write_excel(items):
    excel_file = r'E:\xicidaili.xlsx'
    if not os.path.exists(excel_file):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = u'国内高匿代理IP'
        ws.append(['国家', 'IP地址', '端口', '服务器地址', '是否匿名', '类型',
                   '速度', '连接时间', '存活时间', '验证时间'])
        for item in items:
            ws.append(item)
    else:
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.get_sheet_by_name(u'国内高匿代理IP')
        for item in items:
            ws.append(item)
    wb.save(excel_file)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nn/%s'
    get_html(url)
```

## 总结
哈哈，是不是快了很多！
额...你一定发现问题了，我们再次遇见503...
就是因为太快，所以被服务器鉴别出来了。亲爱的服务器呀，我是好人...
怎么办好呢？要用代理了。

>注意：不要真的爬2488页，会被服务器限制访问。几十页就好。
> P  S ：程序可以正常运行，不过上面的循环好像有点问题... 哈哈

本文仅用于学习。转载请注明。
.com 实战
