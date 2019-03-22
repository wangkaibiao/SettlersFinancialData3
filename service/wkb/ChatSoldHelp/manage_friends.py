# -*- coding: utf-8 -*-
import sys,os
sys.path.append(os.getcwd()+"/service")
import itchat
import re,csv,time,random
from itchat.content import *

#通过如下命令登陆，即使程序关闭，一定时间内重新开启也可以不用重新扫码。
#在手机端点击下线才下线
itchat.auto_login(hotReload=False)

#显示消息
@itchat.msg_register(itchat.content.TEXT)
def msg(msg):
    print(msg['Text'])
    
itchat.run()

#获取好友基础信息
friends=itchat.get_friends(update=True)#每次执行都获取最新的备注名
print(len(friends))

def pho_name_dict():
    friends=itchat.get_friends(update=True)
    pho_name={"手机号":"微信信息"}#生成本次登录产生的新朋友编号
    for friend in friends:
        info=friend.RemarkName+friend.NickName+friend.Signature
        pho_num=re.findall(r"1\d{10}",info)
        if pho_num != []:
            for pho in pho_num:
                pho_name[pho]=info
    return pho_name
    
print(len(pho_name))
#本质为列表类型，<class 'itchat.storage.templates.ContactList'>

#基础信息维度
me=friends[0]#字典类型
for item in me:
    print (item)
    print( me[item])
    
#修改备注
it=friends[1]
it.set_alias(alias=it.RemarkName+'开')
it.set_alias(alias=it.RemarkName.lstrip('待包1')+'开标2')
it.RemarkName.lstrip('儿')#删除指定字符串
#{'Ret': 0, 'RawMsg': '请求成功', 'ErrMsg': '请求成功'}}>
it.alias#实质上是修改的备注it.RemarkName
print("钢材" in it.RemarkName )#True

#观察当前分组计数
def group_dict():#生成初始类计数字典
    group_str="{"
    for name in ["内包","外包","他包","待包","潜在","开标","城东","同事","同行"]:
        for i in range(10):
            if i==9 and name=="同行":
                group_str+='"%s%s":0,"无群标签":0}'%(name,i)
            else:
                group_str+='"%s%s":0,'%(name,i)
    return eval(group_str)

group_count=group_dict()
 
no_label=[]
for friend in friends:
    if "同事" in friend.RemarkName:
        continue
    elif "同行" in friend.RemarkName:
        continue
    else:
        count=0
        for name in group_count.keys():
            if name in friend.RemarkName:
                group_count[name]+=1
                #break#去除多群标签的名影响
            else:
                count+=1
        if count==91:
            group_count["无群标签"]+=1
            no_label.append(friend.RemarkName)
            
group_count
no_label

repeat_group={"含多个群标签的名":"重复数"}
for friend in friends:
    repeat=0
    for name in group_count.keys():
        if name in friend.RemarkName:
            repeat+=1
    if repeat>1:
        repeat_group[friend.RemarkName]=repeat
repeat_group        


#修改分组达到每组198人
init_count={k:v for k,v in group_count.items() if 350>v>0}#635-526
#init_count={'他包1': 229,'内包1': 177,'内包2': 158,'内包3': 5,
#            '城东1': 146,'外包1': 157,'外包2': 10,'开标1': 195,
#            '开标2': 63,'待包1': 330,'潜在1': 7,'潜在2': 3,
#            '潜在3': 81,'潜在4': 43,'潜在5': 31,'潜在6': 28}
#16个标签，'无群标签':911 
init_count_key=['待包1','他包1', '开标1', '内包1', '内包2', '外包1', '城东1'
       , '潜在3', '开标2', '潜在4', '潜在5', '潜在6', '外包2', '潜在1'
       , '内包3', '潜在2']#按顺序显示，保证尽量集中
#for g in g_nam:
#    print(g)
       
#init_count0={'待包1':330, '他包1':229, '开标1':195, '外包1':157
#            , '城东1':146, '潜在3':81,  '开标2':63
#            , '潜在4':41, '潜在5':33, '潜在6':28,  '外包2':10
#            , '潜在1':8, '潜在2':3}#15个标签，'无群标签':1420, 
#2843个好友需要15个标签就够了
for friend in friends:
    print(friend.RemarkName)        
#    if ('同事' or '同行')  in friend.RemarkName:#这个只能判断“同事”不能判断“同行”
#        print('同事' or '同行')
    if '同事' in friend.RemarkName:
        print('同事')
    elif '同行' in friend.RemarkName:
        print('同行')
    else:
        count=0
        for name1 in init_count_key:
            #在的话：超量就修改，不超量就停止;不在的话：计数，
            if name1 in friend.RemarkName:
                if init_count[name1]>200:
                    for name2 in init_count_key:
                        if init_count[name2]<200:
                            time.sleep(random.randint(7,10))
                            #删除指定字符串
                            old=friend.RemarkName
                            #type(old)
                            new=old.replace(name1,"")+name2
                            friend.set_alias(alias=new)
                            init_count[name1]+= -1
                            init_count[name2]+=  1
                            break
                else:
                    break
            else:
                count+=1
        if count==16:#如果全都不在组
            time.sleep(random.randint(7,10))
            for name1 in init_count_key:
                if init_count[name1]<200:
                    friend.set_alias(alias=friend.RemarkName+name1)
                    init_count[name1]+=  1
                    break

                    
                    
            
        
        
        

    
