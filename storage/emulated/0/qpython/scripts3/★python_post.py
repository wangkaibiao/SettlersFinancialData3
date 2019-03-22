#-*- coding:utf-8 -*-

#import requests
#
#headers = {'user-agent': 'haha'}
#
#with open("D:\SFD_assistant\SettlersFinancialData\d_software_develop\python-web\post-test\\test.jpg", "rb") as f:
#    requests.post('http://127.0.0.1:8080', headers=headers, data=f)
	
import urllib.request #as req
import urllib.parse
from base64 import b64encode
from json import dumps,loads
#dumps把数据类型转换成字符串  dump把数据类型转换成字符串并存储在文件中  
#loads把字符串转换成数据类型  load把文件打开从字符串转换成数据类型
import os,time
try:
    import androidhelper as android
except Exception as error:
    print(error)
    


base_path="./storage/emulated/0/sl4a/"#must be self create package ,not system exist
#base_path="./mnt/sdcard/sl4a/"
url = 'http://192.168.0.105:8080/'
headers = {'user-agent': 'wangkaibiao','Content-Type': 'application/json'}#headers是json的标记


def get_image():
    pic_path=base_path+'latest.jpg'
    try:
        android.Android().cameraCapturePicture(pic_path, True)
    except Exception as error:
        print(error)
    f = open(pic_path,"rb")#encoding="utf-8")
    image = f.read()
    f.close()
    os.remove(pic_path)
    return image


#with open(base_path+"tower.jpg", 'rb') as jpg_file:# 读取二进制图片，获得原始字节码，注意 'rb'
while True:
    android.Android().ttsSpeak(
    	"王娅馨，我又回来啦，你可以把图片放在我的眼前，咱们一起看图")
    time.sleep(5)
    #byte_content = jpg_file.read()
    byte_content = get_image()
    base64_bytes = b64encode(byte_content)# 把原始字节码编码成 base64 字节码
    base64_string = base64_bytes.decode('utf-8')# 将 base64 字节码解码成 utf-8 格式的字符串
    phone="SS"
    pic_dict={"name":phone+time.strftime("%Y%m%d%H%M%S",time.localtime()),
              "image_base64_string":base64_string}
    #pic_dict[]=
    json_data = dumps(pic_dict, indent=2).encode()
    #post的数据必须是bytes格式，而 json.dumps 其实转换为 str，所以需要.encode()进一步转化为bytes进行传输
    # 将字典变成 json 格式，缩进为 2 个空格
    #data = urllib.parse.urlencode({"image_base64_string":base64_string}).encode('utf-8')
    #data参数如果要传必须传bytes（字节流）类型的，如果是一个字典，先用urllib.parse.urlencode()编码。
    #decode_url=urllib.parse.unquote(data.decode('utf-8'))
    #print(loads(json_data)["image_base64_string"])        
    request = urllib.request.Request(url = url,data = json_data,headers = headers)#,method = 'POST'    
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')    
    print(html)
    android.Android().ttsSpeak(html)
    
    time.sleep(5)
    
