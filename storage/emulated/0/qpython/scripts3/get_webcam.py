# -*- coding: utf-8 -*-

#import sys
#sys.platform="linux2"
import urllib.request as rq

pic=rq.urlopen("http://192.168.0.105:8080/?n1=wkb7890&n2=%E7%B6%B2%E9%96%8B%E6%A8%99")
#("http://192.168.0.104:8080/stream")
respon=pic.read()
print(respon)
#print(help(rq))

## 在程序所在文件夹下，将图片以二进制形式写入名字为name的文件中
#with open('name1.jpg','wb') as f:
#    f.write(respon)
#
#
#url = 'http://placekitten.com/g/500/600'
#response = urllib.request.urlopen(url)
#img = response.read()
#
## 在程序所在文件夹下，将图片以二进制形式写入名字为name的文件中
#with open('name','wb') as f:
#    f.write(img)
#    
#"""先生成Request对象req，然后使用urlopen()读取req。 
#这里生成Request对象的好处是可以通过Request对象添加data、header信息（访问post网页、伪装浏览器）。"""    
#req = urllib.request.Request(url)
#response = urllib.request.urlopen(req)
#img = response.read()    
