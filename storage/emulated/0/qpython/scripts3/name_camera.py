# -*- coding: utf-8 -*-
try:
    from storage.baidu_cloud import sync
    sync("/storage/emulated/0/qpython/scripts3/","name_camera.py","/scripts3/")
except:
    print("using,testing,2")
    
import androidhelper

droid = androidhelper.Android()
picture_name = droid.dialogGetInput().result
droid.cameraInteractiveCapturePicture('/storage/emulated/0/sl4a/%s.jpg'%picture_name)    