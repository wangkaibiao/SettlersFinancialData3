# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from matplotlib import pyplot


def generate_month():
    
def credit_analysis(name="wangqingke"):#
    html=open("D:\\Databases\\credit\\%s.htm"%name)#不能用urlopen打开，只能打开http协议的
    soup=BeautifulSoup(html.read(),"html.parser")
    #print(soup.get_text())
    #print(soup.prettify())
    #content=soup.find_all("strong")
    #type(content)
    content=soup.find_all(text=re.compile("业务号"))#结果完全不同于soup.find_all(text="业务号")，compile是编译汇编的意思
    loans=[text.split(".")[1] for text in content if "贷款" in text]
    loan=[text.split("(人民币)")[0].split(".")[1] for text in content if "贷款" in text]
    loan=sorted(loan)
    print("最早贷款日:%s"%loan[0][:11])
    print(loan)
    #'109.2018年01月17日机构＂QA＂发放的300000元(人民币)个人经营性贷款,业务号X,组合（不含保证）担保,6期,按月归还,2018年07月17日到期.已于2018年02月08日结清.'
    #pyplot.plot([u"2017年01",u"2017年03","d"],[1,2,3])#直接横纵坐标设置好画序列图即可
    #'2013年06月01日机构＂QA＂发放的900000元'[:8]#'2013年06月'   ，和python2不同   .encode("utf-8")[:8].decode("utf-8")
    #eval('2013年06月01日机构＂QA＂发放的900000元'.split("发放的")[1].split("元")[0])
    loan_dic={}
    for text in loan:#能否用正则表达式提取信息
        date=text[:8]
        loan_num=eval(text.split("发放的")[1].split("元")[0])
        try:
            loan_dic[date] += loan_num
        except:
            loan_dic[date] = loan_num
            
    pyplot.plot(loan_dic.keys(),loan_dic.values())
    html.close()

credit_analysis(name="chenshuyin")

"""1、加入一个征信是否完整下载的检查点"""

#card=[text.split(",")[0] for text in content if "贷记卡" in text]
#2.2013年06月29日机构＂HG＂发放的贷记卡(人民币账户),业务号X,授信额度10000元,信用/免担保.截至2018年10月07日,

