# coding: utf-8

import os
from datetime import datetime
from time import sleep
from threading import Thread
import mp3play


class FileNotFound(Exception):
    pass


class Piano:
    def __init__(self):
        self.t_list = []
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.sound_dir = os.path.join(base_dir, 'res', 'sound')

    def __play_voice(self, voice):
        """播放"""

        # 检查文件是否存在
        filename = os.path.join(self.sound_dir, '{}.mp3'.format(voice))
        if not os.path.exists(filename):
            raise FileNotFound('文件不存在: {}'.format(filename))

        # 加载文件
        clip = mp3play.load(filename)
        # 播放
        clip.play()
        # 每个音源文件的时长都是3秒，所以播放3秒
        sleep(3)
        # 结束播放
        clip.stop()

    def __add_thread(self, filename):
        """添加线程"""
        t = Thread(target=self.__play_voice, args=(filename,))
        self.t_list.append(t)

    def play(self, music_list):
        """
        启动所有线程, 按计划播放
        :param music_list: 钢琴谱 (音源文件名, 下一个音播放前的等待时间)
        """
        for music in music_list:
            self.__add_thread(music[0])

        for index, t in enumerate(self.t_list):
            print('[{}] {}'.format(datetime.now(), music_list[index][0]))
            t.start()
            # 设置下一个音播放前的等待时间
            sleep(music_list[index][1])


# class Piano:
#     def __init__(self):
#         base_dir = os.path.dirname(os.path.dirname(__file__))
#         sound_dir = os.path.join(base_dir, 'res', 'sound')
#
#         # 加载所有音源文件
#         print('waiting...')
#         self.clip_dict = {}
#         all_file = os.listdir(sound_dir)
#
#         for f in all_file:
#             filename = os.path.join(sound_dir, f)
#             clip = mp3play.load(filename)
#             voice_name = f.replace('.mp3', '')
#             self.clip_dict.update({
#                 voice_name: clip
#             })
#         print('finally!\n')
#
#     def __play_voice(self, voice):
#         """播放"""
#
#         # 获取对象
#         clip = self.clip_dict[voice]
#         # 播放3秒
#         clip.play()
#         sleep(3)
#         clip.stop()
#
#     def play_one(self, music):
#         t = Thread(target=self.__play_voice, args=(music[0],))
#         t.start()
#         sleep(music[1])
#
#     def play_all(self, music_list):
#         """
#         启动所有线程, 按计划播放
#         :param voice: 钢琴谱 (音源文件名, 下一个音播放前的等待时间)
#         """
#         for music in music_list:
#             self.play_one(music)