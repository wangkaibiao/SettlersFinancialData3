#-*-coding:utf8;-*-
#qpy:3
#qpy:console
print("This is console module")
import os,time
try:
    import androidhelper as android
except Exception as error:
    print(error)

    
base_path="/storage/emulated/0/sl4a/songs/"#must be self create package ,not system exist
#base_path="./mnt/sdcard/sl4a/"

while True:
    #android.Android().ttsSpeak("i am back")
    time.sleep(1)
    res=android.Android().scanBarcode()
    pic_path=base_path+res.result["extras"]["SCAN_RESULT"]+".mp3"
    print(pic_path)
    time.sleep(1)
    android.Android().mediaPlay(pic_path)
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