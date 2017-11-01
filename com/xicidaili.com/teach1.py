# _*_ coding:utf‐8 _*
from urllib import request
import os
import openpyxl
from bs4 import BeautifulSoup

def get_htmls(url,num,items = []):
    for i in range(110, num+1):
        print(url % i)
        get_html(url%i,items)
        if i%2==0 or i==num:
            write_excel(items)
            items = []


def get_html(url,items,num_retries = 2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        response = request.Request(url=url, headers=headers)
        html = request.urlopen(response).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')
        # items = []
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
        #write_excel(items)
    except request.URLError as e:
        print('get_html Error:'+e.reason)
        html = None
        if num_retries>0:
            if hasattr(e,'code') and 500<=e.code<600:
                # recursively retry 5xx HTTP errors
                return get_html(url,num_retries-1)

def write_excel(items):
    excel_file = r'E:\xicidaili_2.xlsx'
    if not os.path.exists(excel_file):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = u'国内透明代理IP'
        ws.append(['国家', 'IP地址', '端口', '服务器地址', '是否匿名', '类型',
                   '速度', '连接时间', '存活时间', '验证时间'])
        for item in items:
            ws.append(item)
    else:
        wb = openpyxl.load_workbook(excel_file)
        ws = wb.get_sheet_by_name(u'国内透明代理IP')
        for item in items:
            ws.append(item)
    wb.save(excel_file)

if __name__=='__main__':
    url = 'http://www.xicidaili.com/nt/%s'
    get_htmls(url,563)