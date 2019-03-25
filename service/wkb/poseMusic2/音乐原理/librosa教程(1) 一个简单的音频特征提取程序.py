# -*- coding: utf-8 -*-
python音频处理库librosa教程(1) 一个简单的音频特征提取程序
这是librosa教程的第一篇。主要通过解释官网的样例程序来解释如何使用librosa提取音频特征。librosa是一个音频特征提取库，在论文librosa: Audio and Music Signal Analysis in Python中提出的，如果在学术中使用的话，可以引用该论文。

本文的目标是在python中实现对于音频特征提取，提取出一个时序的特征向量。

librosa是一个专用于处理音频的库，其官方教程可以在 Librosa官方教程 中找到，这篇教程也是基于官方教程写出来的。

笔者学习一个库一般都是直接看一篇样例程序，一般来说，弄懂样例程序究竟讲了什么，也就弄懂了这个库了。作为一个目标为提取音频特征的代码库，官方索性就直接用一个简单的“音频特征提取”代码作为样例程序。这也给我们带来了很大的便利。

Feature extraction examplePython
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
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
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
音频读入
Python
y, sr = librosa.load(librosa.util.example_audio_file())
1
y, sr = librosa.load(librosa.util.example_audio_file())
首先，我们需要知道声音是如何在电脑中储存的，声音信号作为一个连续的函数，在计算机中，只能够用采样的形式储存。



具体来说，采样就是将原来的连续函数中，指定间隔求出一系列离散的时刻对应的信号大小，如librosa默认每秒钟采样22050个采样点，则原来的音频信号就变成了每秒钟22050个值得离散函数。显然，当采样点足够密集，那么我们得到的序列就能够足够逼近原函数。在波形图中，声波平均振幅可用来表示响度的大小，而每一个周期的时间(过零率)可以用来表示音高。

librosa.load 函数的具体实现细节如下

loadPython
y, sr = load(path, sr=22050, mono=True, offset=0.0, duration=None, dtype=<class 'numpy.float32'>, res_type='kaiser_best')
1
y, sr = load(path, sr=22050, mono=True, offset=0.0, duration=None, dtype=<class 'numpy.float32'>, res_type='kaiser_best')
返回值的第一部分，就是将连续的音频信号按照给定的采样率(sample rate) 进行采样的结果，这个结果是一个一维的 numpy 数组，可用于后续的分析。

返回值的第二部分，就是采样率，也就是说完全是函数参数中sr的拷贝。在少数情况下，我们设置函数参数为 sr=None ，采样率就完全依照MP3默认的采样率返回，这个时候返回值 sr 就是我们评判数组 y 代表的音频究竟有多快的唯一方式了。

由简单数学推导可以得到音频时间T可以由y和sr决定

    \[T = \frac{len(y)}{sr}\]

波形分割
接下来，y作为一个合成波形，可以分成两个分量，即谐波(harmonic)与冲击波(percussive)。由于笔者也不太清楚他们具体该怎么翻译，所以按照自己的理解自由发挥咯。

Python
y_harmonic, y_percussive = librosa.effects.hpss(y)
1
y_harmonic, y_percussive = librosa.effects.hpss(y)
从粒度上来看，谐波相对为细粒度特征，而冲击波为粗粒度特征。诸如敲鼓类似的声音拥有可辨别的强弱变化，归为冲击波。而吹笛子这种人耳本身无法辨别的特征，是谐波。接下来，我们将分别对于冲击波以及谐波进行特征的提取。感性理解，冲击波表示声音节奏与情感，谐波表示声音的音色。

节拍提取
Python
# Beat track on the percussive signal
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
1
2
# Beat track on the percussive signal
tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
beat_frames指的就是每一拍(beat)所对应的帧(frame)位置。如果不明白beat，frame这些术语都是指的什么，那么可以参考官方文档.

Python
# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length = 512
1
2
# Set the hop length; at 22050 Hz, 512 samples ~= 23ms
hop_length = 512
这一句话真的是一个非常有误解性质的语句，对于hop_length的详细讲述可以在 python音频处理库librosa教程(2) hop_length的选取 里面看到。倘若无法理解的话，这里给出一个捷径：对于librosa里面的所有函数，都会有一个默认的 hop_length=512 ，也就是说，我们完全可以删掉这句话，对于之后的hop_length，我们都直接使用函数的默认值就好了。

节拍提取在音频特征提取中的意义在于，节拍是所有曲子共有的，不同节拍(beat)中，音频特征或多或少有些不同。在我们模型中，如果我们每隔1ms提取出了一个音频特征（如音高），我们不如将同一拍的所有音高取平均值作为这一拍的音频特征。这样表征效果会好很多。

音频特征提取
接下来，我们可以计算梅尔频率倒谱系数(MFCC)，简单来说，MFCC可以用以表达曲目的音高和响度的关联。经典的MFCC的输出向量维数是13，也就是说在非必要的情况下，这个 n_mfcc 参数就不要改了（这是笔者投paper的时候用血换来的教训啊）

Python
# Compute MFCC features from the raw signal
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)

# And the first-order differences (delta features) 
mfcc_delta = librosa.feature.delta(mfcc)
1
2
3
4
5
# Compute MFCC features from the raw signal
mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
 
# And the first-order differences (delta features) 
mfcc_delta = librosa.feature.delta(mfcc)
MFCC本身只反映了音频的静态特性，所以我们需要对他进行差分，以得到动态特性。即音频是“如何”变化的。

既然我们已经分别得到了mfcc以及mfcc_delta，那么我们可以将它们合称为一个特征，合并过程只是单纯的二维矩阵拼接，这里用了np.vstack函数。接着，librosa.util.sync函数用于以窗口形式合并多个连续的变量，比如这里，就以beat_frames为分界点，对每一个分界点中的序列用其平均值表示。到了这一步，我们得到的是，长度为音乐拍数，宽度为特征数的矩阵。

Python
# Stack and synchronize between beat events
# This time, we'll use the mean value (default) instead of median
beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
                                    beat_frames)
1
2
3
4
# Stack and synchronize between beat events
# This time, we'll use the mean value (default) instead of median
beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),
                                    beat_frames)
下面是对于谐波进行分析

Python
# Compute chroma features from the harmonic signal
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)


# Aggregate chroma features between beat events # We'll use the median value of each feature between beat frames 
beat_chroma = librosa.util.sync(chromagram, beat_frames, aggregate=np.median)
1
2
3
4
5
6
# Compute chroma features from the harmonic signal
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
 
 
# Aggregate chroma features between beat events # We'll use the median value of each feature between beat frames 
beat_chroma = librosa.util.sync(chromagram, beat_frames, aggregate=np.median)
由于这里出来的是一个类似于色度图的东西，所以笔者非常怀疑其在后续训练模型的意义是否足够。之后，用同样的方法，将色度图按照beat_frames进行简化。

附录
节拍提取算法详情：Beat Tracking by Dynamic Programming

基于Librosa的拓展：实时的音频特征分析库rcaudio
