import androidhelper as android
import os
import time
#import BaseHTTPServer
from http.server import *
#from SocketServer import ThreadingMixIn
from socketserver import * 
HOST_NAME = ''
PORT_NAME = 8080
 
PAGE_SOURCE = '''
<html>
<head>
<title>MJPEG</title>
</head>
<body>
<h1>Camera</h1>
<img src=/stream />
</body>
</html>
'''
 
class ThreadServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass
 
class StreamerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if (self.path == '/' or not self.path):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(PAGE_SOURCE)
 
        elif (self.path == '/stream'):
            self.send_response(200)
            self.send_header('Connection', 'close')
            self.send_header('Expires', '0')
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, pre-check=0, post-check=0, max-age=0')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=BOUNDARYSTRING')
            self.end_headers()
 
            while True:
                image = get_image()
                self.send_header('Content-Type', 'image/jpeg')
                self.send_header('Content-Length', str(len(image)))
                self.end_headers()
                self.wfile.write(image)
                self.wfile.write("\r\n--BOUNDARYSTRING\r\n")
                time.sleep(1)
 
def get_image():
    android.Android().cameraCapturePicture('/storage/emulated/0/sl4a/latest.jpg', True)
    f = open('/storage/emulated/0/sl4a/latest.jpg')
    image = f.read()
    f.close()
    os.remove('/storage/emulated/0/sl4a/latest.jpg')
    return image
 
if __name__ == '__main__':
    server = ThreadServer((HOST_NAME, PORT_NAME), StreamerHandler)
    server.serve_forever()
