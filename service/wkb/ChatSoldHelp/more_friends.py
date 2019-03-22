# -*- coding: utf-8 -*-

import re,csv,sys,time,itchat,os
from itchat.content import *

#通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。
#在手机端点击下线才下线
itchat.auto_login(hotReload=False)

#获取好友基础信息
friends=itchat.get_friends(update=True)
print(len(friends))


##信息分析
#wkb=friends[1]
#print("18253995666" in wkb.RemarkName)#True
#
##手机号匹配 
#text="s127362839138717648372936 1839306271g82732973 28649703767"  
#m=re.findall(r"1\d{10}",text)#['12736283913', '17648372936']
#匹配过的不再重复用，比如13871764837不会被匹配出来

def pho_user_dict():
    friends=itchat.get_friends(update=True)
    pho_user={"手机号":"微信UserName"}#生成本次登录产生的新朋友编号
    for friend in friends:
        pho_num=re.findall(r"1\d{10}",
                       friend.RemarkName
                       +friend.NickName
                       +friend.Signature)
        if pho_num != []:
            for pho in pho_num:
                pho_user[pho]=friend.UserName
    return pho_user
    
pho_user1=pho_user_dict()           
print( len(pho_user))#1937
print(pho_user.keys())

csvfile = open('D:\\PythonProject\\ChatSoldHelp\\pho_nums.csv',
               'w',newline='')
#w建立文件,r读取文件，wb表示以二进制建立文件，后续容易出错
#newline=''表示行与行之间没有空行
writer = csv.writer(csvfile)#打开写入功能
writer.writerow(["header_手机号"])#只写入到单行
pho_list=[[pho] for pho in pho_user.keys()]
writer.writerows(pho_list)#批量写入，但对象必须是列表中的列表
csvfile.close()#关闭过程

#好友档案MySQL或者csv
chats = open('D:\\PythonProject\\ChatSoldHelp\\chat_database.txt','w',encoding='utf-8')
王开标={"微信":["王","开","标"]}
chats.write(str(pho_name))
chats.close()

chat_history=open('D:\\PythonProject\\ChatSoldHelp\\chat_database.txt','r')
type(chat_history)
wkb=chat_history.read()
chat_history.close()
wkb=eval(wkb)
wkb["测试itchat群消息【网名】中国民生银行王开标"][0]#['王', '开', '标']→'开'


#有针对性的交流
contacts=['18253995666','18253993666','18253905066','13953999999']
def send_person(pho_list=['18253995666','13953999999'],s_msg=u"王开标你好"):
    pho_user=pho_user_dict() 
    for pho_num in pho_list :
        time.sleep(2)
        try:
            itchat.send_msg(s_msg,toUserName=pho_user[pho_num])                     
#        print(pho_user[pho_num])
        #msg必须是Unicode类型的，否则报ASCII错误           
        except:
            print( "none")
        
send_person()       
#聊天室
chatrooms=itchat.get_chatrooms(update=True)
#保存在通讯录或当前收到信息的群
print( len(chatrooms))#35
print( len(chatrooms[0]))#33
print( u'\u6c11\u751f\u94f6\u884c\u6b22\u8fce\u60a8')
groups = itchat.search_chatrooms(name = u"测试")#根据关键字搜索
for group in groups:
    print( group.NickName)
#城东支部
#城东支行金银提升小组
#城东支行党支部
for item in groups[1] :
    print( item)
    print( groups[1][item])
    
def send_group(msgContentList, groupNickName):
    if len(msgContentList) == 0:
        print( 'No msg need send')
        return True
    groups = itchat.search_chatrooms(name = groupNickName)
    #print( groups)
    groupName = groups[0]['UserName']
    for msgContentItem in msgContentList:
        itchat.send(msgContentItem, toUserName = groupName)
        
send_group(["聊","记","录"],"测试")

#开始运行

#预设要使用的外部变量        
pholist=['18253995666','13953999999']
smsg=u"王开标Google" 
msglist=["聊","liap","5"]
groupNick="t群消"       
#自动保存聊天记录，同时便于以后训练分析
chat_history=open('D:\\PythonProject\\ChatSoldHelp\\test_chat_database.txt'
                  ,'r',encoding='utf-8')
wkb=chat_history.read()
chat_history.close()
chat_s=eval(wkb)
#chat_s={"AAA微信名":[["聊","记","录"],["时刻","类型","内容"]]}
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP
                      , SHARING, RECORDING, ATTACHMENT, VIDEO]
                      ,isFriendChat=True, isGroupChat=True
                      , isMpChat=True)
def save_content(msg):#msg为字典类型，且不能随便加参数
    #print(msg)
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S"
                                 , time.localtime())
    try:
        msg_from = itchat.search_friends(
                                         userName=msg['FromUserName']
)['RemarkName']#保证不变和唯一性
    except:
        msg_from = itchat.search_chatrooms(
                                           userName=msg['FromUserName']
)['NickName'] + '【网名】' + msg['ActualNickName']
    print(msg_from)
    if msg['Type'] == 'Text' or msg['Type'] == "Friends":
        b=[msg_time_rec,msg['Type'],msg['Text']]
        print(b)
        try:
            a=chat_s[msg_from]
            chat_s[msg_from]=a+[b]            
        except:
            chat_s[msg_from]=[b]
    elif msg ['Type'] == 'Map':
        x,y,loca,point = re.search('<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*poiname=\"(.*?)\"', msg['OriContent']).group(1,2,3,4)
        b=[msg_time_rec,msg['Type'],loca.__str__()+point.__str__()]
        print(b)
        try:
            a=chat_s[msg_from]
            chat_s[msg_from]=a+[b]            
        except:
            chat_s[msg_from]=[b]       
    elif msg['Type'] == 'Card':
        b=[msg_time_rec,msg['Type'],msg['RecommendInfo']['NickName']]
        print(b)
        try:
            a=chat_s[msg_from]
            chat_s[msg_from]=a+[b]            
        except:
            chat_s[msg_from]=[b]         
    elif msg['Type'] == 'Sharing':
        b=[msg_time_rec,msg['Type'],msg['Text']]
        print(b)
        try:
            a=chat_s[msg_from]
            chat_s[msg_from]=a+[b]            
        except:
            chat_s[msg_from]=[b]        
#    elif msg['Type'] == "Attachment" or msg['Type'] == "Video" or msg['Type'] == 'Picture' or msg['Type'] == 'Recording':
    else:
        b=[msg_time_rec,msg['Type'],msg['FileName']]
        print(b)
        try:
            a=chat_s[msg_from]
            chat_s[msg_from]=a+[b]            
        except:
            chat_s[msg_from]=[b]      
    now= time.localtime(time.time())#获取当前时间结构
    if  now[4]%3==0:#每隔3分钟保存一次，但是当前得有会话发生
        chats = open('D:\\PythonProject\\ChatSoldHelp\\test_chat_database.txt'
                     ,'w',encoding='utf-8')
        #在Windows下Python使用open()函数打开文件时会默认使用gbk解码
        #，即使文件本身存储为UTF-8格式。指定解码方式打开避免解码错误
        chats.write(str(chat_s))
        chats.close()
    if msg['Text']=="orderyousendperson":
        print("orderyousendperson")
        send_person(pholist,smsg)#不会被收集记录，可以调用外部预设变量
    elif msg['Text']=="orderyousendgroup":
        send_group(msglist, groupNick)#不会被收集记录


itchat.run()#托管微信让其自动运行

#找到话题并匹配到喜欢的人
#来话自动匹配营销库并提示推荐
  




