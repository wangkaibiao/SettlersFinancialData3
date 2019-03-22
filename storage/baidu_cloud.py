#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bypy,第一次运行时需要授权，只需跑任何一个命令（比如 bypy info）然后跟着说明（登陆等）来授权即可。
授权只需一次，一旦成功，以后不会再出现授权提示.
更详细的了解某一个命令：bypy help <command>
显示在云盘（程序的）根目录下文件列表：bypy list
把当前目录同步到云盘：bypy syncup  or bypy upload  
把云盘内容同步到本地来：bypy syncdown  or bypy downdir /
比较本地当前目录和云盘（程序的）根目录（个人认为非常有用）：bypy compare
更多命令和详细解释请见运行bypy的输出。

调试
运行时添加-v参数，会显示进度详情。
运行时添加-d，会显示一些调试信息。
运行时添加-ddd，还会会显示HTTP通讯信息（警告：非常多）
经验分享,请移步至wiki，方便分享/交流。
"""
from bypy import ByPy#,gui
import os,sys,psutil


"""-------------------------------------------------------------------------"""
_paths=["/media/sfd/1CEE36D0EE36A1C6/core/","/media/sfd/LENOVO/SFD_assistant/core/"]
for _path in _paths:
    if os.path.exists(_path):
        base_path=_path
externalPaths=[base_path + 'basic_linux' ,
               base_path + 'intelligent_device' ,
               base_path + 'knowledge_continue' ,
              ]
#os.listdir(externalPaths[0])

"""-------------------------------------------------------------------------"""
def make_paths(paths=[]):#用于初始化开发环境
    if paths:
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        return "创建成功"
    else:
        return "请输入路径列表"
#make_paths(externalPaths) 
        
"""-------------------------------------------------------------------------""" 
def test():
    bp=ByPy()
    bp.list("basic_linux/") # or whatever instance methods of ByPy class
    bp.syncup(base_path)
    bp.syndown("/apps/bypy",base_path)
    bp.downfile("basic_linux/wps-office_10.1.0.6634_amd64.deb",externalPaths[0])
    bp.downfile("basic_linux/can_google.crx",externalPaths[0])   
    #gui.BypyGui()

"""-------------------------------------------------------------------------"""
def qpython_sync(current_dir="/*/",file_name="*.py"):
    move_path="/run/user/1000/gvfs/mtp:host=%5Busb%3A001%2C002%5D/Internal storage/qpython"
    sourceFile=os.getcwd()+"/storage/emulated/0/qpython"+current_dir+file_name
    targetFile=move_path+current_dir+file_name
    if os.path.isfile(sourceFile): 
        with open(sourceFile, "rb") as source:
            with open(targetFile, "wb") as copy:
                copy.write(source.read()) 
        print("copy success")
        



