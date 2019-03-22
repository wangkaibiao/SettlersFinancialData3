# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:15:17 2017 @author: wangkaibiao
动态网页是指跟静态网页相对的一种网页编程技术。静态网页，随着html代码的生成，页面的内容和显示效果就基本上不会发生变化了——除非你修改页面代码。
而动态网页则不然，页面代码虽然没有变，但是显示的内容却是可以随着时间、环境或者数据库操作的结果而发生改变的。与静态网页相对应的，
能与后台数据库进行交互，数据传递。也就是说，网页 URL的后缀不是.htm、.html、.shtml、.xml等静态网页的常见形动态网页制作格式，
而是以.aspx、.asp、.jsp、.php、.perl、.cgi等形式为后缀，并且在动态网页网址中有一个标志性的符号——“?”。可以通过以下方式简单验证某网页是否
为动态网页。在页面上右键查看源代码，和右键审查元素所看到的html代码是不一样的，如果后者中能看到商品数据信息，而前者没有的话，
就说明这个页面是动态生成的。
"""

import pymysql as pdb
from urllib2 import urlopen
#from urllib.request import urlopen#use for python3
import time#往前推几天又两种办法
import random
from lxml import etree
import smtplib
import os
 

#os.name
##如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统。
#os.uname()#获取详细的系统信息
##注意uname()函数在Windows上不提供，也就是说os模块的某些函数是跟操作系统相关的
##操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，要注意
## 查看当前目录的绝对路径:
#os.path.abspath('.')#'/home/bdai/SettlersFinancialData'
## 在某个目录下创建一个新目录，
## 首先把新目录的完整路径表示出来:
#os.path.join('/Users/michael', 'testdir')#'/Users/michael/testdir'
## 然后创建一个目录:
#os.mkdir('/Users/michael/testdir')
## 删掉一个目录:
#os.rmdir('/Users/michael/testdir')
#
##判断是否是绝对路径：
#os.path.isabs("/media/bdai/LENOVO/Databases/fundnets_backup.csv")#True
#
#os.mknod("/media/bdai/LENOVO/Databases/fundnets_backup.csv")#创建空文件
#fp = open("test.txt","w") #直接打开一个文件，如果文件不存在则创建文件
#
#
#time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())#'2018-07-29 10:53:05'


'''-------一、连接数据库并查找继续点--------''' 
def todb(data_base_name='wangkaibiao'):
    return pdb.connect(host='localhost',
                     port=3306,#mysql安装默认端口是3306，安装未更改的话是3306
                     user='root',
                     passwd='123456',
                     db=data_base_name,
                     charset="utf8")
    
db=todb()
cursor = db.cursor()

#★★★★★一定要先备份数据库，防止下方参数设置失误而功亏一篑★★★★★
win_secure_file_priv="D:/Databases/fundnets_backup.csv"
secure_file_priv="/var/lib/mysql-files/fundnets_backup%s.csv\
"%time.strftime("%Y%m%d", time.localtime())
#"./fundnets_backup.csv"
#"/media/bdai/LENOVO/Databases/fundnets_backup.csv"
#以上两种方法都显示权限不足的问题，这说明ubuntn的mysql只在特定文件夹操作，
#此外，编程序一定要注意正确示例中的标点符号区别，
#毕竟windows和linux的底层基础程序语言是不同的。
try:
    os.remove(secure_file_priv)
    print("成功删除文件")
except:
    print("文件不存在")
win_backup_sql='select * from fundnets into outfile %s '%win_secure_file_priv 
#1323170
backup_sql='select * from fundnets into outfile "%s" '%secure_file_priv
cursor.execute(backup_sql)
#★★★★★一定要先备份数据库，防止下方参数设置失误而功亏一篑★★★★★    

#查找获取数据的起始日期（用列表的最后一个基金）
check_sql='select max(netdate) from fundnets where fundid=%s'
cursor.execute(check_sql,"000001")
print (cursor.fetchall())

#从断点处继续下载追加数据
continue_sql = 'select count(*) from fundnets where netdate=%s'
cursor.execute(continue_sql,"2018-07-13")
print (cursor.fetchall())

check_sql = 'select count(*) from fundnets_check where netdate=%s'
cursor.execute(check_sql,"2018-11-09")
print (cursor.fetchall())

#恢复最近保存的数据库：由csv导入到数据库，5分钟就导入123万行
def recover():#套用函数防止误删
    delete_table='drop table if exists fundnets '
    #或只删数据"delete from fundnets"
    cursor.execute(delete_table)
    #'CREATE TABLE fundnets (fundid VARCHAR(6) NOT NULL,rate1 VARCHAR(25),\
    #rate2 VARCHAR(25),rate3 VARCHAR(25),nets VARCHAR(10000))'
    #净值日期	单位净值	累计净值	日增长率	申购状态	赎回状态	分红送配
    create_table='CREATE TABLE fundnets (fundid CHAR(6) NOT NULL,netdate DATE,\
    net CHAR(255),sumnet CHAR(255),daygrowrate CHAR(255),\
    canbuy CHAR(255),cansold CHAR(255),dividends CHAR(255))'
    cursor.execute(create_table)
    
    windows_import_sql=' load data infile "D:/Databases/fundnets_backup.csv" \
    into table fundnets ' #前面直接没设置导出的，此处就可以不设置直接导入
    linux_import_sql=' load data infile \
    "/var/lib/mysql-files/fundnets_backup.csv" \
    into table fundnets ' #mysql> show variables like '%secure%';
    #通过secure_file_priv找到有权限的文件夹
    cursor.execute(linux_import_sql)
    db.commit()
    
    
#重新收集一遍数据来检查程序的准确性
create_table='CREATE TABLE fundnets (fundid CHAR(6) NOT NULL,netdate DATE,\
net CHAR(255),sumnet CHAR(255),daygrowrate CHAR(255),\
canbuy CHAR(255),cansold CHAR(255),dividends CHAR(255))'
create_check='CREATE TABLE fundnets_check (fundid CHAR(6) NOT NULL,netdate DATE,\
net CHAR(255),sumnet CHAR(255),daygrowrate CHAR(255),\
canbuy CHAR(255),cansold CHAR(255),dividends CHAR(255))'
cursor.execute(create_table)


'''-------二、定义爬取单个基金数据的函数--------'''   
#http://fund.eastmoney.com/js/fundcode_search.js#基金名称和代码  
def fund_nets(table="fundnets",fundid="000011",sdate="1990-01-01",edate="2018-11-20"):
    #获取api静态网页数据，【包含】起始日期的数据
    try:
        server_engine="http://fund.eastmoney.com/f10/F10DataApi.aspx?"
        stable_parameter="type=lsjz&page=1&per=10000&"
        variable_parameter="code=%s&sdate=%s&edate=%s"%(fundid,sdate,edate)
        url=server_engine+stable_parameter+variable_parameter
        apidata = urlopen(url,timeout=5)#设置timeout后，urlopen不会一直等待网址响应、也就不会出现卡死现象
        ht = apidata.read()#str类型的网页源码，这条指令和parse冲突，不能同时运行
        strdata = etree.HTML(ht, parser=etree.HTMLParser(encoding='utf-8'))#<type 'lxml.etree._Element'>
        tbody=strdata.xpath("/html/body/table/tbody//tr")#chrome copy xpath
        print("    %s获取 %s 行xpath数据"%(fundid,len(tbody)))        
        #要防止汉语在数据库中因为编码问题而无法插入，所以在明确列标题意义的前提下，尽量用英语替换
        rows=[]
        for row in tbody:
            tds=[fundid]#根据提前设计的数据收集格式而定
            for i in range(1,8):#根据表头th的数量来定                
                #row.xpath("./td[1]/text()")#结果是列表['2017-08-21']
                td=row.xpath("./td[%s]/text()"%i)
                if i==7:
                    if td ==[]:
                        tds.append("no")
                    else:
                        tds.append("yes")
                elif i==5:
                    if td[0]==u"开放申购":
                        tds.append("yes")
                    else:
                        tds.append("no")
                elif i==6:
                    if td[0]==u"开放赎回":
                        tds.append("yes")
                    else:
                        tds.append("no")
                else:
                    if td ==[]:
                        tds.append("")
                        print(i)
                    else:
                        tds.append(td[0])
            rows.append(tds)
        print("    %s整理得到 %s 行列表数据"%(fundid,len(rows)))
#        rows[1]
#        print(u'\u5f00\u653e\u7533\u8d2d'+u'\u5f00\u653e\u8d4e\u56de')
        
        if len(rows)==0:
            return "nodata",url
        else:
            db = todb()
            cursor = db.cursor()
#insql="INSERT IGNORE INTO "+table+" VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
#需要配合创建表添加额外唯一性参数使用
            insql="INSERT INTO "+table+" VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.executemany(insql,rows)#整体提交防止只获取部分数据
            #not enough arguments for format string就是参数数量不匹配的提示
            #
            db.commit()
            db.close()
            return "insert_sucess",len(rows)        
    except:
        return "error",url
    
    
'''-------三、定义发送邮件来定时监控数据收集进度--------'''  
def sendmail(Text):#全过程不能出现中文字符和标点
    Server = "smtp.qq.com" # QQ邮箱的SMTP服务器地址
    Subject = "oversight schedule"  # 邮件主题
    To = "cmbc95568@139.com" # 收件人
    From = "780901581@qq.com" # 发件人
    #Text = "This is the email send by xpleaf, from xpleaf@163.com!" # 邮件内容
    Body = '\r\n'.join(("From: %s" % From,
                    "To: %s" % To,
                    "Subject: %s" % Subject,
                    "",
                    Text)) 
    s = smtplib.SMTP()  # 实例化一个SMTP类
    s.connect(Server, '25') # 连接SMTP服务器
    s.starttls()    # 开启TLS（安全传输）模式
    s.login('780901581@qq.com', 'ydbnqlalrowxbecg')   # 登陆到163邮件服务器
    s.sendmail(From, [To], Body)    # 发送邮件
    s.quit()    # 退出
    

'''------四、开始收集数据，使用函数可以降低错误率因为参数集中一目了然-------'''
#采集过程中可能会因为本地网络访问而被打断(使用timeout方法)
def collect_data(table="fundnets",start=0,
                 sdate="1990-01-01",edate="2018-05-17"):
    #读取目标基金、并生成列表
    fundid_str=open("a_fund_trade//fundid.txt")
    fundid=eval(fundid_str.read()) #eval的列表字符串中不能有回车，即列表元素要紧挨着
    lens=len(fundid)
    print("基金代码列表长度为：%s，随机一个代码为：%s"%(lens,
                                  fundid[random.randint(0,lens)]))
    
    i=start
    #i=598#继续点==已经成功插入基金的个数，这是列表索引从0开始决定的
    #收集异常值
    nodata_fi={"无数据基金":"待查看网址"}
    error_fi={"错误基金":"待查看网址"}
    oversight=0#监督以避免死循环产生
    lastminute=1#每隔10分钟只发一次进度汇报的分钟标记
    
    while i<len(fundid):
        #不能是<=否则该循环永远不能停止。超出条件后自动终止while循环，不用添加break
        now= time.localtime(time.time())#获取当前时间结构
        if  now[4]%10==0 and now[4] != lastminute :#每到10分钟发一次进度汇报
            lastminute=now[4]
            sendmail("schedule:%s"%i) 
        rd=random.randint(1,9)
        for fi in fundid[i:i+rd]:
            if oversight>3:
                oversight=0
            i+=1
            result,url=fund_nets(table,fi,sdate,edate)
            #result,url=fund_nets(fi,"1990-01-01","2018-05-17")
            if result=="error" and oversight<3:
                i=i-1 #如果多次无法继续，要跳过
                #这一步一旦发生，有可能造成死循环，无法继续进行：
                #停止的基金会造成死循环，timeout的原因不会
                oversight +=1
                break
                print(i,result)
            elif result=="error" and oversight==3:
                oversight +=1
                error_fi[fi]=url
                break            
            elif result=="nodata":
                nodata_fi[fi]=url        
            else:
                print(i,result,">>>>>>>>>>>>>>>>>>>>>>>>")
                
    print(nodata_fi,error_fi)
    continue_check=open("a_fund_trade//continue_check.txt","w")
    #,encoding="utf-8"
    continue_check.write(str([nodata_fi,error_fi]))
    continue_check.close()
    
#开始收集
collect_data(table="fundnets",start=0,sdate="1990-01-01",edate="2018-11-11")
    
#处理错误
fund_nets(table="fundnets",fundid="003941",
              sdate="2018-05-18",edate="2018-05-18") 


'''------五、检查数据的准确完整有效性-------'''
#程序稳定性检查对比
count1_sql = 'select count(*) from fundnets'
cursor.execute(count1_sql)
print ("fundnets的数据量为：%s"%cursor.fetchall())
count2_sql = 'select count(*) from fundnets_check'
cursor.execute(count2_sql)
print ("fundnets_check的数据量为：%s"%cursor.fetchall())

#找出重复数据
check_repeat1=' SELECT COUNT(*) as repetitions,\
fundid,netdate  \
FROM fundnets  \
GROUP BY fundid,netdate  \
HAVING repetitions >1 '  #一个基金一天只有一个数据
cursor.execute(check_repeat1)
repetition=cursor.fetchall()#列表不能直接和%s同时使用
print ("fundnets重复数据为%s条"%len(repetition))#fundnets重复数据为2973条

check_repeat2=' SELECT COUNT(*) as repetitions,\
fundid,netdate,net,sumnet,daygrowrate,canbuy,cansold,dividends  \
FROM fundnets_check  \
GROUP BY fundid,netdate  \
HAVING repetitions >1 '  
cursor.execute(check_repeat2)#选择的字段越少、速度越快
repetition=cursor.fetchall()
print ("fundnets_check重复数据为%s条"%len(repetition))
#fundnets_check重复数据为0条
    
#三种过滤重复数据的方法
distinct='SELECT DISTINCT \
fundid,netdate,net,sumnet,daygrowrate,canbuy,cansold,dividends \
FROM fundnets'

group_by='SELECT fundid,netdate,net,sumnet,daygrowrate,canbuy,cansold,\
dividends  FROM fundnets \
GROUP BY (fundid,netdate)'

    #设置双主键模式来设置数据的唯一性，键的默认值不能为NULL，可设置为NOT NULL
create_table='CREATE TABLE fundnets (fundid CHAR(6) NOT NULL,\
netdate DATE NOT NULL,net CHAR(255),sumnet CHAR(255),daygrowrate CHAR(255),\
canbuy CHAR(255),cansold CHAR(255),dividends CHAR(255)) \
PRIMARY KEY (fundid,netdate)'
    #INSERT IGNORE INTO 如果数据库没有数据，就插入新的数据，如果有就跳过这条数据。
    #INSERT INTO 在遇到重复数据时会抛出错误
    #REPLACE INTO 如果存在primary 或 unique相同的记录，则先删除掉。再插入新记录
    #另一种设置数据的唯一性方法是添加一个UNIQUE索引
create_table='CREATE TABLE fundnets (fundid CHAR(6) NOT NULL,\
netdate DATE NOT NULL,net CHAR(255),sumnet CHAR(255),daygrowrate CHAR(255),\
canbuy CHAR(255),cansold CHAR(255),dividends CHAR(255)) \
UNIQUE (fundid,netdate)'

#两种方法删除重复数据
create_table='CREATE TABLE tmp \
SELECT * FROM fundnets_check  GROUP BY (fundid,netdate)'
delete='DROP TABLE fundnets_check'
rename='ALTER TABLE tmp RENAME TO fundnets_check'

   #在数据表中添加 INDEX（索引） 和 PRIMAY KEY（主键）简单删除重复记录
delete_repetition='ALTER IGNORE TABLE fundnets_check \
ADD PRIMARY KEY (fundid,netdate)'
cursor.execute(delete_repetition)#1625075，用了大约10分钟

