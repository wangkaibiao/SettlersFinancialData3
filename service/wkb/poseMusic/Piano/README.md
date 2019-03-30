###### 一、简介
    通过持续播放多个钢琴音源文件，形成钢琴曲。用程序演奏钢琴曲，你也可以！

###### 二、环境要求  
    1.python2    
    
    2.pip install mp3play
    
    3.将res/sound中的音源文件保存至本地

###### 三、说明
    1.音源文件
        所在目录：res/sound
        0-7: 钢琴键盘从左往右，从低到高
        
        C: do (白键)
        C+: 升do降re (黑键)
        D: re
        D+: 升re降mi
        E: mi
        F: fa
        F+: 升fa降sol
        G: sol
        G+: 升sol降la
        A: la
        A+: 升la降si
        B: si
    
    2.开发建议：
        A.将第一个音的播放时间适当延长(系统初始化)
        B.根据音符节拍设置等待时长:
            休止符：延长等待时间
            1拍：音源播放后等待2秒
            2拍：音源播放后等待1秒
            4拍: 音源播放后等待0.5秒
            8拍: 音源播放后等待0.25秒
            16拍: 音源播放后等待0.125秒
            32拍: 音源播放后等待0.0625秒
            64拍：经过测试，电脑暂不支持