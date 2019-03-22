#import androidhelper,sys

#droid = androidhelper.Android()
#droid.cameraCapturePicture('/storage/emulated/0/autoqpython.jpg')
#"the,path,must,be,/storage/emulated/0/,if,/sdcard,not,exist"
#droid.cameraStopPreview()
#sys.exit(1)
#droid.cameraInteractiveCapturePicture('/sdcard/qpython.jpg')
import androidhelper 
import time 

droid = androidhelper.Android() 
for i in range(3): 
    temp = str(i) 
    path = '/storage/emulated/0/picscript/' 
    path += time.strftime("%B-%_e-%_I-%M-") 
    path += temp 
    path += '.png' 
    droid.cameraCapturePicture(path, True) 