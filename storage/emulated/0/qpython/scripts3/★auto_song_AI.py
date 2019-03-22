#-*- coding:utf-8 -*-
from aip import AipImageClassify	
import os,time
from fuzzywuzzy import process
try:
    import androidhelper as android
except Exception as error:
    print(error)
    

base_path="/storage/emulated/0/sl4a/songs/"#must be self create package ,not system exist
#base_path="./mnt/sdcard/sl4a/"

def play_file(mp3_path=base_path,keywords=["授信","重整"]):
    mp3_list=os.listdir(mp3_path)
    mp3_list=["".join([a+" " for a in mp3_name]) for mp3_name in mp3_list]#把每个字符后面加上空格
    keyword="".join(["".join([A+" " for A in word]) for word in keywords])#把每个字符后面加上空格，同时合并成一条
    one_choice=process.extract(keyword,mp3_list,limit=1)[0][0]
    return mp3_path+"".join(one_choice.split())

#play_file()

while True:
    android.Android().ttsSpeak("i am back")
    time.sleep(1)
    pic_path=base_path+'latest.jpg'
    try:
        android.Android().cameraCapturePicture(pic_path, True)
    except Exception as error:
        print(error)
    time.sleep(1)
    with open(pic_path,"rb") as f:
        image = f.read()
        APP_ID = '15354485'
        API_KEY = 'I7GsZGwUaNfAd1NeCwwFEns8'
        SECRET_KEY = 'B7irS89wKXkXxfbFhvyOvt9xSS5Y2MCP'    
        client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
        options = {}
        options["baike_num"] = 0
        objects=client.advancedGeneral(image, options)['result']
        #recog="%s%s%s%s"%(int(objects[0]['score']*10),objects[0]['keyword'],int(objects[1]['score']*10),objects[1]['keyword'])
        #recog=[objects[0]['keyword'],objects[1]['keyword']]
        recog=[obj['keyword'] for obj in objects]
        print(recog)
        f.flush()#文件关闭后会自动刷新缓冲区，但有时你需要在关闭前刷新它，这时就可以使用 flush() 方法
    os.remove(pic_path)
    android.Android().ttsSpeak(str(recog))
    time.sleep(1)
    android.Android().mediaPlay(play_file(base_path,recog))
    while True:
        time.sleep(1)
        singing=android.Android().mediaIsPlaying().result
        #print(singing)
        if singing==True:
            continue
        else:
            break
    time.sleep(1)
    android.Android().mediaPlayClose()
    time.sleep(1)