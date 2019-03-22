#-*- coding:utf-8 -*-
import soundmeter,os


def test():
    cmd ="soundmeter --collect --seconds 1"
    while True:
        maxsound=os.popen(cmd).readlines()[5]#把执行Linux命令的结果传递给变量
        print(maxsound)
