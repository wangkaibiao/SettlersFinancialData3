#-*-coding:utf8;-*-
#qpy:3
#qpy:console

print("This is console module")
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
    res=android.Android().scanBarcode()
    recog=[res.result["extras"]["SCAN_RESULT"].strip('儿童歌曲-')]
    android.Android().ttsSpeak(str(recog))
    time.sleep(1)
    play_song=play_file(base_path,recog)
    print(play_song)
    android.Android().mediaPlay(play_song)
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