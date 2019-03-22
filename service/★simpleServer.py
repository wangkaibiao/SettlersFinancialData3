#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 20:32:35 2019 @author: sfd
"""
from http.server import HTTPServer,BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    '''处理请求并返回页面'''

    # 页面模板
    Page = '''
<!DOCTYPE html>
<html lang="ZH-CN">
<head>
  <meta charset="utf-8">
  <title>web RTC 测试</title>
  <style>
    .booth {
      width:400px;
     
      background:#ccc;
      border: 10px solid #ddd;
      margin: 0 auto;
    }
  </style>
</head>
<body>
  <div class="booth">
    <video id="video" width="400" height="300"></video>
    <button id='tack'> snap shot</button>
    <canvas id='canvas' width='400' height='300'></canvas>
    <img id='img' src=''>
  </div>
 
 
  <script>
    var canvas = document.getElementById('canvas'),
        snap = document.getElementById('tack'),
        img = document.getElementById('img'),
        vendorUrl = window.URL || window.webkitURL;
// 想要获取一个最接近 1280x720 的相机分辨率
var constraints = { audio: true, video: { width: 600, height: 500 } }; 

navigator.mediaDevices.getUserMedia(constraints)
.then(function(mediaStream) {
  var video = document.querySelector('video');
  video.srcObject = mediaStream;
  video.onloadedmetadata = function(e) {
    video.play();
  };
}).catch(function(err) { console.log(err.name + ": " + err.message); }); // 总是在最后检查错误
    
    snap.addEventListener('click', function(){
    
        //绘制canvas图形
        canvas.getContext('2d').drawImage(video, 0, 0, 400, 300);
        
        //把canvas图像转为img图片
        img.src = canvas.toDataURL("image/png");
        
    })
  </script>
</body>
</html>
    '''

    # 处理一个GET请求
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(self.Page.encode())

#----------------------------------------------------------------------

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()