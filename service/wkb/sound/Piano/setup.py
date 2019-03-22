# coding: utf-8
import os
import platform


# 获取python版本和操作系统类型
version = platform.python_version_tuple()
system = platform.system()

# 拼接命令
if version[0] == '3':
    if system == 'Windows':
        command = 'pip install'
    else:
        command = 'pip3 install'
else:
    command = 'pip install'

command += ' mp3play'
os.system(command)
