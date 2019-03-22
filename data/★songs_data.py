# -*- coding: utf-8 -*-
import requests,time,random
from selenium import webdriver


def get_source():
    browser = webdriver.Chrome()
    datas=[]
    for a in range(11,1000):
        page_num="0"*(3-len(str(a)))+str(a)
        songs_list_url="https://api.7mtt.cn/album/%s/songs"%page_num    
        browser.get(songs_list_url)
        time.sleep(random.randint(1,2))
        #pageSource = browser.page_source
        dic=browser.find_element_by_xpath('/html/body/pre').text
        dic1=eval(dic)
        datas.extend(dic1["data"])
        if a%10==0:#20%10
            with open("/media/bdai/LENOVO/SFD_assistant/object_data/song_datas.txt","wb") as dt:
                dt.write(str(datas).encode())
        #browser.close()


def download_mp3():
    song_datas=eval(open("/media/bdai/LENOVO/SFD_assistant/object_data/song_datas.txt","r").read())
    len(song_datas)
    song_name_url=[[song['songName'],song['songFileUrl']] for song in song_datas]
    #print(len(song_name_url),len(set(song_name_url)))
    song_name=[]
    #len(song_name)
    error_song=[]
    #song_name_url.index(['相信孩子', 'https://qiniuuwmp3.7mtt.cn/lic_BypH7fplAKsLKZmicD3E6B8T.mp3'])
    count=0
    for name_url in song_name_url[:]:
        count +=1
        #mp3_url = 'https://qiniuuwmp3.7mtt.cn/Fg0QUSBPohvUM_ZPtMmJCYbqb9mY.mp3' 
        #time.sleep(random.randint(1,3))
        if name_url[0] not in song_name:
            song_name.append(name_url[0]) 
            try:
                song=requests.get(name_url[1]) 
                with open("/media/bdai/LENOVO/SFD_assistant/object_data/故事绘本/%s.mp3"%name_url[0], "wb") as code:
                    code.write(song.content)
            except Exception as error:
                error_song.append(name_url[0])
                print(error)
        if count % 1000 ==0:
            with open("/media/bdai/LENOVO/SFD_assistant/object_data/song_name.txt","wb") as dt:
                dt.write(str(song_name).encode())

