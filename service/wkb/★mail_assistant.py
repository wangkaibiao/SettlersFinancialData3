# -*- coding: utf-8 -*-
"""Created on Sun May  6 21:53:47 2018 @author: 18253"""
   
import poplib
import base64
from lxml import etree
from urllib2 import urlopen
from readability import Document
from bs4 import BeautifulSoup 


'''一、登录邮箱'''

host = "pop3.139.com"# pop3服务器地址
username = "cmbc95568@139.com"# 用户名
password = "wkb230870"# 密码
pp = poplib.POP3(host)# 创建一个pop3对象，这个时候实际上已经连接上服务器了
pp.set_debuglevel(1)# 设置调试模式，可以看到与服务器的交互信息
print(pp.getwelcome().decode('utf-8'))
pp.user(username)# 向服务器发送用户名#b'+OK'
pp.pass_(password)# 向服务器发送密码#b'+OK login success'

'''二、获取服务器上信件信息，本应用中只获取邮件中的地址就行'''
#返回是一个列表：第一项是一共有多少封邮件，第二项是共有多少字节
print('Messages: %s. Size: %s' % pp.stat())# stat()返回邮件数量和占用空间:
resp, mails, octets = pp.list()# list()返回所有邮件的编号:
print(mails)# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
#通过索引号获取邮件，获取最新一封邮件, 注意索引号从1开始:
index = len(mails)#求出收件箱内的邮件数目
resp, content_lines, octets= pp.retr(index)
#必须在链接状态下获取最新一封邮件,lines存储了该封邮件的原始文本的每一行,可以获得整个邮件的原始文本:
print(len(content_lines),type(content_lines))#(1421, <type 'list'>)

"""整理邮件内容，获取网址列表"""
#邮件的内容是混合编码、但是肯定包含base64，base64编码转换需要摘出集中的纯base64的内容
useful_lines=[]#找到集中的纯base64的内容
start_line=0
for i,line in enumerate(content_lines):
    if "base64" in line:#必须先保证找到起始行之后，才能进行下边的判断
        useful_lines.append(i+1)
        start_line=i
        print(start_line,content_lines[start_line:start_line+3])
    elif (start_line>0) and (i>start_line):#有起始行了，并且确保判断的是起始行之后的行
         useful_lines.append(i)
         if "==" in line:#google 的比较特殊，base64编码之后还有内容，但是百度的没有
             break

monitor_content ="".join(content_lines[min(useful_lines):max(useful_lines)+1])

#a = base64.b64encode("我是字符串")
#a=base64.b64decode(monitor_content)#解码必须是完整的开头和结尾
#type(a)
#print(a)
#with open("./temp/googlenews.html","w") as news_email:
#    news_email.write(a)
Unicode_str=base64.b64decode(monitor_content)#解码必须是完整的开头和结尾
strdata = etree.HTML(Unicode_str, parser=etree.HTMLParser(encoding='utf-8'))
hrefs=strdata.xpath("//@href")#选取名为 href 的所有属性而不管它们所在元素的位置。
urls=[href for href in hrefs if "baidu.com" not in href]#百度格式的网址提取
if urls==[]:
    #hrefs=strdata.xpath("//*")#选取文档中的所有元素。但是Google的结果不能提取标签的属性，看似有标签实际上没有标签    
    urls=[url.replace("url=","") for url in Unicode_str.split("&") if "url=" in url]


"""收集内容"""
#http://linyi.iqilu.com/caijing/2018/1117/4113682.shtml
for news_url in urls:
    apidata = urlopen(news_url,timeout=15)#设置timeout后，urlopen不会一直等待网址响应、也就不会出现卡死现象
    ht = apidata.read()#str类型的网页源码，这条指令和parse冲突，不能同时运行
    #response = requests.get('http://example.com')
    #doc = Document(response.text)
    doc=Document(ht)    
    print(doc.title())
    type(doc.summary())#unicode
    clean_html=BeautifulSoup(doc.summary()) 
    print(clean_html.get_text()) 
    
    