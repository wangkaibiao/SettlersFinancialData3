# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:12:48 2018

@author: 18253
"""

import pandas as pd#pandas不用考虑字符编码问题


content=open(
"/media/bdai/LENOVO/Databases/文字数据/2018年度济南分行零售业务风险政策指引v4.txt")
content_str=content.read()
"新增信用类小贷业务客户评分原则上不低于8档，新增保证类小贷业务客户评分原则上不低于7档" in content_str#True

                          
qs=pd.read_csv("/media/bdai/LENOVO/Databases/文字数据/12套题.csv")
questions=qs["questions"]
selections=qs["selections"]
#i=31
for i in range(189):
    selection=selections[i].split("[")
    if len(selection)==1:
        if questions[i] in content_str:
            qs["answer"][i]="T"
        else:
            qs["answer"][i]="F"
    else:
        ans=[]
        for sele in selection:            
            one_selection=sele.split("].")
            try:
                if one_selection[1].strip() in content_str:
                    
                    #去除空格、末尾标点符号可以增加准确性
                    ans.append(one_selection[0])
            except:
                print("空")
        qs["answer"][i]=str(ans)
                
qs["answer"]

##确保Python2写入text文件时不出现编码问题
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
#qs.to_excel("题库答案.xlsx")
qs.to_csv("题库答案2.csv")
        
