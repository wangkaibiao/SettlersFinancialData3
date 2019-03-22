#-*- coding:utf-8 -*-
#import random
from http.server import HTTPServer,BaseHTTPRequestHandler
from json import loads
import base64
import sys
sys.path.append("/media/bdai/LENOVO/SFD_assistant/SettlersFinancialData/d_software_develop/intelligent_device_web/")
sys.path.append("D:\SFD_assistant\SettlersFinancialData\d_software_develop\intelligent_device_web")
#from keras_tf_imagenet import resnet50
from aip import AipImageClassify
from fuzzywuzzy import fuzz,process #Qpython3.2不支持u" "操作
print(fuzz.ratio("Qpython3.2不支持u操作", "不支持Qpython3.2u操作"))
fuzz.token_sort_ratio("Qpython3.2 不 支 持 u 操作", "不 支 持 Qpython3.2 u 操作")
choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
process.extract("new york jets", choices, limit=2)


def image_classify(pic_path="./d_software_develop/intelligent_device_web/image/timg.jpg"):
    """ 你的 APPID AK SK """
    APP_ID = '15354485'
    API_KEY = 'I7GsZGwUaNfAd1NeCwwFEns8'
    SECRET_KEY = 'B7irS89wKXkXxfbFhvyOvt9xSS5Y2MCP'
    
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    
    """ 读取图片 """
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    
    image = get_file_content(pic_path)
    
    """ 调用通用物体识别 """
    #client.advancedGeneral(image);
    
    """ 如果有可选参数 """
    options = {}
    options["baike_num"] = 0
    #options["result_num"] = 3
    
    """ 带参数调用通用物体识别 """
    objects=client.advancedGeneral(image, options)['result']
    return "王娅馨，这%s成像%s；还有%s成像%s"%(
            int(objects[0]['score']*10),objects[0]['keyword'],int(objects[1]['score']*10),objects[1]['keyword'])
    
#image_classify()
    


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print (self.headers['user-agent'])
        if("wangkaibiao" == self.headers['user-agent']):
            length = int(self.headers['content-length'])
            json_data = loads(self.rfile.read(length))#bytes（字节流）类型
            print(type(json_data))
            pic_name=json_data["name"]#.encode()
            pic_data=json_data["image_base64_string"].encode()#transfer to bytes（字节流）类型
            #rand_int=random.randint(1,99)
            image_data = base64.b64decode(pic_data)# 将 base64 字符串解码成图片字节码
            pic_path="./d_software_develop/intelligent_device_web/image/%s.jpg"%pic_name
            with open(pic_path, "wb") as jpg_file:
                # 将字节码以二进制形式存入图片文件中，注意 'wb'
                #/相對路徑，\絕對路徑
                #f.write(pic_data[:rand_int])
                #f.flush()#文件关闭后会自动刷新缓冲区，但有时你需要在关闭前刷新它，这时就可以使用 flush() 方法
                jpg_file.write(image_data)
        #process_result="save pic %s success"%pic_name
        self.send_response(200)
        self.end_headers()
        #self.wfile.write(resnet50(pic_path).encode())#(process_result.encode())
        self.wfile.write(image_classify(pic_path).encode())

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()

