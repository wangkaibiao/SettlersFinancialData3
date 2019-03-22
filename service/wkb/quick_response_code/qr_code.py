#-*- coding:utf-8 -*-
# test created on 14-10-28 下午12:48  
# Copyright 2014 offbye@gmail.com 
 
"""生成带logo的二维码
参数解释：
version：控制二维码的大小，取值范围从1到40。取最小值1时，二维码大小为21*21。
         取值为 None （默认）或者使用fit=true参数（默认）时，二维码会自动调整大小。
error_correction：控制二维码纠错级别。
ERROR_CORRECT_L：大约7%或者更少的错误会被更正。
ERROR_CORRECT_M：默认值，大约15%或者更少的错误会被更正。
ERROR_CORRECT_Q：大约25%或者更少的错误会被更正。
ERROR_CORRECT_H：大约30%或者更少的错误会被更正。
box_size：控制二维码中每个格子的像素数，默认为 10。
border：控制二维码四周留白包含的格子数，默认为4。
image_factory：选择生成图片的形式，默认为 PIL 图像。
mask_pattern：选择生成图片的的掩模。
方法属性解释,常用方法：
add_data(str,optimize=20):添加要转换的文字到data参数；如果使用了optimize优化参数，
        数据将被拆分为多个块来进行优化，以找到一个长度至少为这个值的足够简洁的方式来生成二维码。设置为“0”以避免优化。
make(fit=True):当fit参数为真或者没有给出version参数时，将会调用best_fit方法来找到适合数据的最小尺寸。
        如果没有设置mask_pattern，将会调用best_mask_pattern方法来找到找到最有效的掩模图案。
        最后将这些数据传递给makeImpl方法来生成二维码。与qrcode本体的make方法不一样的是，这个方法没有任何返回值。
make_image(fill_color=None, back_color=None,image_factory=None):创建二维码的图像并返回，默认为 PIL 图像。**
"""   
__author__ = ['"Xitao":<offbye@gmail.com>']   
import qrcode  
from PIL import Image, ImageDraw, ImageFont  
import os,sys,zipfile,shutil,requests


"""
   由于zip格式中并没有指定编码格式，Windows下生成的zip文件中的编码是GBK/GB2312等，因此，
   导致这些zip文件在Linux下解压时出现乱码问题，因为Linux下的默认编码是UTF8。
   Python解压缩ZIP文件出现乱码问题的解决方案,查看zipfile的源码后，终于找到原因：
if zinfo.flag_bits & 0x800:
    # UTF-8 filename
    fname_str = fname.decode("utf-8")
else:
    fname_str = fname.decode("cp437")
   原来编码不能被正确识别为utf-8的时候，会被是被识别并decode为cp437编码，如果原来是gbk编码的话就会变成乱码。
   作者：大河马爱吃草\链接：https://www.jianshu.com/p/d263c2533628\來源：简书
"""
def process_zip():
    filePath="/media/bdai/LENOVO/SFD_assistant/object_data/儿歌mp3/儿歌童谣1912首打包.zip"
    release_file_dir="/media/bdai/LENOVO/SFD_assistant/object_data/儿歌1912"
    is_zip = zipfile.is_zipfile(filePath)
    if is_zip:
        zip_file_contents = zipfile.ZipFile(filePath, 'r')
        for file in zip_file_contents.namelist():
            filename = file.encode('cp437').decode('gbk')#先使用cp437编码，然后再使用gbk解码
            print(filename)
            zip_file_contents.extract(file,release_file_dir)#解压缩ZIP文件
            os.chdir(release_file_dir)#切换到目标目录
            os.rename(file,filename)#重命名文件
        

"""
#fc-list 查看所有的字体 
#fc-list :lang=zh 查看所有的中文字体
img = Image.open("./d_software_develop/quick_response_code/wkb.jpeg")
draw = ImageDraw.Draw(img)
ttf_ttc = ImageFont.truetype("/usr/share/fonts/truetype/arphic/uming.ttc", 20)#字体location,大小,encoding="utf-8"
draw.text((0, 35),"文字内容",fill=(0,25,25), font=ttf_ttc)#文字位置，内容，字体
img.show()
img.save("path")
""" 
 
def gen_qrcode(string, path, logo=""):  
    """
    生成中间带logo的二维码
    需要安装qrcode, PIL库
    :param string: 二维码字符串
    :param path: 生成的二维码保存路径
    :param logo: logo文件路径
    :return:
    """  
    qr = qrcode.QRCode(  
        version=2,  
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=8,  
        border=3  
    )  
    qr.add_data(string)  
    qr.make(fit=True)#
 
    qr_img = qr.make_image()  
    qr_img = qr_img.convert("RGBA")  
 
    if logo and os.path.exists(logo):  
        icon = Image.open(logo)  
        img_w, img_h = qr_img.size#248  
        factor = 4  
        size_w = int(img_w / factor)  
        size_h = int(img_h / factor)  
 
        icon_w, icon_h = icon.size  
        if icon_w > size_w:  
            icon_w = size_w  
        if icon_h > size_h:  
            icon_h = size_h  
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)  
 
        w = int((img_w - icon_w) / 2)  
        h = int((img_h - icon_h) / 2)  
        icon = icon.convert("RGBA")  
        qr_img.paste(icon, (w, h), icon)
    draw = ImageDraw.Draw(qr_img)
    ttf_ttc = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 15)
    #/usr/share/fonts/truetype/arphic/uming.ttc
    draw.text((20, 0),string,fill=(0,25,25), font=ttf_ttc)
    qr_img.save(path)  
    
    
def sum_image(path = "./d_software_develop/quick_response_code/QRs",images = [],quality_value = 100):
    UNIT_SIZE = 248 # 单个图像的大小为248*248
    TARGET_WIDTH = 5 * (UNIT_SIZE+55) # 拼接完后的横向长度为6*248 
    target = Image.new('RGB', (TARGET_WIDTH, (UNIT_SIZE+55)*14))
    h=0    
    for i in range(int(len(images)/5)): # 6个图像为一组
        w=0
        imagefile = []
        j = 0
        for j in range(5):
            imagefile.append(Image.open(path+'/'+images[i*5+j])) 
        for image in imagefile:     
            target.paste(image, (w,h))# 将image复制到target的指定位置中
            w += UNIT_SIZE+53 # left是左上角的横坐标，依次递增
#            right += UNIT_SIZE # right是右下的横坐标，依次递增
        h += UNIT_SIZE+53
     # quality来指定生成图片的质量，范围是0～100
    target.save(path+'/'+'sum_image.jpg', quality = quality_value)


 
#if __name__ == "__main__":
mp3_list=os.listdir("/media/bdai/LENOVO/SFD_assistant/object_data/儿歌mp3/songs")
#mp3_list=[mp3 for mp3 in mp3_list if ".mp3" in mp3]
mp3_list=["小猴取球","小蜗牛排队","掉进陷阱里的小老虎","小蜗牛让座","着火了","懂事的小熊猫","牛奶炸药包","换房子","贪心的小狮子","大雁南飞","零食大王","蜡烛花","上学迟到了","小象笨笨种白菜","教师节礼物","小企鹅捕鱼","负责的老师","风宝宝来了","新来的小熊","快乐准则","小狐狸佳佳","小白兔分奶糖","小刺猬和小兔","小兔子和雪人","大恐龙希希","看谁跑得慢","小兔找珍珠","一座小桥","松鼠赔玻璃","冬暖","怪乘客","失信的小黄莺","鸭子领蛋","脏小猪找朋友","一担草帽","难忘的生日","母亲节的礼物","丁丁的零花钱","小蚂蚁和粮食","乐的黑眼圈"]
#len(mp3_list)
#QR_list=[]
for mp3 in mp3_list:
    #name="QR碼- 维基百科，自由的百科全书"
    gen_qrcode(mp3,
               "./d_software_develop/quick_response_code/QRs/%s_qr.png"%mp3, 
               "./d_software_develop/quick_response_code/wkb1.jpeg")
    
sum_image(images=["%s_qr.png"%mp3 for mp3 in mp3_list])

def copy_file():
    base_path="/media/bdai/LENOVO/SFD_assistant/object_data/故事绘本/"
    for mp3 in mp3_list:
        try:
            shutil.copy(base_path+mp3+".mp3","/media/bdai/LENOVO/SFD_assistant/object_data/temp_songs/")
        except Exception as error:
            print(error)
            
def aim_download():
    song_datas=eval(open("/media/bdai/LENOVO/SFD_assistant/object_data/song_datas.txt","r").read())
    dic_name_url={song['songName']:song['songFileUrl'] for song in song_datas}
    song_name=[]
    #len(song_name)
    error_song=[]
    for mp3 in mp3_list:
        song_name.append(mp3) 
        try:
            song=requests.get(dic_name_url[mp3]) 
            with open("/media/bdai/LENOVO/SFD_assistant/object_data/temp_songs/%s.mp3"%mp3, "wb") as code:
                code.write(song.content)
        except Exception as error:
            error_song.append(mp3)
            print(error)


