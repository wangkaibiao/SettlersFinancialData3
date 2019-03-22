import androidhelper,numpy
droid = androidhelper.Android()
#droid.makeToast(str(droid.getRunningPackages()))
#print(str(droid.ActivityManager()))#.getMemoryInfo
res=droid.scanBarcode()
#res=droid.recognizeSpeech()


print(
	res.result["extras"]["SCAN_RESULT"])