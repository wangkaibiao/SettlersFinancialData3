# -*- coding: utf-8 -*-
'''才一百多万行数据，是否考虑直接用python处理完再快速导入的MySQL中？？？'''

import pymysql as pdb
import random
import numpy as np


def todb(db='wangkaibiao'):#可以同时开两个数据库，但是得从头到尾无遗漏执行程序
    return pdb.connect(host='localhost',
                     port=3306,#mysql安装默认端口是3306，安装未更改的话是3306
                     user='root',
                     passwd='123456',
                     db=db,
                     charset="utf8")
    
wkb=todb()
wkb_cursor = wkb.cursor()   

wkb_cursor.execute("show tables")
train_table=wkb_cursor.fetchall()[0][0]
print(train_table)


#ft=todb(db='fund_train')
#ft_cursor=ft.cursor()

#多了容易造成行大小超限
def create_table(table="2week_average_grow"):
    delete_table='drop table if exists '+table
    #或只删数据"delete from fundnets"
    wkb_cursor.execute(delete_table)
    create_table_sql ='CREATE TABLE '+table+' (fundid VARCHAR(6) NOT NULL,\
    rate_m VARCHAR(25),nets VARCHAR(10000))'
    wkb_cursor.execute(create_table_sql)
    #不能放在return后边，否则不保存插入数据
#    wkb.commit()#1456868条数据插入用时5分钟
#    wkb.close()#关闭之后，后续的Python执行会显示错误
    print("ok")
    
#create_table("1mon_ave_aft_2week_divided_3day_ave")

    
def processdata(table="1mon_ave_aft_2week_divided_3day_ave"):
    #5分钟处理1200个基金，实现随时分析处理较大数据
    create_table(table)
    fundid_str=open("a_fund_trade//fundid.txt")
    fundid=eval(fundid_str.read())
    #eval的列表字符串中不能有回车，即列表元素要紧挨着
    lens=len(fundid)
    print("基金代码列表长度为：%s，随机一个代码为：%s"%(lens,
                                  fundid[random.randint(0,lens)]))
    
    select_all_sql='select fundid,sumnet,netdate from fundnets'
    wkb_cursor.execute(select_all_sql)
    all_sumnet=wkb_cursor.fetchall()
    alls=np.array(all_sumnet)#156万条数据
    #alls[1:3,:]
    error_fund=["含有杂质的基金"]
    trains=[]
    i=0
#    fi="762001"
    for fi in fundid:
        i+=1
        print("当前进行到第%s个"%i)
        test=alls[alls[:,0]==fi,:]
        test1=test[test[:,2].argsort()]#按照日期升序排列
    #np.array(["1"]).astype(np.float32)#array([ 1.], dtype=float32)
    #np.array(["a"]).astype(np.float32)#ValueError: could not convert string to float: a
    #np.array(["1%"]).astype(np.float32)#ValueError: invalid literal for float(): 1%
        try:
            nets=test1[:,1].astype(np.float32)
            for j in range(len(nets)-91):
#                rate1=sum(nets[j+71:j+91])/20/nets[j+60]-1
#                #2周之后的一个月内平均净值比当前时点的增长情况
#                #"2week_average_grow"
                rate1=(sum(nets[j+71:j+91])/20) / (sum(nets[j+57:j+60])/3) -1
                #2周之后的一个月内平均净值比当前时点近3日平均净值的增长情况
                #"1mon_ave_aft_2week_divided_3day_ave"
                net_60=list(nets[j:j+60])
                #len(net_60)
                trains.append([fi,str(rate1),"%s"%net_60])#注意缩进
                #trains[0][2]
        except:
            error_fund.append(fi)
            print("%s基金数据含有杂质"%fi)
            
    random.shuffle(trains)
    print(trains[0][2])
#    trains1=[map(str,data) for data in trains]
#    t=map(str,trains[0])
#    print(type(trains[0][1]),type(t[1]),type(trains1[0][1]))
#    #(<type 'numpy.float64'>, <type 'str'>, <type 'str'>)
    print("处理并随机排序后的结果包含%s条数据"%len(trains))
    #(<type 'numpy.float64'>, <type 'str'>, <type 'str'>)
    #处理后的结果包含1456868条数据
    insql = "INSERT INTO "+table+" VALUES (%s,%s,%s)"#和上边创建的表对应        
    wkb_cursor.executemany(insql,trains)#防止按键触发KeyboardInterrupt
    wkb.commit()#1456868条数据插入用时5分钟
    wkb.close()
    print("成功创建训练数据库，异常基金有%s条"%len(error_fund))
    
    error_fund_str=open("a_fund_trade//error_fund.txt","w")#,encoding="utf-8"
    error_fund_str.write(str(error_fund))
    error_fund_str.close()  
    
processdata("1mon_ave_aft_2week_divided_3day_ave")


#查看异常基金的情况（一般是缺失值造成整理数据异常）
wkb_cursor.execute('select fundid,sumnet,netdate from fundnets \
                   where fundid="001106"')
wkb_cursor.fetchall()
#查看整理后的数据格式
wkb_cursor.execute(
        'select * from 1mon_ave_aft_2week_divided_3day_ave limit 5,6')
wkb_cursor.fetchall()


#用复制数据库的方法、产生随机排序的数据表，非常浪费时间
#rand_ct='CREATE TABLE grow_rand AS  \
#(SELECT * FROM grow ORDER BY RAND() )'
##复制表并随机排序的方法之一，1436613条记录用时4h17m
## 1436613条记录select count(*) from grow;用时7s
#ft_cursor.execute(rand_ct)
#ft.commit()

#导出数据到CSV，157万条数据不到1分钟导出
secure_file_priv="/var/lib/mysql-files/%s.csv\
"%"1mon_ave_aft_2week_divided_3day_ave"
csv_sql='select * from 1mon_ave_aft_2week_divided_3day_ave \
into outfile "%s"'%secure_file_priv #必须用引号把文件名隔开
wkb_cursor.execute(csv_sql)


#由csv导入到数据库，5分钟就导入123万行
ctsql3 ='CREATE TABLE 2_week_grow (fundid VARCHAR(6) NOT NULL,\
rate_m VARCHAR(25),nets VARCHAR(10000))'
wkb_cursor.execute(ctsql3)

import_sql2=' load data infile \
"E:/Databases/1mon_ave_aft_2week_divided_3day_ave.csv" \
into table 1mon_ave_aft_2week_divided_3day_ave ' #1323170
wkb_cursor.execute(import_sql2)
wkb.commit()