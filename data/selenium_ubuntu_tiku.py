# -*- coding: utf-8 -*-
"""
学习关键字：
pip3 install selenium   安装selenium
selenium 保存iframe中文
selenium js
"""
from selenium import webdriver
from storage import baidu_cloud as bdc
from time import sleep
from lxml import etree
import csv


'''一、设置浏览器参数并打开一个新的浏览器窗口
sudo mv chromedriver /usr/bin/   移动到/usr/bin/文件夹下(复制则将mv改为cp)，不需要加上执行权限 chmod +x chromedriver

'''
def chrome():
    chrome_options = webdriver.ChromeOptions()#继承源码中的类，详情搜索：selenium配置chrome选项
    chrome_options.add_extension(bdc.externalPaths[0]+"/can_google.crx")
    browser = webdriver.Chrome(options=chrome_options)
    return browser        
#c=chrome()
#c.get("http://360.hao245.com")#当网页完全打开加载完成时才会继续下一步
    

class test(object):#虽然括号里没有写参数，但是建立实例时要把init中的参数都传入
    def __init__(self,url):
        self.url="https://www.baidu.com"#"http://360.hao245.com"
    def a_chrome(self,url2):#加上self才能使用init中的参数
        chrome_options = webdriver.ChromeOptions()#继承源码中的类，详情搜索：selenium配置chrome选项
        chrome_options.add_extension(bdc.externalPaths[0]+"/can_google.crx")
        browser = webdriver.Chrome(options=chrome_options)
        #return browser.get(url)
        browser.get(self.url)
        sleep(10)
        browser.get(url2)        
#scan=test("随便输入一个，但必须有对应的参数")
#a=scan.a_chrome("https://pan.baidu.com/")
#b=scan.a_chrome("https://www.baidu.com")#会新打开窗口

'''二、登陆上之后可以在下边做任意控制操作
在火狐浏览器上安装katalon recorder，并录制导出动作，注意导出时可以选择各种程序语言环境、如选择python2'''
def test_question_ans():#目前只能操控固定的窗口
    url="https://nexam.cmbc.com.cn/wis18/usermain/paper/userpaper.answeruserpapercurr.flow?sid=5851745584847088"
    url="https://nexam.cmbc.com.cn/wis18/userpaper.viewuserhispaperqueslist.flow?p_id=6094126582324386&trys=2"
    #"https://nexam.cmbc.com.cn/wis18/usermain/paper/userpaper.answeruserpapercurr.flow?sid=5851745584847088"
    browser=chrome()
    browser.get(url)
    #对于嵌套frame的网页，要先转换到相应层的frame、然后处理里边包含的html
    browser.switch_to.frame(0)#通过index索引号逐个尝试目标信息在哪一层，
    #每次都要重新打开首页    
    for i in range(0,100):#开始下载目标信息保存到html文件，用于后续提取
        sleep(0.5)
        with open("question_ans/probe12_%s.html"%i,"w") as f:
            f.write(browser.page_source)        
        browser.find_element_by_xpath('//*[@id="next"]').click()    
    #后续从离线网页提取信息，
    questions=[]
    for i in range(2,5):
        for j in range(100):
            htmlfile=open("/media/bdai/LENOVO/Databases/question_ans/probe%s_%s.html"%(i,j),'r')
            htmlhandle = htmlfile.read()
            html_data=etree.HTML(htmlhandle,parser=etree.HTMLParser(encoding='utf-8'))    
            question_ans=html_data.xpath('//*[@id="maindiv"]/table/tbody/tr/td/table/tbody/tr[2]/td/div/table/tbody/tr/th[3]/div/form/table[2]/tbody/tr/th/table/tbody/tr/th/div//text()')
            questions.append(question_ans)
    #并保存到csv文件中    
    questions_file = open("test.csv",'w')
    writer = csv.writer(questions_file)
    writer.writerows(questions)
    questions_file.close()

'''三、无框架的情况'''
browser=chrome()
url="https://nexam.cmbc.com.cn/wis18/userpaper.viewuserhispaperqueslist.flow?p_id=6094126582324386&trys=10"
browser.get(url)

questions=[]
for i in range(0, 155):  # 开始下载目标信息保存到html文件，用于后续提取
    sleep(0.5)
    questions.append( browser.find_element_by_xpath('//*[@id="mainfrm"]/table[1]/tbody/tr[3]/td/table/tbody/tr[2]'
                                                    ).get_attribute('textContent')  )
    browser.find_element_by_xpath('//*[@id="mainfrm"]/table[2]/tbody/tr/td/p/input[2]').click()

#并保存到csv文件中
questions_file = open("test.csv",'w')
writer = csv.writer(questions_file)
writer.writerow(questions)
questions_file.close()