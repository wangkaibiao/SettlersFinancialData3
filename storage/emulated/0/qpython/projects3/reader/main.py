#-*-coding:utf8-*-
#qpy:console
"""This script shows how to use SL4A APIs in android"""

import androidhelper,os,time


droid = androidhelper.Android()

#def speak(choice):
#  result = droid.ttsSpeak(choice)
#  return result.error is None

def alert_dialog_with_buttons():
  title = "閱讀模式"
  message = ("繼續播放、隨機播放、從頭播放")
  droid.dialogCreateAlert(title, message)
  droid.dialogSetPositiveButtonText('continue')
  droid.dialogSetNegativeButtonText('random')
  droid.dialogSetNeutralButtonText('restart')
  droid.dialogShow()
  response = droid.dialogGetResponse().result
  return response['which']
  #response['which'] in ('positive', 'negative', 'neutral')

#print(alert_dialog_with_buttons())

def alert_dialog_with_list(text_file):
  title = "閱讀文件目錄"
  droid.dialogCreateAlert(title)
  droid.dialogSetItems(text_file)
  #['foo', 'bar', 'baz']
  droid.dialogShow()
  response = droid.dialogGetResponse().result  
  #droid.dialogGetSelectedItems()
  return response

base_dir="./storage/emulated/0/qpython/projects3/reader/"
text_file=[txt for txt in os.listdir(base_dir) if ".txt" in txt]
#print(text_file)
index=alert_dialog_with_list(text_file)
txt_name=text_file[index["item"]]
file_path=base_dir+txt_name
print(file_path)
try:
    from memory import *
    start=m_dic
except:
    start={}

def reader():
    file=open(file_path,encoding="utf-8")
    reader=file.read().split("。")
    print(len(reader))
    choice=alert_dialog_with_buttons()
    if choice=='positive':
        try:
            start_index=start[txt_name]
        except:
            start_index=0
            start[txt_name]=0
    elif choice=='negative':
        import random
        start_index=random.randint(0,len(reader))
    else:
        start_index=0
    print(len(reader[start_index:]))  
    for knowledge in reader[start_index:]:
    #while True:
      #print(len(knowledge))
      #speak(knowledge)
      #droid.ttsSpeak(knowledge)
      print(start_index)
      droid.ttsSpeak(knowledge)
      start_index += 1
      if (start_index % 3 ==0) and (choice=='positive'):
          start[txt_name]=start_index
          with open(base_dir+"memory.py","w",encoding="utf-8") as memory:
              memory.write('m_dic=%s'%str(start))
      while True:
          if droid.ttsIsSpeaking().result==False:
              break
          else:
              time.sleep(0.1)
              continue

if __name__ == '__main__':
  reader()