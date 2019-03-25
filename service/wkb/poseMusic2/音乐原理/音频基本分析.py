# -*- coding: utf-8 -*-
"""
Python声音处理入门【注：本文加入了译者的理解，并非严谨的译作，仅供参考。】，
原文Basic Sound Processing with Python描述了怎样在Python中通过pylab接口对声音进行基本的处理。

音频 属性详解(涉及采样率、通道数、位数、比特率、帧等) - 郎涯工作室 - 
CSDN博客: https://blog.csdn.net/aoshilang2249/article/details/38469051

简谱1、2、3、4、5、6、7分别对应的五线谱音高为do、re、mi、fa、so、la、si（ti）。
c、d、e、f、g、a、b为唱名，也是由do、re、mi、fa、so、la、si变过来的，依次对应，比如do和c在钢琴上弹的是一个键。
简谱表示音的高低的基本符号，用七个阿拉拍数字标记。为了标记更高或更低的音，则在基本符号的上面或下面加上小圆点。
在简谱中，不带点的基本符号叫做中音；在基本符号上面加上一个点叫高音；加两个点叫倍高音；加三个点叫超高音。
在基本符号下面加一个点叫低音；加两个点叫倍低音；加三个点叫超低音。
"""
import sys
sys.path.append("/media/sfd/LENOVO/SFD_assistant/SettlersFinancialData2/service/sound")
import os
from pylab import*
from scipy.io import wavfile
import pydub#sudo apt install ffmpeg  才能正常读取mp3
from pydub.playback import play 
import numpy as np


def plot_sound():
    sampleMumber = len(channel1)#总采样点数  n
    #python自身不支持播放声音，假如你想在python中回放声音，参考pyalsaaudio(Linux)或PyAudio。    
    channel1_f = channel1 / (2.**15)
    #这表示原始声压值在wav文件中一一映射到区间[-2^15, 2^15 -1]。我们把声压值归一化，即映射到区间[-1, 1):
    duration= sampleMumber / sampFreq#结合采样率sampFreq可得信号持续时长，单位是秒
    #绘制音调图,以时间(单位ms)为x轴，声压值为y轴，绘制音调图。先创建时间点数组
    timeArray = arange(0, sampleMumber) / sampFreq   * 1000 #每个采样发生的第毫秒时刻
    plot(timeArray, channel1_f, color='k')
    ylabel('Amplitude')
    xlabel('Time (ms)')


def read(file_path='/service/sound/Piano/res/sound/E3.mp3',_format="mp3",s=100,e=300):#读取mp3
    audiofile = pydub.AudioSegment.from_file(os.getcwd()+file_path,_format)[s:e]#截取音频文件多少毫秒  
    play(audiofile)#播放截取的音频文件
    #play(audiofile[100:300])
    #audiofile = pydub.AudioSegment.from_file(os.getcwd()+'/service/sound/pianopi/bowl.wav',format="wav")
    #读取wav文件 ,下载文件440_sine.wav，文件中加入了基频(F0)为440Hz的噪声。    
    sampFreq=audiofile.frame_rate#44100
    #以int16或int32（32位wav）格式读入wav文件,16位.wav文件对应int16，32位.wav文件对应int32，不支持24位.wav。    
    snd_int=np.frombuffer(audiofile._data, np.int16)#转换成数字矩阵    
    #snd_int.dtype#查看文件类型,dtype('int16')
    #snd_int.shape#查看文件的通道数和采样点数,(271872,) 但是看不出
    channels = audiofile.channels
    #按声道分开
    if channels==1:
        return sampFreq , snd_int , "None"
    else:
        return sampFreq , snd_int[0::channels] , snd_int[1::channels]#[start:end:step]
    
sampFreq,channel1,channel2=read('/service/sound/Piano/res/sound/A7.mp3',"mp3",100,120)
plot_sound() 


def pinpu():    
    #绘制频谱图,频谱图也是一种很有用的图形表示方式。用函数fft对声音进行快速傅立叶变换（FFT），得到声音的频谱。
    #让我们紧跟技术文档的步伐，得到声音文件的功率谱：    
    p = fft(channel1_f)         #执行傅立叶变换
    #技术文档中指定了执行fft用到的抽样点数目，我们这里则不指定，默认使用信号n的采样点数。
    #不采用2的指数会使计算比较慢，不过我们处理的信号持续时间之短，这点影响微不足道。
    nUniquePts = ceil((sampleMumber+1)/2.0)
    p = p[0:int(nUniquePts)]
    p = abs(p)
    #fft变换的返回结果为复合形式，比如复数，包含幅度和相位信息。获取傅立叶变换的绝对值，得到频率分量的幅度信息。
    p = p / float(sampleMumber)    #除以采样点数，去除幅度对信号长度或采样频率的依赖
    p = p**2            #求平方得到能量
    #乘2（详见技术手册）
    #奇nfft排除奈奎斯特点
    if sampleMumber % 2 > 0:       #fft点数为奇
        p[1:len(p)] = p[1:len(p)]*2
    else:               #fft点数为偶
        p[1:len(p)-1] = p[1:len(p)-1] * 2
    
    freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / sampleMumber)
    plot(freqArray/1000, 10*log10(p), color='k')
    xlabel('Freqency (kHz)')
    ylabel('Power (dB)')    
    #绘制的频谱图如下所示。注意图中y轴是能量的对数10*log10(p)，单位分贝；x轴是频率/1000，单位kHz。
    
    #为了检验计算结果是否等于信号的能量，我们计算出信号的均方根rms。广义来说，可以用rms衡量波形的幅度。
    #如果直接对偏移量为零的正弦波求幅度的均值，它的正负部分相互抵消，结果为零。
    #那我们先对幅度求平方，再开方（注意：开方加大了幅度极值的权重？）
    rms_val = sqrt(mean(channel1_f**2))#0.0615000626299
    #信号的rms等于总能量的平方根，那么把fft在所有频率上的能量值相加然后求平方根，应该等于rms。
    sqrt(sum(p))#0.0615000626299
    
    
def patch():
    sound_path=os.getcwd()+'/service/sound/Piano/res/sound/'
    sounds=os.listdir(sound_path)
    feature100_610={}
    for sound in sounds:
        sampFreq,channel1,channel2=read('/service/sound/Piano/res/sound/'+sound,"mp3")
        #len(channel1)#22491/17=1323
        #np.array(range(12)).reshape(3,-1).sum(axis=1).shape  #(3,)
        feature100_610[sound]=list(channel1.reshape(17,-1).sum(axis=1))#.shape
        #np.corrcoef([0,1,2],[100,4,7])#自身以及行与行之间的相关系数矩阵
    with open("./feature100_610.py","w") as f:
        f.write(str(feature100_610))
        
plot(range(17), 
     [-93721, 48130, 119375, 41753, -54122, -89073, -81617, 65237, 91177, 44435, -28120, -56240, -58709, 9845, 
      80651, 39143, -2811], color='k')        
        
# Feature extraction example
import numpy as np
import librosa
 
# Load the example clip
y, sr = librosa.load(librosa.util.example_audio_file())
 
# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length = 512
 
# Separate harmonics and percussives into two waveforms
y_harmonic, y_percussive = librosa.effects.hpss(y)
 
# Beat track on the percussive signal
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
 
# Compute MFCC features from the raw signal
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
 
# And the first-order differences (delta features)
mfcc_delta = librosa.feature.delta(mfcc)
 
# Stack and synchronize between beat events
# This time, we'll use the mean value (default) instead of median
beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
                                    beat_frames)
 
# Compute chroma features from the harmonic signal
chromagram = librosa.feature.chroma_cqt(y=y_harmonic,
                                        sr=sr)
 
# Aggregate chroma features between beat events
# We'll use the median value of each feature between beat frames
beat_chroma = librosa.util.sync(chromagram,
                                beat_frames,
                                aggregate=np.median)
 
# Finally, stack all beat-synchronous features together
beat_features = np.vstack([beat_chroma, beat_mfcc_delta])