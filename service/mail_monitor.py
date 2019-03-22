# -*- coding: utf-8 -*-
"""舆情监控"""
import os,sys,poplib,base64,csv
from urllib.request import urlopen
sys.path.append(os.getcwd()+"/storage/emulated/0/qpython/lib/python3.2/site-packages")
#from aip import AipNlp   
from aip.nlp import AipNlp

from lxml import etree
from bs4 import BeautifulSoup
from readability import Document


##全局变量必须放在最前面
#monitor_result=[]
#error_num=0
#success_num=0
#index=2298#2300
#while index < 5302:
#    index +=1
#    try:#防止整体错误        
##for index in range(2450,5301):
        
def oneMailUrls(index=6346):#index是第几封邮件，1代表最早一封邮件，0代表最新一封邮件    
    '''一、登录邮箱'''
    host = "pop3.139.com"# pop3服务器地址
    username = "cmbc95568@139.com"# 用户名
    password = "wkb230870"# 密码
    pp = poplib.POP3(host)# 创建一个pop3对象，这个时候实际上已经连接上服务器了
    pp.set_debuglevel(1)# 设置调试模式，可以看到与服务器的交互信息
    pp.user(username)# 向服务器发送用户名#b'+OK'
    pp.pass_(password)# 向服务器发送密码#b'+OK login success'    
    '''二、获取服务器上信件信息，本应用中只获取邮件中的网址就行''' 
    if index==0:
        index=len(pp.list()[1])
        print("共有%s封邮件"%index)
    resp, content_lines, octets= pp.retr(index)#必须在链接状态下获取最新一封邮件,len(pp.list())
    #resp是反应结果，content_lines存储了该封邮件的原始文本的每一行,octets是邮件内容总长度
    """三、整理邮件内容，获取网址列表"""
    if (b'From:baidunews@baidu.com' in content_lines)or(b'Delivered-To: wangkaibiao01@gmail.com' in content_lines):
        #邮件的内容是混合编码、但是肯定包含base64，base64编码转换需要摘出集中的纯base64的内容
        useful_lines=[]#找到集中的纯base64的内容
        start_line=0
        for i,line in enumerate(content_lines):
            try:
                line=line.decode()
                isByte=True
            except:
                print("内容不是byte类型")
            if "base64" in line:#必须先保证找到起始行之后，才能进行下边的判断
                useful_lines.append(i+1)
                start_line=i
                #print(start_line,content_lines[start_line:start_line+3])
            elif (start_line>0) and (i>start_line):#有起始行了，并且确保判断的是起始行之后的行
                 useful_lines.append(i)
                 if "==" in line:#google 的比较特殊，base64编码之后还有内容，但是百度的没有
                     break 
        if isByte:
            monitor_content =("".encode()).join(content_lines[min(useful_lines):max(useful_lines)+1]).decode()
        else:
            monitor_content ="".join(content_lines[min(useful_lines):max(useful_lines)+1])
        Unicode_str=base64.b64decode(monitor_content).decode()#解码必须是完整的开头和结尾
        strdata = etree.HTML(Unicode_str, parser=etree.HTMLParser(encoding='utf-8'))
        extract=strdata.xpath('string(.)').replace("\r\n","")
        print(extract)
        hrefs=strdata.xpath("//@href")#选取名为 href 的所有属性而不管它们所在元素的位置。
        urls=[href for href in hrefs if "baidu.com" not in href]#百度格式的网址提取
        if urls==[]:#选取Google网址，Google的结果不能提取标签的属性，看似有标签实际上没有标签    
            urls=[url.replace("url=","") for url in Unicode_str.split("&") if "url=" in url]  
        urls.append(extract)
        return urls
    else:
        return "这封邮件不是监控邮件"
#oneMailUrls(6345)  

def getContent():
    
      
            
            """收集内容"""
            """ 你的 APPID AK SK """
            APP_ID = '14658509'
            API_KEY = 'C14bCL7NkReQpak382maUYXi'
            SECRET_KEY = '8vWAXHBTmfL3r96PlKIggpwuXwdNl4wz'
            client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
            #[1网址，2标题，3内容，4情感分析items词典，5公司名列表，6评论观点列表，7文章分类，8文章标签]
            #http://linyi.iqilu.com/caijing/2018/1117/4113682.shtml
            #monitor_result=[]
            for news_url in urls:                
                one_monitor=[]
                one_monitor.append(news_url)#①网址
                try:#确保一条新闻具有完整性
                    news=urlopen(news_url,timeout=15)#设置timeout后，urlopen不会一直等待网址响应、也就不会出现卡死现象
                    news_html=news.read()#str类型的网页源码，这条指令和parse冲突，不能同时运行
                    #response = requests.get('http://example.com')
                    #doc = Document(response.text)
                except:
                    one_monitor.append("urlopen_error")
                    monitor_result.append(one_monitor) 
                    success_num +=1
                    print("打开网址错误")
                    continue
                try:#③内容，评论观点抽取最大就3000字
                    news_contents=Document(news_html)    
                    news_title=news_contents.title().strip(" ")[:39].encode("utf-8")#②标题，此处如果用默认的ascii转码、由于超出范围会报错
                    #print(news_title)#则删除空白符（包括'\n', '\r',  '\t',  ' ')
                    one_monitor.append(news_title)
                    news_content=BeautifulSoup(news_contents.summary()).get_text().strip(" ")[:2000].encode("utf-8")
                    #len(news_content)#print(news_content)
                    one_monitor.append(news_content)
                    emotion_content=news_content.decode("utf-8")[:500].encode("utf-8")#要防止str只截取定长字节而有不完整汉字
                    #print(emotion_content)
                except:
                    one_monitor.append("extract_error")
                try:             
                    #print(emotion_content)  #print(u"我很高兴"[:1000])#我很高兴
                    emotion=client.sentimentClassify(emotion_content)["items"]#④情感
                    one_monitor.append(emotion)
                except:
                    one_monitor.append("emotion_error")
                try:#⑤机构名列表
#                    ids = [1,4,3,3,4,2,3,4,5,6,1]
#                    list(set(ids))#结果是重新排序的
                    orgs=[item["item"].encode("utf-8") for item in client.lexer(news_content)["items"] if item["ne"] =="ORG"]
                    one_monitor.append(";".join(list(set(orgs))))
                    #print(";".join(list(set(orgs))))
                except:
                    one_monitor.append("org_error")
                try:#⑥评论观点列表
                    conments=[item['abstract'].encode("utf-8") for item in client.commentTag(news_content)['items']]
                    one_monitor.append(";".join(list(set(conments))))
                    #print(";".join(list(set(conments))))
                except:
                    one_monitor.append("comment_error")
                try:#⑦文章分类
#                    a=[[1,2],[4,3,5]]
#                    [c for b in a for c in b]
                    group=client.topic(news_title, news_content)["item"].values()#[[字典],[字典]]
                    #group=client.topic("对严重失信者，能否限制其发预付卡？法学家谈如何破解预付卡立法瓶颈", news_content)["item"].values()
                    value_list=[dic[u'tag'] for dic_list in group for dic in dic_list]#float类型不能参与join
                    one_monitor.append(u";".join(value_list).encode("utf-8"))
                    #print(u";".join(value_list).encode("utf-8"))
                except:
                    one_monitor.append("topic_error")
                try:#⑧文章标签
                    keyword=client.keyword(news_title, news_content)["items"]#[字典]
                    #keyword=client.keyword("对严重失信者，能否限制其发预付卡？法学家谈如何破解预付卡立法瓶颈", news_content)["items"]
                    key_list=[dic[u'tag'] for dic in keyword]
                    one_monitor.append(u";".join(key_list).encode("utf-8"))                   
                    #print(u";".join(key_list).encode("utf-8"))
                    print("成功%s"%success_num)
                except: 
                    one_monitor.append("keyword_error")
                    error_num +=1
                    print("其中有误%s"%error_num)                                   
                    
                monitor_result.append(one_monitor) 
                success_num +=1
                #time.sleep(1)
                
                if success_num % 200 == 0:#要定期保存，防止功亏一篑
                    with open("./temp/risk_monitoring%s.csv"%index,"w") as reader:
                        writer = csv.writer(reader)
                        writer.writerows(monitor_result)
    except:
        print("出现系统整体错误%s"%(index-1))

with open("./temp/risk_monitoring_new.csv","w") as reader:
    writer = csv.writer(reader)
    writer.writerows(monitor_result)
    

def content_recheck():   
    content_csv=open("./temp/risk_monitoring.csv","rb") 
    content=csv.reader(content_csv)
    type(content)#_csv.reader
    title=next(content)#第一行标题
    type(title),len(title)#(list, 8)
    content_list=[row for row in content]
    type(content_list),len(content_list)#(list, 81)
    type(content_list[1]),len(content_list[1])#(list, 8)
    content_list[10][7]
    
    str_content_list=[r[:4]+[";".join([s.encode("utf-8") for s in eval(r[4])]),
                      ";".join([s.encode("utf-8") for s in eval(r[5])])] for r in content_list]
    with open("./temp/risk_monitoring_str.csv","w") as reader:
        writer = csv.writer(reader)
        writer.writerows(str_content_list)

with open("./temp/long_short.csv","w") as reader:
    writer = csv.writer(reader)
    writer.writerows([[1,1,2],[3,1],[1],[1,2,3,4]])
        
#调用评论观点抽取

    
#参数	类型	描述
#log_id	uint64	请求唯一标识码
#prop	string	匹配上的属性词
#adj	string	匹配上的描述词
#sentiment	int	该情感搭配的极性（0表示消极，1表示中性，2表示积极）
#begin_pos	int	该情感搭配在句子中的开始位置
#end_pos	int	该情感搭配在句子中的结束位置
#abstract	string	对应于该情感搭配的短句摘要
    
""" 调用文章分类 """
client.topic(title, content);

#文章分类 请求参数详情
#
#参数名称	是否必选	类型	说明
#title	是	string	篇章的标题，最大80字节
#content	是	string	篇章的正文，最大65535字节
#文章分类 返回数据参数详情
#
#参数名称	类型	详细说明
#item	object	分类结果，包含一级与二级分类
#+lv1_tag_list	array of objects	一级分类结果
#+lv2_tag_list	array of objects	二级分类结果
#++score	float	类别标签对应得分，范围0-1
#++tag	string	类别标签

""" 调用文章标签 """
client.keyword(title, content);

#文章标签 请求参数详情
#
#参数名称	是否必选	类型	说明
#title	是	string	篇章的标题，最大80字节
#content	是	string	篇章的正文，最大65535字节
#文章标签 返回数据参数详情
#
#参数	是否必须	类型	说明
#items	是	array(object)	关键词结果数组，每个元素对应抽取到的一个关键词
#+tag	是	string	关注点字符串
#+score	是	number	权重(取值范围0~1)

    


emotion=client.sentimentClassify(text2)
emotion["items"]

orgs=client.lexer(text2)
orgs.keys()#[u'log_id', u'text', u'items']
linyi_orgs=[item["item"] for item in orgs["items"] if item["ne"] =="ORG"]
   
    
"""  """
comment=client.commentTag(text2)#调用评论观点抽取
conments=[item['abstract'] for item in comment['items']]
    
#参数	类型	描述
#log_id	uint64	请求唯一标识码
#prop	string	匹配上的属性词
#adj	string	匹配上的描述词
#sentiment	int	该情感搭配的极性（0表示消极，1表示中性，2表示积极）
#begin_pos	int	该情感搭配在句子中的开始位置
#end_pos	int	该情感搭配在句子中的结束位置
#abstract	string	对应于该情感搭配的短句摘要
    
""" 调用文章分类 """
client.topic(title, content);

#文章分类 请求参数详情
#
#参数名称	是否必选	类型	说明
#title	是	string	篇章的标题，最大80字节
#content	是	string	篇章的正文，最大65535字节
#文章分类 返回数据参数详情
#
#参数名称	类型	详细说明
#item	object	分类结果，包含一级与二级分类
#+lv1_tag_list	array of objects	一级分类结果
#+lv2_tag_list	array of objects	二级分类结果
#++score	float	类别标签对应得分，范围0-1
#++tag	string	类别标签

""" 调用文章标签 """
client.keyword(title, content);

#文章标签 请求参数详情
#
#参数名称	是否必选	类型	说明
#title	是	string	篇章的标题，最大80字节
#content	是	string	篇章的正文，最大65535字节
#文章标签 返回数据参数详情
#
#参数	是否必须	类型	说明
#items	是	array(object)	关键词结果数组，每个元素对应抽取到的一个关键词
#+tag	是	string	关注点字符串
#+score	是	number	权重(取值范围0~1)
