#000、有错误要先自己看和理解，然后再上网搜索错误提示的英语并看和理解
"""
有错误要先自己看和理解，然后再上网搜索错误提示的英语并看和理解
"""
#001、Linux双系统安装或者重装
"""
新安装：用韩博士制作启动U盘，新式电脑使用USB-HDD+模式、同时bios设置uefi优先，
老式电脑用RAW模式、同时bios设置支持legacy，安装的时候选择【双系统】或者【其他】、
用减号来还原一个盘成为空白分区、接着用加号新建一个分区、最下边选择【/】、点击安装。
重装的时候也选择【其他】，win10系统下会自动保留原分区且不删除非空白分区中的文件。

重装：U盘作为启动盘-恢复原来容量，2016年12月17日 https://blog.csdn.net/dark5669/article/details/53716039
一般我们用U盘做PE 的时候，会占用u盘500M到1G左右的空间，但是平常格式化的话，不会恢复。我们在磁盘管理里可以看到，
优盘未分配的空间，就是你要恢复的空间；windows 有个磁盘管理的命令，我们可以使用它来恢复我们的U盘空间；
1.打开cmd，命令行下输入：diskpart 那么你就会发现，你已经进入了diskpart 这个目录（模块）
2.DISKPART>下，输入：list disk 这会显示 ，你当前计算机磁盘的列表，你可以根据 大小来判断，哪个是你的U盘；
3.选中U盘，输入：sel disk 1（大小为U盘16G） 它会输出：磁盘 1 现在是所选磁盘
4.清除磁盘 输入：clean
5.右击电脑打开管理，打开存储，打开磁盘管理，右击可移动磁盘选择新加卷，格式化即可恢复。
"""
#002、软启动系统,sudo是标配
"""
在windows下安装软件，我们只需要有EXE文件，然后双击，下一步直接OK就可以了。但在LINUX下，不是这样的。
每个LINUX的发行版，比如UBUNTU，都会维护一个自己的软件仓库，我们常用的几乎所有软件都在这里面。
这里面的软件绝对安全，而且绝对的能正常安装。那我们要怎么安装呢？在UBUNTU下，我们维护一个源列表，
源列表里面都是一些网址信息，这每一条网址就是一个源，这个地址指向的数据标识着这台源服务器上有哪些软件可以安装使用。
编辑源命令：sudo gedit /etc/apt/sources.list
在这个文件里加入或者注释（加#）掉一些源后，保存。这时候，我们的源列表里指向的软件就会增加或减少一部分。
接一下要做的就是：sudo apt update
这个命令，会访问源列表里的每个网址，并读取软件列表，然后保存在本地电脑。我们在新立得软件包管理器里看到的软件列表，
都是通过update命令更新的。
update后，可能需要upgrade一下，sudo apt upgrade
这个命令，会把本地已安装的软件，与刚下载的软件列表里对应软件进行对比，如果发现已安装的软件版本太低，就会提示你更新。
如果你的软件都是最新版本，会提示：升级了 0 个软件包，新安装了 0 个软件包，要卸载 0 个软件包，有 0 个软件包未被升级。
总而言之，update是更新软件列表，upgrade是更新软件。
"""
#003、搜狗输入法安装和启用
"""
百度搜索即可,sudo dpkg -i 搜狗拼音安装包.deb
"""
#004、将python3设置为系统默认
"""
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 150  ，这个数字代表优先级，
数字越大越优先。
"""
#005、安装spyder和pip
"""
输入spyder3并回车，根据系统提示的命令安装python3的spyder；
输入pip3并回车，根据系统提示的命令安装python3的pip；
pip3 show tensorflow
pip3 list  列出本地所有的安装包
pip uninstall 包名卸载不用的包
"""
#006、mysql数据库安装
"""
sudo apt-get install mysql-server 数据库服务器，用于管理数据库与表，控制用户访问，以及处理SQL查询；
apt-get isntall mysql-client    MySQL客户端程序，实现用户与服务器的连接与交互功能；
sudo apt-get install libmysqlclient-dev   编译使用MySQL的其他程序的过程中会用到的一些库及头文件（可能用不到）。 
第一步：进入/etc/mysql目录下，然后sudo vim/vi debian.cnf【ubuntu使用sudo vi debian.cnf】查看里面的用户名和密码，
然后使用这个文件中的用户名和密码进入mysql,假如debian.cnf中的用户名为debian-sys-maint,
则：mysql -u debian-sys-maint -p按回车，这时需要你输入密码，复制debian.cnf中的密码（不要手动输入)；
此时你能进入到mysql里面了。按照其他的修改秘密方法仍然不能使用mysql -u root -p 进入root用户。
查看一下user表，错误的起因就是在这里，root的plugin被修改成了auth_socket，用密码登陆的plugin应该
是mysql_native_password。

mysql> SELECT user,host,plugin FROM mysql.user;

+-----------+-----------+-----------------------+

| user      | host      | plugin                |

+-----------+-----------+-----------------------+

| root      | localhost | auth_socket           |

| mysql.sys | localhost | mysql_native_password |

+-----------+-----------+-----------------------+

关于auth_socket，在官方有说明：
https://dev.mysql.com/doc/mysql-security-excerpt/5.5/en/socket-authentication-plugin.html ，
反正现在暂时不用它， 那就把这里改了。
mysql> UPDATE mysql.user SET authentication_string=PASSWORD('123456'), plugin='mysql_native_password' WHERE user='root';
显示   Query OK, 1 row affected, 1 warning (0.01 sec)
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
mysql> quit
重启服务，问题就解决了。sudo service mysql stop； sudo service mysql start； mysql -u root -p  并回车
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.7.10 MySQL Community Server (GPL)
"""
#007、使用github
"""
配置git指定用户名和邮箱：
$ git config --global user.name "wangkaibiao"
$ git config --global user.email "cmbc95568@139.com"
在某文件夹下打开终端，克隆 git clone https://github.com/wangkaibiao/SettlersFinancialData2.git
修改本地仓库代码，完成后，在仓库目录下打开终端，用git add .命令告诉git，将所有文件修改添加到仓库：
用git commit命令告诉git，将文件提交到仓库：git commit -m "add a new file"
推送到远程github仓库：git push origin master，此处的master也可以换成分支名

强制覆盖本地：
git fetch --all  
git reset --hard origin/master
git pull
"""
#008、核心基础理解
"""
linux系统总结：专为程序员设计的稳定安全快速电脑操作系统，主要采用命令行式操作，类似于python环境的脚本式操作。
操作系统本质是基础软件【核心是架构中的机器指令集，加不同的C语言编译器】，其他软件相当于是特定功能的增加，
不同的是操作系统软件需要对机器指令集支持。此外，电脑出厂时都带有bios（basic input output system）设置功能，
可以作最简单必要基础的设置，然后引入操作系统，如windows和linux操作系统。
"""
#009、python项目系统结构
"""
包（文件夹）、模块（.py文件）、类（def class ）、函数、变量，
以上加入  __init__.py  文件后就可以直接import导入了，有时还需要sys.path.append()
"""
#010、Ubuntu apt-get彻底卸载软件包
"""
apt-get的卸载相关的命令有remove/purge/autoremove/clean/autoclean等。具体来说：
apt-get purge / apt-get --purge remove 删除已安装包（不保留配置文件)。 如软件包a，依赖软件包b，
则执行该命令会删除a，而且不保留配置文件;
apt-get autoremove   删除为了满足依赖而安装的，但现在不再需要的软件包（包括已安装包），保留配置文件。
apt-get remove 删除已安装的软件包（保留配置文件），不会删除依赖软件包，且保留配置文件。
apt-get autoclean APT的底层包是dpkg, 而dpkg 安装Package时, 会将 *.deb 放在 /var/cache/apt/archives/中，
apt-get autoclean 只会删除 /var/cache/apt/archives/ 已经过期的deb。
apt-get clean 使用 apt-get clean 会将 /var/cache/apt/archives/ 的 所有 deb 删掉，可以理解
为 rm /var/cache/apt/archives/*.deb。
那么如何彻底卸载软件呢？ 具体来说可以运行如下命令：
# 删除软件及其配置文件  apt-get --purge remove <package>
# 删除没用的依赖包  apt-get autoremove <package>
# 此时dpkg的列表中有“rc”状态的软件包，可以执行如下命令做最后
清理：dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P
当然如果要删除暂存的软件安装包，也可以再使用clean命令。
"""
#011、apt和apt-get区别
"""
不能什么事情都依赖重装，否则请不要使用Linux，那和自杀没区别；在Linux上，一切皆文件，当然这些程序也是以文件的形式存在的，
Linux下不涉及注册表的操作，重新安装的时候只要完全覆盖，怎么可能存在装不上的情况呢？如果你真的什么都不懂，就多折腾几次，
折腾不来的说明你没有天分，还是放弃Linux吧。
Debian 作为 Ubuntu、Linux Mint 和 elementary OS 等 Linux 操作系统的母板，其具有强健的「包管理」系统，它的每个组件和
应用程序都内置在系统中安装的软件包中。Debian 使用一套名为 Advanced Packaging Tool（APT）的工具来管理这种包系统，不过
请不要把它与 apt 命令混淆，它们之间是其实不是同一个东西。在基于 Debian 的 Linux 发行版中，有各种工具可以与 APT 进行交互，
以方便用户安装、删除和管理的软件包。apt-get 便是其中一款广受欢迎的命令行工具，另外一款较为流行的
是 Aptitude 这一命令行与 GUI 兼顾的小工具。在使用 apt 命令时，用户不必再由 apt-get 转到 apt-cache 或 apt-config，
而且 apt 更加结构化，并为用户提供了管理软件包所需的必要选项。简单来说就是：
apt = apt-get、apt-cache 和 apt-config 中最常用命令选项的集合。
虽然 apt 与 apt-get 有一些类似的命令选项，但它并不能完全向下兼容apt-get命令。也就是说，可以用apt替换部分apt-get系列命令:
apt 命令	取代的命令	命令的功能
apt install	apt-get install	安装软件包
apt remove	apt-get remove	移除软件包
apt purge	apt-get purge	移除软件包及配置文件
apt update	apt-get update	刷新存储库索引
apt upgrade	apt-get upgrade	升级所有可升级的软件包
apt autoremove	apt-get autoremove	自动删除不需要的包
apt full-upgrade	apt-get dist-upgrade	在升级软件包时自动处理依赖关系
apt search	apt-cache search	搜索应用程序
apt show	apt-cache show	显示装细节
当然，apt 还有一些自己的命令：
新的apt命令	命令的功能
apt list	列出包含条件的包（已安装，可升级等）
apt edit-sources	编辑源列表
需要大家注意的是：apt 命令也还在不断发展， 因此，你可能会在将来的版本中看到新的选项。
"""
#012、删除包含关键字的文件或文件夹
"""
find . -name '*spyder*' -type d -print -exec sudo rm -rf {} \;
find . -name '*spyder*' -type f -print -exec sudo rm -rf {} \;
其中.代表当前目录，'*spyder*'代表包含关键字，d代表文件夹、f代表文件，必须有print以显示处理过程和结果，
{}代表find查找的结果，必须有；且用\来转义避免系统歧义。sudo rm -rf 文件夹 表示完全删除文件夹。
"""
#013、ubuntu段错误（核心已转储）仍然无法解决spyder问题
"""
配置操作系统使其产生core文件，首先通过ulimit命 令查看一下系统是否配置支持了dump core的功能。
通过ulimit -c或ulimit -a，可以查看core file大小的配置情况，如果为0，则表示系统关闭了dump core。
可以通过ulimit -c unlimited来打开。若发生了段错误，但没有core dump，是由于系统禁止core文件的生成。
解决方法: $ulimit -c unlimited （只对当前shell进程有效）；或在~/.bashrc　的最后加入： ulimit -c unlimited （一劳永逸）
用gdb查看core文件，发生core dump之后, 用gdb进行查看core文件的内容, 以定位文件中引发core dump的行.
gdb [exec file] [core file]    如: gdb ./test test.core
"""
#014、python操控adb实现qpython自动开发运行【临时放弃，在已有圈子内做精、不扩大未知范围了】
"""
ATX ATX-uiautomator2 使用 QPython 在 Android 手机内执行自动化
linpengcheng · February 11, 2018 · Last by linpengcheng replied at 2 months ago · 6502 hits
根据帖子
在 Android 手机内执行 UI 自动化测试
动手实践了一把，把相关的操作步骤记录一下，由于uiautomator2 版本的升级 ，需要依赖的库在原帖上增加了progress 和retry
手机上直接push电脑上的uiautomator2库，
uiautomator2在手机上还需要安装依赖库为：
huamanize、progress、requests、retry 四个
下面是具体的实践步骤
电脑端uiautomator2安装
1、安装uiautomator2，执行命令
pip install --pre -U uiautomator2
2、设备安装atx-agent
首先Android设备连接到PC，并能够adb devices发现该设备，执行命令
python -m uiautomator2 init
最后提示success，代表atx-agent初始化成功。
C:\Users\LiN>python -m uiautomator2 init
2018-02-11 20:15:21,139 - __main__.py:243 - INFO - Device(C4Y5T16810004018) init
ialing ...
2018-02-11 20:15:21,917 - __main__.py:110 - INFO - install minicap
2018-02-11 20:15:22,247 - __main__.py:117 - INFO - install minitouch
2018-02-11 20:15:22,976 - __main__.py:132 - INFO - apk(1.0.9) already installed,
 skip
2018-02-11 20:15:23,139 - __main__.py:164 - INFO - atx-agent(0.2.0) already inst
alled, skip
2018-02-11 20:15:23,140 - __main__.py:198 - INFO - launch atx-agent daemon
2018-02-11 20:15:25,371 - __main__.py:213 - INFO - atx-agent output: server star
ted, listening on 192.168.31.128:7912
2018-02-11 20:15:25,373 - __main__.py:214 - INFO - success
QPython安装
QPython是一个能让安卓手机运行和编写Python的APP，Github下载地址下载链接
下载qpython-release.apk，然后使用adb install安装即可。
安装好之后，由于uiautomator2的库依赖huamanize、progress和requests，打开QPython，点击QPYPI，
然后点击INSTALL WITH PYTHON'S PYPI，分别执行:
pip install requests
pip install humanize
pip install progress
安装成功即可。
将相关的库及脚本文件push到手机内
在手机上运行编写的自动化脚本文件，需要用到uiautomator2库和相关的依赖库retry，由于INSTALL WITH PYTHON'S PYPI无法直接安装，
所以直接将电脑上uiautomator2库的整个文件夹复制到制定的文件夹下就好了。
经过观察QPython中路径在这个下面：
/storage/emulated/0/qpython
将uiautomator2库复制到qpython/lib/python2.7/site-packages下，执行命令
adb push C:\Python35\Lib\site-packages\uiautomator2 /storage/emulated/0/qpython/lib/python2.7/site-packages
将retry库复制到qpython/lib/python2.7/site-packages下，执行命令
adb push C:\Python35\Lib\site-packages\retry /storage/emulated/0/qpython/lib/python2.7/site-packages
将写好的自动化脚本文件atx_agent_demo.py复制到qpython/scripts3下，执行命令
C:\Users\LiN>adb push D:\PycharmProjects\autotest\atx_agent_demo.py /storage/emulated/0/qpython/scripts3
手机端运行脚本
文件atx_agent_demo.py用网易云音乐来进行简单的demo演示
import uiautomator2 as ut2
def main():
    u = ut2.connect('http://0.0.0.0:7912')
    print(u.info)
    u.app_start('com.netease.cloudmusic')
    u(text='私人FM').click()
    u(description='转到上一层级').click()
    u(text='每日推荐').click()
    u(description='转到上一层级').click()
    u(text='歌单').click()
    u(description='转到上一层级').click()
    u(text='排行榜').click()
    u(description='转到上一层级').click()
if __name__ == '__main__':
    main()
打开QPython，点击文件，然后点击dcripts找到atx_agent_demo.py，运行即可。附上运行的GIF
How to run QPython over adb shell
由 匿名 (未验证) 提交于 2018-07-23 16:37:49
    登录或注册以发表评论27 次浏览
可以将文章内容翻译成中文,广告屏蔽插件可能会导致该功能失效(如失效，请关闭广告屏蔽插件后再试):
由 Google 翻译翻译强力驱动
问题:
I installed the QPython on my (rooted) phone. I'm having trouble, however, 
running the python binary over the adb shell (busybox).
I can run the python binary after setting:
export LD_LIBRARY_PATH=/vendor/lib:/system/lib:/data/data/com.hipipal.qpyplus/files
However, I cannot import any module from the standard library even setting $PYTHONPATH
export PYTHONPATH=/data/data/com.hipipal.qpyplus/files/lib/python2.7/site-packages
I found a piece of advice how to run QPython in different terminal on the community wiki 
( http://wiki.qpython.org/hacker/#how-to-execute-qpythons-python-in-other-terminals ), 
and I dumped the enviromnent and loaded it in the adb shell, the loaded python still could not load 
any libraries from standard library, like random.
Loading standard libraries from QPython console works just fine. Any pointers?
回答1:
I got python to work by following the provided link, http://wiki.qpython.org/hacker/
#how-to-execute-qpythons-python-in-other-terminals, prepending all lines in the script with export, 
then running as root ". /sdcard/qpyenv.sh". Finally I could run "python" and "import os" and all warning 
at the top disappeared.
root@trelte:/ # . /sdcard/qpyenv.sh                                            
root@trelte:/ # python
Python 2.7.2 (default, Oct 25 2014, 20:52:15) 
[GCC 4.9 20140827 (prerelease)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>>
回答2:
In my experience you only need to set two variables for this to work:
export PYTHONHOME=/data/data/org.qpython.qpy/files
export LD_LIBRARY_PATH=
.:/data/data/org.qpython.qpy/files/lib/:/data/data/org.qpython.qpy/files/:/data/data/org.qpython.qpy/lib/
but you need to run as root so you can access things in /data/data/org.qpython.qpy/
"""
#015、关于qpython3.6的使用
"""
安装完qpython3.2之后、安装qpy3_V9_180314.apk，此时可以切换了，如果直接运行脚本会提示
……qpython3-android5.sh not found     ，这时先打开qpython3的console功能、看看能否显示python3.6.4的命令行窗口，
如果显示、然后运行脚本，否则在运行脚本后的错误提示窗口中输入
【If it still fail, please execute the following code in the console】
"source /data/data/com.hipipal.qpyplus/files/bin/init.sh && python" 【or】
"source /data/data/com.hipipal.qpyplus/files/bin/init.sh && python-android5" (for android5 / androidL user)
再尝试运行脚本，如果还不行就安装qpython2，然后在qpy3中点击释放资源、打开qpython3、打开qpython2、重复以上步骤【做一下切换、如果只提示成功不提示抽取文件失败即可】。
可以运行脚本后、也可以删除qpy3和qpython2。
"""
#016、一定要看清程序的依赖库版本，快速安装源
"""
pip3 install opencv-python==3.* -i https://mirrors.ustc.edu.cn/pypi/web/simple

"""
#017、Linux下TensorFlow.js的PoseNet demo
"""
首先将项目clone下来    git clone https://github.com/tensorflow/tfjs-models.git
进入PoseNet目录        cd posenet/
使用yarn安装，如果电脑上没有安装yarn，可以先使用  sudo apt install yarn -g   安装yarn
安装完运行             yarn 
进入demos文件夹 cd demos 并运行命令 yarn  以安装依赖关系并准备build目录，
安装完成，现在可以运行demo了     yarn watch ，打开命令窗口给出的网址  http://localhost:1234/
点击Camera feed demo会打开摄像头，进行实时的姿态估计 
点击Coco images demo则会演示如何在图像中进行姿态估计，并且演示了多人和单人姿态估计之间的差异
☆★☆后期通过修改demo文件夹下的html文件和js文件来作为本地服务器以增加可用性☆★☆ 
"""
#018、chrome调用网络摄像头
"""
Chrome为什么允许网络摄像头通过http？  回答 (2)关注 (0)查看 (836)
我正在使用webrtc视频构建自助服务终端应用程序。它只在内部网络上提供，我希望能够始终通过http允许我的网站摄像头。
有没有办法做到这一点？
用户回答回答于 2018-03-16  哟有，管理员可以使用策略覆盖提示：视频捕获
此列表中的模式将与请求URL的安全来源相匹配。如果找到匹配项，则不需要提示就可以访问音频捕获设备。
注意：目前只有在Kiosk模式下运行时才支持此策略。
在Windows上，可以使用Regedit创建注册表项。
Software\Policies\Chromium\VideoCaptureAllowedUrls\1 = "http://www.example.com/"
Software\Policies\Chromium\VideoCaptureAllowedUrls\2 = "http://[*.]example.edu/"
在Linux上，可以将策略写入一个文件中：
mkdir -p /etc/opt/chrome/policies/managed
touch /etc/opt/chrome/policies/managed/test_policy.json
在test_policy.json：
{  "VideoCaptureAllowedUrls": ["http://www.example.com/", "http://[*.]example.edu/"]   }

用户回答回答于 2018-03-16   使用命令行标志:
使用--use-fake-ui-for-media-stream命令行标志
示例(OS X)：/Applications/Google\ Chrome.app/Contents/MacOS/Google\ 
Chrome http://html5-demos.appspot.com/static/getusermedia/record-user-webm.html --use-fake-ui-for-media-stream
"""
