# -*- coding: utf-8 -*-
try:
    from storage.baidu_cloud import qpython_sync
    qpython_sync("/scripts3/","★test_sync.py")
except:
    print("using,testing,2")

try:
    import androidhelper
    droid = androidhelper.Android()
    droid.makeToast("导入androidhelper成功")
except:
    print("不存在androidhelper库")
"""--------------------------------------------------------------------------"""