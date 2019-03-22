#001、单片机 指令集 和 操作系统的关系【编译器 处在唯一枢纽：程序→编译器→指令集→cpu架构】
"""【一土点儿 - CSDN博客 https://blog.csdn.net/zhongjin616/article/details/18765301】
阅读数：2555 2014-01-25


1> 首先讨论各种单片机与操作系统的关系【CPU属于单片机、编译是如何应需而生的】
说到单片机，大家第一时间想到的应该是51单片机，对吧。不错，更高级一点的AVR，把他称为单片机，
我们也还觉得可以接受。那么再高级一点的ARM7，8086，80386，Core i3，Athlon 等等我们更习惯称他们为CPU，
因为学习计算机原理的时候都是这么叫的，但按照单片机的定义，他们也是归属于单片机。这也不怪大家，
中国的教育都是这样，只注重告诉你是什么，而不告诉你他们之间的联系。
上述几种单片机或者芯片（如果你还是觉得把core i3叫做单片机你不习惯的话）在原理上都是一样，
即都是有运算器 控制器 寄存器构成的，不同之处在于它们的硬件电路实现不同，个数不同，功耗不同，
计算能力不同，但都提供相同的基本功。OK，终于让cpu找到了组织，那么就介绍为什么有的单片机要操作系统，
有的在我们学习的过程中压根就跟操作系统不挨边。

51/AVR单片机  在学习他们的时候，都是先介绍它们有哪些资源——有几个寄存器，有几个时钟等，
然后就是怎么用汇编，用C或者是C与汇编混合编程。这里我们用的语言都是可以直接操作硬件资源的，
因此我们可以自己决定什么时候使用哪个寄存器，什么时候将寄存器内容写到辅存储器中。

ARM单片机 在学习它的时候，我们可以给他搭载操作系统，如MicroC/OS，iOS X, Android或者其他
定制的linux操作系统，但有时我们也经常不让它搭载操作系统，而是直接像使用51单片机那样来操作它。

Core i3 / Athlon单片机（或者CPU，如果你还是不喜欢用单片机来形容这么牛逼的硬件）
你几乎没有听说过身边谁会在这种单片机上开发应用【这里指操作系统类的】（如果有，一定要引荐我认识一下哦），
因为在这种单片机上开发的应用有一个很牛逼的名字——操作系统！ 由于这种单片机提供的资源太多，能干的活太多，
我们需要有一个专门的程序来负责管理它，从而避免对相同的功能重复开发。这样我们就可以从对硬件编程中解放出来，
更专注于应用层面的开发。从某种意义上来说，操作系统也就是一个应用程序而已，只不过他有点特别。

一般这种情况下，打个比方会比较好——单车和汽车。单车很简单，我们对它的构成及零部件也很熟悉，链条掉了，
我们也完全能够应付。这就好比51单片机，资源不多，我们完全能够hold住。相较而言，汽车则复杂很多，
有减速系统，刹车系统，电子系统，空调系统等等，但是我们并不需要清楚他们的硬件工作原理，
我们只需要知道按那个开关，踩那个踏板就好了。这就好比单片机上的操作系统，它不需要我们清楚硬件的构造，
想要实现功能，直接调用系统提供的API就可以了。 在我们双脚不停的蹬着踏板，自行车就前进这个动作中，
我们是清楚的知道这其中各个部件的运行原理过程的；但如果你是踏着油门，汽车就跑起来，
我觉得大部分人都不了解其中涉及到了哪些部件，以及各个部件的原理的。但这不妨碍我们使用，不是吗。


2> cpu与指令集的关系
cpu依靠指令来计算和控制系统，每款CPU在设计时就规定了一些列与其硬件电路相配合的指令系统，
或者说某款cpu的硬件设计其实就是针对某个指令集的一种硬件实现。
指令集也就是所谓的目标代码（或称为机器代码，是可以直接在CPU上运行的代码）可以看作是
要求cpu对外提供的功能，某款CPU的设计肯定是朝着某个指令集来的。所以，不同的cpu架构，
也表示这他的指令集要么较之前的指令集有所拓展或者就是实现了一种全新的指令集。指令集中的一条指令，
就是让cpu完成一系列的动作，而该动作的完成则表明了某种运算的完成。一个功能可能需要一条或几条指令来实现。
比如汇编的MOV或者LD语句就可能对应着几条cpu指令。
   【机器语言（machine language）是一种指令集的体系。这种指令集称为机器代码（machine code），是计算机的CPU可直接解读的数据。
    机器代码有时也被称为原生码（Native Code），这个名词比较强调某种编程语言或库与运行平台相关的部分。
    机器语言是用二进制代码表示的计算机能直接识别和执行的一种机器指令的集合。它是计算机的设计者通过计算机的硬件结构赋予
    计算机的操作功能。机器语言具有灵活、直接执行和速度快等特点。不同种类的计算机其机器语言是不相通的，
    按某种计算机的机器指令编制的程序不能在另一种计算机上执行。要用机器语言编写程序，编程人员需首先熟记所用计算机的
    全部指令代码和代码的涵义。手编程序时，程序员要自己处理每条指令和每一数据的存储分配和输入输出，
    还需记住编程过程中每步所使用的工作单元处在何种状态。这是一件十分繁琐的工作，编写程序花费的时间往往是
    实际运行时间的几十倍或几百倍。而且，这样编写出的程序完全是0与1的指令代码，可读性差且容易出错。
    在现今，除了计算机生产厂家的专业人员外，绝大多数程序员已经不再学习机器语言。
机器语言是微处理器理解和使用的用于控制它的操作的二进制代码。
8086到Pentium的机器语言指令长度可以从1字节到13字节。
尽管机器语言看似非常复杂，但它是有规律的。
现今存在着超过100000种机器语言的指令，因此不可能将它们的种类完全列出。
以下是一些示例：指令部分的示例  0000 代表 加载（LOAD）  0001 代表 存储（STORE）  ...
               寄存器部分的示例  0000 代表寄存器 A  0001 代表寄存器 B  ...
               存储器部分的示例  000000000000 代表地址为 0 的存储器
                                000000000001 代表地址为 1 的存储器
                                000000010000 代表地址为 16 的存储器
                                100000000000 代表地址为 2^11 的存储器
               集成示例        0000,0000,000000010000 代表 LOAD A, 16
                              0000,0001,000000000001 代表 LOAD B, 1
                              0001,0001,000000010000 代表 STORE B, 16
                              0001,0001,000000000001 代表 STORE B, 1
      】

下面介绍几种常见的CPU架构与指令集的对应关系（所谓架构是指硬件电路的实现）：
intel X86架构CPU可能实现了多个指令集x86，x86-64，MMX，SSE，SSE2，SSE3，SSSE3 ，
而这些指令集中的指令让cpu完成的动作都比较复杂，所以也称为CISC
AMD amd64架构的cpu 兼容了x86指令集还拓增了3D-Now!指令集，用于加强对3D显示的支持。
ARM ARMv1~ARMv7架构的cpu实现了Thumb指令集和ARM指令集。这些指令集中的一条指令
让cpu完成的动作都比较简单，所以也称为RISC指令集


3> 指令集与操作系统的关系【编译器为何不同的原因、C语言属于高级语言只不过使用早而被硬件适应了】
这里要重新提及一下之前讲到的两个概念：指令集——就是机器代码；操作系统——就是应用程序

首先我们要知道计算机之父冯-诺伊曼说计算机只能运行在二进制上。所以不论是
操作系统还是普通的应用程序最终都得转化到二进制代码才能够被cpu所处理。
而用高级语言编写的普通应用程序都必须经过编译器编译后成为二进制代码（指令）才能运行。
而不同的cpu所实现的指令集不同，所以不同的指令集对应的编译器也不尽相同，编译器不同，
相同的高级语言程序经过编译后所得到的二进制代码也不同。这就引出了“移植”和“跨平台”两个概念。
OK，重新捋一下：cpu架构-指令集-编译器-程序 环环相扣，紧密联系。所以你就会听到说Windows操作系统
只能够运行在X86架构的CPU上，不能运行在Power 或 ARM 上，因为指令集不同，又所以就有了“Wintel”联盟。
所以你也可以看到有的编译器是有硬件厂家提供的，比如Intel就提供C和C 的编译器，
这样编译出来的程序就能更好的利用硬件的性能。那为什么又会听到linux可以运行在不同架构的CPU上呢？
那是因为linux是开源的，因此就可以将它移植到不同的CPU平台上，然后在用相应的编译器编译，
就得到了可以在该CPU上运行的二进制代码了。而Windows是封闭的，得不到源代码，
而MS自己又没有移植到别的CPU平台上的打算，所以当然就只能在X86上运行了。
（BTW，X86也是性能最好的CPU之一，而Windows对性能要求较高，所以MS当然也就不愿意移植了）
"""

#002、编译器和解释器的区别【解释器是经过编译器编译的可以直接运行的机器代码、如python.exe】
"""
共同点是：不同CPU架构需要不同的版本

不同点是：解释器是一条一条的解释执行源语言。 ... 编译器是把源代码整个编译成目标代码，
执行时不在需要编译器，直接在支持目标代码的平台上运行，这样执行效率比解释执行快很多。 
比如C语言代码被编译成二进制代码（exe程序，如python.exe），在windows平台上执行。


举例1>Python解释器，阅读: 468356 【python的运行基础核心还是C语言】
当我们编写Python代码时，我们得到的是一个包含Python代码的以.py为扩展名的文本文件。
要运行代码，就需要Python解释器去执行.py文件。由于整个Python语言从规范到解释器都是开源的，
所以理论上，只要水平够高，任何人都可以编写Python解释器来执行Python代码（当然难度很大）。
事实上，确实存在多种Python解释器。

CPython，当我们从Python官方网站下载并安装好Python 2.7后，我们就直接获得了一个官方版本的
解释器：CPython。这个解释器是用C语言开发的，所以叫CPython。在命令行下运行python就是启动CPython解释器。
CPython是使用最广的Python解释器。教程的所有代码也都在CPython下执行。

IPython，IPython是基于CPython之上的一个交互式解释器，也就是说，IPython只是在交互方式上有所增强，
但是执行Python代码的功能和CPython是完全一样的。好比很多国产浏览器虽然外观不同，但内核其实都是调用了IE。
CPython用>>>作为提示符，而IPython用In [序号]:作为提示符。

PyPy，PyPy是另一个Python解释器，它的目标是执行速度。PyPy采用JIT技术，对Python代码进行动态编译（注意不是解释），
所以可以显著提高Python代码的执行速度。绝大部分Python代码都可以在PyPy下运行，但是PyPy和CPython有一些是不同的，
这就导致相同的Python代码在两种解释器下执行可能会有不同的结果。如果你的代码要放到PyPy下执行，
就需要了解PyPy和CPython的不同点。

Jython，Jython是运行在Java平台上的Python解释器，可以直接把Python代码编译成Java字节码执行。

IronPython，IronPython和Jython类似，只不过IronPython是运行在微软.Net平台上的Python解释器，
可以直接把Python代码编译成.Net的字节码。

小结，Python的解释器很多，但使用最广泛的还是CPython。如果要和Java或.Net平台交互，
最好的办法不是用Jython或IronPython，而是通过网络调用来交互，确保各程序之间的独立性。


举例2>libpython2.7.so.1.0 cannot open的解决方法
【so文件是unix的动态连接库，是二进制文件，作用相当于windows下的.dll文件。 
补充： 在Android中调用动态库文件(*.so)都是通过jni的方式。
2012年03月10日 14:01:42 huzhenwei 阅读数：44223
使用源代码的方式安装Python2.7之后，在import某些库时抛出了如下异常：
ImportError: libpython2.7.so.1.0: cannot open shared object file: No such file or directory
一 原因分析,    由于在系统的lib路径中找不到这个共享库。
   注： 如果编译时加上了--enable-shared，才会编译这个共享库，默认的位置是python可执行程序
所在目录的lib目录下，如/usr/local/python27
二 解决方法
  1. 可以使用如下方式编译Python以解决这个问题：
    ./configure --enable-shared --prefix=/usr/local/python27
    make && make install
  2. cp /usr/local/python27/lib/libpython2.7.so.1.0 /usr/local/lib
     cd /usr/local/lib
     ln -s libpython2.7.so.1.0 libpython2.7.so
  3. 使用命令whereis libpython2.7.so.1.0得到如下结果就说明
    libpython2.7.so.1: /usr/local/lib/libpython2.7.so.1.0
  4. 如果whereis没有结果，或者还有import错误，可以尝试如下操作：
    在/etc/ld.so.conf中加入新行/usr/local/lib
    保存后，运行
    /sbin/ldconfig
    /sbin/ldconfig –v


举例3>dll和exe的区别和联系  2010年03月17日 14:30:00 judy1017 阅读数：2486
        转自：http://www.cnblogs.com/choi/archive/2006/08/11/474139.html
在Windows世界中，有无数块活动的大陆，它们都有一个共同的名字——动态链接库。
现在就让我们走进这些神奇的活动大陆，找出它们隐藏已久的秘密吧！
初窥门径:Windows的基石,　　随便打开一个系统目录，一眼望去就能看到很多扩展名DLL的文件，
这些就是经常说的“动态链接库”，DLL是Dynamic LinkLibrary(即“动态链接库”)的缩写。
从Microsoft公司推出首个版本的Windows以来，动态链接库就一直是这个操作系统的基础。
　　1.看看DLL里有什么
　　与其用晦涩的专业术语来解决DLL是什么，不如先来看看DLL里有什么。DLL和EXE文件一样，
其中包含的也是程序的二进制执行代码和程序所需的资源(比如图标、对话框、字符串等)，
可是为什么要把代码放在DLL里面，而不是做成EXE呢？其实DLL中的代码是以API函数形式出现的，
通俗地说，DLL中包含的程序代码都被做成了一个个小模块，应用程序通过按下所需DLL中特定的按钮，
来调用DLL中这个按钮所代表的功能。在使用“记事本”等程序时，如果要保存文件或打开文件，
就会弹出通用文件对话框，让我们选择文件位置。你可知道，这就是调用了系统底层DLL中的通用对话框界面。
　　2.系统中几个重要的DLL
　　Windows中有3个非常重要的底层DLL:Kernel32.dll、User32.dll、GDI32.dll。
其中Kernel32.dll顾名思义就是内核相关的功能，主要包含用于管理内存、进程和线程的函数;
而User32.dll中包含的则是用于执行用户界面任务的函数，比如把用户的鼠标点击操作传递给窗口，
以便窗口根据用户的点击来执行预定的事件;GDI32.dll的名称用了缩写，
全称是Graphical DeviceInterface(图形设备接口)，包含用于画图和显示文本的函数，
比如要显示一个程序窗口，就调用了其中的函数来画这个窗口。
　　3.为什么要用DLL
　　刚才在谈到这个问题的时候，我们只是解释了DLL将程序代码封装成函数的原理。
为什么封装成函数，就能成为系统中大量使用DLL的理由呢？①扩展应用程序,由于DLL能被应用程序动态载入内存。
所以，应用程序可以在需要时才将DLL载入到内存中，这让程序的可维护性变得很高。比如QQ的视频功能需要升级，
那么负责编写QQ的程序员不必将QQ所有代码都重写，只需将视频功能相关的DLL文件重写即可。②便于程序员合作,
这个和我们最终用户关系不大，仅供了解。我们都知道编程工具有很多，比如VB、VC、Delphi等，
如果好几个人合作来编写一个大的程序，那么可能有的人用VB，有的人用VC，每人负责的部分所使用的编程语言都不同，
究竟放在哪个编译器中进行编译呢？这就好比一群来自各个国家的人在共同编写一篇文章，如果他们所使用的语言都不同，
写出来的文章怎么可能凑到一起呢？而有了DLL后，可以让VC程序员写一个DLL，然后VB程序员在程序中调用，
无需为怎么将它们都编译为一个单独的EXE而发愁了。③节省内存,如果多个应用程序调用的是同一个动态链接库，
那么这个DLL文件不会被重复多次装入内存中，而是由这些应用程序共享同一个已载入内存的DLL。就好比一个办公室中，
很少会为每一个员工配置一台饮水机的，而是在一个公共位置放上一个饮水机，所有需要喝水的职员都可以共用这台饮水机，
降低了成本又节约了空间。④共享程序资源,包括刚才提到过的通用文件对话框在内，DLL文件提供了应用程序间共享资源的可能。
资源可以是程序对话框、字符串、图标，或者声音文件等。⑤解决应用程序本地化问题,在下载了某个程序的汉化包后，
打开汉化说明，经常可以看到用下载包中的DLL文件覆盖掉程序原来的DLL，汉化就完成了。
这些程序都是将执行代码和应用程序界面分开编写了，所以汉化者只需简单地将其中和程序界面相关的DLL汉化并发布即可。


举例4>GCC全过程详解+剖析生成的.o文件  2018年05月24日 20:26:36 ShadowsGtt 阅读数：3954
使用GCC编译一个.c文件影藏了哪些过程？
GCC四步详解
第一步：预处理(也叫预编译)
        gcc -E  hello.c  -o hello.i
        或者 cpp hello.c > hello.i     【cpp是预编译器】
        将所有#define删除，并且展开所有的宏定义
        处理所有的条件预编译指令，如#if #ifdef  #undef  #ifndef  #endif #elif
        处理#include，将包含的文件插入到此处，这是一个递归的过程
        删除所有注释   //   /* */
        添加行号和文件名标识，以便于编译时产生的错误警告能显示行号
        保留#pragma编译器指令
第二步：编译
        gcc  -S  hello.i   -o  hello.s
        将预处理完的.i文件进行一系列的词法分析、语法分析、语义分析及优
        化后生成响应的汇编代码文件，这是整个程序构建的最核心的部分，也是最复杂的部分
第三步：汇编
        gcc  -c  hello.s  -o  hello.o或者 as  hello.s -o  hello.o
        汇编是将第二步生成的汇编代码编程机器可执行的指令，每一个汇编语句几乎都对应一条机器指令
第四步：链接
         链接动态库和静态库

生成的目标文件有什么，什么是目标文件？
目标文件就是源代码经过编译后但未进行链接的那些中间文件,Linux下的 .o文件就是目标文件，
目标文件和可执行文件内容和格式几乎都一样，所以我们可以广义地将目标文件和可执行文化
看成一类型文件。他们都是按照ELF文件格式存储的	。Linux下有哪些ELF类型的文件？
.o文件、可执行文件、核心转储文件(core dump)、.so文件(动态链链接库）

可执行文件的概貌详解，File  Header.text section.data section.bss section
文件头(File Header)，描述了整个文件的文件属性，包括目标文件是否可执行、是静态链接还是
动态链接及入口地址、目标硬件、目标操作系统等信息、段表（描述文件中各个段的偏移位置及属性等）
代码段(.text)存放了程序源代码编译后生成的机器指令
数据段(.data)存放已初始化的全局静态与非静态变量和已初始化的局部静态变量
.bss段 存放未初始化的全局变量(全局静态和非静态变量)和局部静态变量，但是.bss段只是为这些变量预留位置而已，
并没有内容，所以这些变量在.bss段中也不占据空间。

深入挖掘 .o文件：使用命令：
objdump  -h  xxxx.o        打印主要段的信息
objdump  -x  xxxx.o        打印更多的详细信息
objdump  -s  xxx.o         将所有段的内容以16进制方式打印出来
objdump  -d  xxx.o  或者-S 将所有包含指令的段反汇编
objdump  -t  xxx.o         查看所有的符号以及他们所在段
readelf  -h  xxx.o         查看.o文件的文件头详细信息
readelf  -S  xxx.o         显示.o文件中的所有段,即查看段表
size xxx.o           查看.o文件中各个段所占大小
nm xxx.o             查看.o文件中所有的符号

使用命令gcc -c test.c编译下面这个test.c程序生成test.o文件，然后查看test.o文件结构，
test.c
/* this is a test code */
/* test.c */ 
int printf(const char *format, ...); 
int g_var2 = 10;
int g_var2; 
void func(int i)
{
    printf("%d\n",i);
} 
int main(void)
{
    static int static_var1 = 20;
    static int static_var2;    
    int var3 = 1;
    int var4;
    func(static_var1 + static_var2 + var3 + var4);
    return var3;
}
然后查看生成的test.o文件的结构
objdump -h test.o
行：
    .text  :代码段(存放函数的二进制机器指令)
    .data :数据段(存已初始化的局部/全局静态变量、未初始化的全局静态变量)
    .bss  :bss段(声明未初始化变量所占大小)
    .rodata :只读数据段(存放 " " 引住的只读字符串)
    .comment :注释信息段
    .node.GUN-stack :堆栈提示段
列：
    Size:段的长度
    File Off :段的所在位置(即距离文件头的偏移位置)
段的属性：
    CONTENTS：表示该段在文件中存在
    ALLOC :表示只分配了大小，但没有存内容

关于.bss段，我们说.bss段是存放未初始化的全局变量(静态与非静态)和局部静态变量的，
所以我们程序中的g_var2和stactic_var2应该都在.bss段中被预留位置，所以.bss段的size应该是8个字节，
但是结果却是4个字节，怎么回事呢？这就是不同的编译器实现不一样的原因了，有些编译器会将未初始化的
全局非静态变量放在.bss段，有些则不放，只是预留一个未定义的全局变量符号，等到最终链接成可执行文件的
时候再在.bss段分配空间。而我的编译器是没有将g_var2（全局未初始化的非静态变量）放在任何段下面，
让我们真正的查看一下g_var2，首先，我们使用  readelf -S  test.o  查看段表（主要为了查看每个段的段号）
然后我们再使用 readelf -s  test.o看一下符号表（我们定义的变量名都是符号，包括函数名）
符号表里会显示这个符号所在的位置。
我们看到static_var1和g_var1所在段的段号为3（3是.data段），static_var2所在段的段号为4（4是.bss段），
而g_var2却没有被放入任何一个段，只是用COM标记了一下，那这个COM表示什么意思呢？COM标记的符号被称为弱符号，
一个变量名是弱符号，则这个变量的大小在编译的时候不能被确定，而在链接之后才能确定该变量的大小。
test.o文件在链接之后，g_var2会被放入.bss段（当然，也只是说明g_var2所需要的空间大小，并不会存放内容），
而在程序运行的时候g_var2这样的变量才会真正去占用内存空间。
强制将某变量或者某函数放入某个段，__attribute__((section(".data")))  int   g_var2;   //强制将g_var2放入.data段中

各种变量所在位置总结
    全局已初始化非静态变量、局部已初始化静态变量会被放入.data段
    全局未初始化静态变量会被放入.bss段
    全图未初始化非静态变量不会被放入任何一个段，只是用COM标记一下


举例5>python调用.so动态链接库的基本过程
【在python需要用到外部的C文件和C++文件，这里主要是想使用C和C++中的函数，我们需要将这些文件封装成so的动态链接库文件。
python加载动态库方面是默认从系统lib库上查找库文件。我的目录在当前目录下，所以需要从libdy.so变为./libdy.so】
动态链接库在Windows中为.dll文件，在linux中为.so文件。以linux平台为例
说明python调用.so文件的使用方法。本例中默认读者已经掌握动态链接库的生成方法，
如果不太清楚的可以参考《动态链接库的使用》，调用上例动态链接库的使用中的 sum.so：
import ctypes
so = ctypes.CDLL('./sum.so')
print "so.sum(50) = %d" % so.sum(50)
so.display("hello world!")
print "so.add() = %d" % so.add(ctypes.c_float(2), ctypes.c_float(2010))

输出结果如下：output
so.sum(50) = 1275
hello world!
so.add() = 2012

注意：如果python在调用C函数内部出现了问题，系统不会提示具体出现什么问题，
只会提示"segmentation fault"。所以最好是先用C语言调用该动态库验证没有问题了再提供给python调用。
python传参给C函数时，可能会因为python传入实参与C函数形参类型不一致会出现
问题( 一般int, string不会有问题，float要注意 )。这时需要在python调用时传入的实参
做一个类型转换(见so.add(float, float)函数的调用)。转换方式见下表：

数组的传入传出，如果将python中list传入C函数数组，则需要提前转换。
import ctypes
pyarray = [1, 2, 3, 4, 5]
carrary = (ctypes.c_int * len(pyarray))(*pyarray) //有点类似malloc的方式生成carray
print so.sum_array(carray, len(pyarray))
refer

如果如果需要将C array返回python，需要提前把array传入，然后在C函数中修改，
返回时再把c array转换为np.array
pyarray = [1,2,3,4,5,6,7,8]
carray = (ctypes.c_int*len(pyarray))(*pyarray)
so.modify_array(carray, len(pyarray))
print np.array(carray)

output，[10 20 30 40 50 60 70 80]

也可以用形参方式提前定义函数接口，然后再传入numpy结构
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
so = ctypes.CDLL('./sum.so')
pyarray = np.array([1,2,3,4,5,6,7,8], dtype="int32")
fun = so.modify_array
fun.argtypes = [ndpointer(ctypes.c_int), ctypes.c_int]
fun.restype = None
fun(pyarray, len(pyarray))
print np.array(pyarray)
注意：numpy中的数据类型指定很重要，即dtype的设定

图片的传入传出，转递数据域。背景知识：python中的opencv图片是用numpy的方式保存的，
而opencv3 C语言的图片数据结构为cvMat (IplImage已经逐弃用)所以需要把python中numpy图片
转换为ctypes.POINTER(ctypes.c_ubyte)的指针转入其数据域，再将其行列信息传入，
就可以在C中从最底层初始化一个CvMat，如果要初始化一个别数据结构的图片也是同理
(如darknet的image,caffe的blob)

python numpy image 转换为 C pointer的方法，
python_frm.ctypes.data_as(C.POINTER(ctypes.c_ubyte))
注意：传入numpy image前一定要确保numpy image是numpy array数据类型
比如我遇到的bug
image = cv2.imread("xxx.jpg");
image传入ctypes_so.fun之中图片是有效的，但
image = whl_img[y1:y2, x1:x2]
这时候进入ctypes_so.fun的图片会变成一个乱码
即，crop之后的numpy image的type虽然也为numpy array，但实际传入的image data却不正确
解决方法：无论是何种方式得到的numpy image，都强行转换为numpy array，再传入ctypes_so.fun
image = numpy.array(image)    可以解决这个bug
refence

如果使用opencv2 可以考虑直接将numpy image转换为IplImage，opencv3 python已经
不支持cv2.cv的函数了，但Opencv2可能还可以尝试以下方法：numpy image to iplimage

python调用C++中的类：因为python不能直接调用C++中的类，所以必须把C++中的类转换为C的接口。
转换原则，所有的C++关键字及其特有的使用方式均不能出现在.h文件里，.h中仅有C函数的包装函数声明
在class.cpp中实现对类的成员函数接口转换的函数，包括对类内成员的读写函数get() and set()
如果要在包装函数中要实例化对象，尽量用new constructor()的将对象的内存实例化在堆中，否则对象会被析构
记得在所有包含函数声明的文件中加入以下关键字，声明该函数为C函数，否则该函数的符号不会记录在二进制文件中
#ifdef __cplusplus
extern "C" {
#endif
xxxxxx function declaration xxxxx
#ifdef __cplusplus
}
#endif
code
refer
refer


举例6>Android和Python之间的不能说的小秘密   2017年08月15日 21:14:29 python热爱者 阅读数：13193
看到这个标题，大家可能会认为就是Android运行python脚本，或者用python写app，这些用QPython和P4A就可以实现了。
我在想既然C可以调用Python，那么Android能不能通过JNI去调用C里的方法，C再去调用Python方法，实现Android与Python交互呢？
用最近很热的一个概念来说JNI就是个壳。（本文假设大家有JNI开发基础）

Python C，Python C是C语言调用Python的一组API，通过它我们可以调用到Python方法。
Python C开发步骤：
引入头文件Python.h;
初始化python（Py_Initialize();）
引入模块（pModule = PyImport_Import("pythoncode");）
获取模块中的函数（PyObject_GetAttrString(pModule, "hello");
调用获取的函数（PyEval_CallObject(pFunction, NULL);
释放python（Py_Finalize();）
对应的代码如下：……
当然，直接运行这段代码会报错，因为Python.h找不到还有相应的lib找不到，这里强烈建议使用mac或者Linux开发！！！
填坑效率会比Windows高好多。具体怎么样处理这里先不说，如果实在需要，留言给我，我会另开一篇博文，
毕竟这里是讲Android调用python的，而这个是在桌面环境下C调用Python的，而且百度也很多。

JNI Python C，
当我成功使用C语言调用Python之后，我着手在JNI开发里调用Python，Python文件放在assets中 。
但是在开发过程中遇到了以下几个问题：头文件找不到（Python.h）；没有移动平台的python.so；兼容性；找不到.py文件。
接下来一个一个填坑。
头文件找不到（Python.h）  在MK文件中添加引用  include $(CLEAR_VARS)  ，这段代码其实也把下一个问题解决了。
另外我们刚项目开始的时候可能为了开发方便，会在gradle中配置JNI资源文件夹路径，可是这导致了run project的时候
AS也会对其中的C文件进行语法检查，这样由于没有外部头文件依赖，编译不会通过，
所以我们需要在gradle中把JNI资源文件夹删了，用[]代替  sourceSets.main {

当我们编译成功SO库之后，C文件在运行中并不会被调用，而是调用编译为.so的文件中的方法。
没有移动平台的python.so，想要运行Python必须要有解释器，Android本身没有带，所以我们需要在程序中内嵌一个解释器，
可是苦于找不到合适的so库，曾把P4A的python编译了一次，可是版本兼容性差，可用性不高。直到找到了Crystax NDK，
它在10.3之后已经开始支持python for Android了，而且这个NDK资源包还填了几乎所有Android调用python的坑，
包括第一个找不到头文件的问题，兼容的问题。在MK文件中，我们还需要加一段代码，编译crystax so库。include $(CLEAR_VARS)

兼容性，Android目前有7个常见平台需要适配，其余的都没问题，只有X86和X86_64的有问题，推测crystax NDK Windows还没完善，
因为mac下是可以直接编译的，所以有关编译的东西最好用Linux和Mac，Windows下我删了一个头文件，就可以运行了，没有发现异常
具体哪个我忘了，不过运行时报错哪个就去相应的文件里把头文件依赖删了就行，就一个。
然后生成7个平台的so库只需要在Application.mk中添加以下代码即可(APP_PLATFORM看个人调节)：
APP_PLATFORM := android-19APP_ABI := armeabi-v7a armeabi mips mips64 arm64-v8a x86 x86_64

找不到.py文件，不知道什么原因，assets文件夹里的py文件获取不到，似乎是不能识别asset路径？求大神告知。
解决方法就是把assets文件夹里的文件复制到设备的data文件夹里，再进行初始化。
JNI C代码：……
Python方面就是个简单的hello函数，返回“hello”字符串。

优化，当我把上述问题一一解决之后，终于见到之前写的python代码里返回的hello语句了。可由此也出现了一个问题，
当我调用Python方法的时候，必须先引入模块，再引入方法，而且当我们需要添加Python方法的时候，我们还要去写重复的调用方法，
只是换个方法名，而且需要再次编译各平台so库，我就想有没有一种方法可以只修改Python方法和java调用方法，而不去动C方法呢。
修改后的流程图如下：

优化后流程
Python端增加一个路由方法，再写一个函数字典，把所有方法都加到字典里，C里调用的就是这个路由方法，
java端调用的时候传入json里面包含了所需python方法，当json传入python中路由方法之后，自动匹配到相应的方法，
每次添加新的方法只需要在python中添加字典已经方法，java调用时传入新的方法即可。
Python路由方法：
def router(args):
Python函数字典：
routes = { 'hello': hello, 'add': add, 'mul': mul,
JNI C调用python方法：
JNIEXPORT jstring JNICALL Java_com_jcmels_liba_pysayhello_PyBridge_call
java调用：
json.put("function", "hello");
后记
到此，Android call Python就基本完成了，调用第三方库的话只需要把ctype文件
（Crystax文件夹中的sourcespython.5libs对应平台modules_ctypes.so）放到assets文件夹中就可以
通过cdll.LoadLibrary来调用第三方库了。在此感谢joaoventura大神的指导！


举例7>可运行于Android的Python解释器  2017年03月06日 22:12:34 srplab1 阅读数：4021 标签： androidpython
  本文一个运行于android的python解释器的例子，版本为python2.7，也可以是其它版本，Python共享库采用NDK编译。
  这里的例子为了说明如何初始化python解释器，运行python脚本，例子中的界面比较简单，一个输入栏用于输入python脚，
  一个输出栏用于显示运行的结果。Android代码基于java，需要通过java调用python。
  这里Python解释器基于cle开发，提供了java到native的双向调用。首先需要初始化cle，然后加载和初始化python解释器，
  最后是获取输入的脚本并捕获输出结果。
  
  
  
举例8>CLE框架下导入Python第三方库
前面的博客已经讲过了怎么使用CLE框架，在Android项目中嵌入Python解释器，但是有一些细节，很多人还不清楚
Android 工程的ibs目录中放的libpython3.4m.so是什么？
要回答这个问题，首先要了解Python解释器的源码结构。Python解释器源码可以从官网下载，也可以从Github上下载 Python解释器源码

划去一些无关的内容，具体说一下结构
Include：包含Python提供的所有头文件，如果需要自己使用C/C++编写自定义模块扩展Python，就需要用到这写头文件
Lib： 由Python语言编写的所有标准库
Modules：包含了标准库中所有使用C语言编写的模块
Parser：对Python代码进行词法分析和语法分析的部分
Objects：所有Python的内建对象
Python：Python运行的核心。解释器中的Compiler和执行引擎部分
如果对源码学习感兴趣，推荐一本书《Python源码剖析》，看过之后会受益匪浅，特别是对想自己改写Python解释器的人
那么回到我们的话题，libpython3.4m.so实际上只是Parser、Objects、Python以及一小部分Modules编译出来的动态库，只是提供了Python解释器的核心功能。如有时间，在以后的博客，我会详细讲解，如何手动用NDK，使用Android.mk文件以及Makefile文件，分别在Windows系统和Ubuntu系统上交叉编译出完整的在Android上运行的Python so库。
为什么使用CLE框架集成Python解释器后，有些标准库报找不到错误？
看博客不细心的人，可能没有注意到一张图，这里面放的so是什么？

我们打开下载的CLE文件starcore_for_android.2.6.0，进入里面的python.files目录下面，一路下去找到一个叫lib-dynload的目录

可以看到，里面放了一堆so库，这个就是上文讲的Modules里面编译出来的Python标准库，这些Python的标准库都是用C语言写的，CLE框架中，将Modules里面的标准库模块都编译成了一个个小的so，这样做的好处就是可以按需集成，我们知道Android的Apk文件都是要尽可能小的，你没有用到的模块，可以不用集成到apk中，否则全部打包到libpython.so中，无端增加了apk大小。
好了，到此铺垫都讲完了。现在具体谈一下装载Python库的思路
1.将需要的Python库打包到工程的assets目录下，在适当的时候，将assets目录下的文件都拷贝到手机存储中，这个存储可以是sdcard，也可以是内部的/data/data/package-name下
2.在需要引入这些库的时候，使用我们一开始讲的方法，将路径添加到Python的模块搜索列表——sys.path列表，让解释器能搜索到它们。
下面我们以一个实例来具体说明，这次我们需要移植的是爬虫需要用到的两个库，requests和BeautifulSoup，有了这两个库，我们瞬间就能将废旧的Android手机制作成Python爬虫机，老机器焕发新生命，怎么样激不激动？
1.打包库
如果我们本地Python环境中已经安装了这些库，可以直接去Python的库目录打包，因为这些库基本是纯Python代码，是跨平台的，当然，别把Python2.x和Python3.x搞混。如果没有安装，去相关的官网下载它们的源码打包。


很多人可能不知道，Python本身就是支持导入zip格式的包的，不信的同学可以自己在本地实验一下，将自己写的库压缩为zip，然后依然可以愉快的import。以上包中，python3.5.zip是纯Python代码的标准库，在CLE里面已经提供了，唯一需要说明的地方，是certifi库为什么没有打包，而是以目录形式提供呢？这里也正是我采坑的地方，之前试验一直报错没有成功移植requests库，就是因为打包了certifi，后来反复测试定位到该包，发现里面有一个cacert.pem文件，不是.py文件，在压缩包中无法被读取，因此只能以文件夹形式提供了。
另外还有一个小点说一下，相信绝大部分人不会犯错，但总有粗心大意的。打包的时候，要打包这个库的源码父目录，就像certifi一样，是打包这个certifi目录，而不是进到certifi里面，选中所有文件压缩。之前一个同事就是犯这种错误，一直和我说不成功。
2.递归拷贝
在工程的assets目录创建python文件夹，将所有包复制进该目录，在app启动的适当时候，调用以下代码拷贝assets中的所有文件到手机存储
		// Extract python files from assets
        AssetExtractor assetExtractor = new AssetExtractor(this);
        assetExtractor.removeAssets("python");
        assetExtractor.copyAssets("python");

        // Get the extracted assets directory
        String pyPath = assetExtractor.getAssetsDataDir() + "python";
1
2
3
4
5
6
7
AssetExtractor类在Android 平台的Python——JNI方案（二）一文已经提过了，这里再次给出开源库中的
链接 这里只有一点需要特别说明，在刚开始的时候我准备剪裁lib-dynload文件夹提供的C语言部分的Python标准库，结果试验性的放了几个so，一直报各种找不到错误，最后不想浪费时间试错，直接将lib-dynload中的所有so拷贝到了assets/python文件夹，有时间的朋友可以精心剪裁出真正需要的so，减小apk体积。
3.添加库到搜索路径中
还没看过CLE使用的那篇博客，请先浏览CLE的使用一文Android 平台的Python——CLE方案实现（三）
另外需要注意的是在Android清单文件中，网络权限别忘了
<uses-permission android:name="android.permission.INTERNET" />
protected void init() {
        final String appLib = getApplicationInfo().nativeLibraryDir;
        AsyncTask.execute(new Runnable() {

            @Override
            public void run() {
                loadPy(appLib);
            }
        });
    }

    void loadPy(String appLib){
        // Extract python files from assets
        AssetExtractor assetExtractor = new AssetExtractor(this);
        assetExtractor.removeAssets("python");
        assetExtractor.copyAssets("python");

        // Get the extracted assets directory
        String pyPath = assetExtractor.getAssetsDataDir() + "python";

        try {
            // 加载Python解释器
            System.load(appLib + File.separator + "libpython3.5m.so");
        } catch (Exception e) {
            e.printStackTrace();
        }

        /*----init starcore----*/
        StarCoreFactoryPath.StarCoreCoreLibraryPath = appLib;
        StarCoreFactoryPath.StarCoreShareLibraryPath = appLib;
        StarCoreFactoryPath.StarCoreOperationPath = pyPath;

        StarCoreFactory starcore = StarCoreFactory.GetFactory();
        //用户名、密码 test , 123
        StarServiceClass service = starcore._InitSimple("test", "123", 0, 0);
        mSrvGroup = (StarSrvGroupClass) service._Get("_ServiceGroup");
        service._CheckPassword(false);

        /*----run python code----*/
        mSrvGroup._InitRaw("python35", service);
        StarObjectClass python = service._ImportRawContext("python", "", false, "");
        /* 设置Python模块加载路径 即sys.path.insert() */
        python._Call("import", "sys");
        StarObjectClass pythonSys = python._GetObject("sys");
        StarObjectClass pythonPath = (StarObjectClass) pythonSys._Get("path");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"python3.5.zip");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"requests.zip");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"idna.zip");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"certifi");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"chardet.zip");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"urllib3.zip");
        pythonPath._Call("insert", 0, pyPath+ File.separator +"bs4.zip");
        pythonPath._Call("insert", 0, appLib);
        pythonPath._Call("insert", 0, pyPath);

        python._Set("JavaClass", Log.class);
        service._DoFile("python", pyPath + "/test.py", "");
        Log.d("callpython", "python end");
    }
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
5在Crytax-NDK的Python中集成第三方库
有了CLE，我为什么仍然执着于Crytax-NDK中的Python解释器了？说实话，我并不是特别喜欢CLE，因为它封装了太多细节，且源码并未开源，具体实现代码不知，性能就无法掌控，特别是无用代码，导入一些非必要的so和jar，增加了apk体积，因为这个框架并不是专门针对python的，还可以集成其他的很多脚本语言到Android中，为了通用性，往往就需要很多对我们来说无用的代码，性能也会有牺牲。但是它的优点也很明确，那就是使用简单，不需要你会Ndk开发，技术成本低。
使用Crytax-NDK实现，具体思路和上面讲的是一样的，直接参看Android 平台的Python——JNI方案（二）一文，然后将需要的第三方库源码打包安装到手机存储，需要注意的地方就是在调用的Python脚本的开始处，加上以下代码，也可以使用其他更优雅的方式，完成这个搜索路径添加，这里只是一个简单的demo代码演示。
import sys
sys.path.append("你拷贝到手机上的路径/assets/python/urllib3.zip")
sys.path.append("你拷贝到手机上的路径/assets/python/chardet.zip")
sys.path.append("你拷贝到手机上的路径/assets/python/certifi")
sys.path.append("你拷贝到手机上的路径/assets/python/idna.zip")
1
2
3
4
5
但是，但是……
HTTPSConnectionPool(host='www.baidu.com', port=443): Max retries exceeded with url: / (Caused by SSLError("Can't connect to HTTPS URL because the SSL module is not available.",))
1
这里有一个极其操蛋的问题，使用requests访问https的地址时，会报错，只能访问http地址。因为Crytax-NDK库的Python解释器编译得有问题，没有支持openssl，真不知道Crytax-NDK的作者怎么想的，由于Crytax-NDK是开源的，我好不容易找到了其源码，查看了他们编译Python解释器的脚本，真让人无语，不能访问https的Python有什么用？

可以看到，在编译ssl模块时，加了一个OPENSSL_HOME属性控制，即有ssl源码时，就编译这部分，否则跳过，然而Crytax-NDK里面openssl的目录是空的，所以最后生成的Python一系列so中，唯独没有ssl的so。尝试从其他地方拷贝一个ssl的so是不可行的，因为他们的Python解释器里，ssl的属性是没有enable的，你拷贝了解释器也并不会去链接，然并卵，看来只能手动重新编译这个Python解释器了，但是手上没有搭建环境，光环境搭建就得折腾一番，下次博客在写吧，下次的博客我主要讨论一下，自己手工编译解释器，然后运用cython模块编译pyjnius库，实现纯手动在Android搭建一个python.so+ pyjnius.so的环境，实现简便的Java与Python的互操作，有了它，CLE基本可以扔掉了。如果不知道pyjnius，请谷歌。
最后，如果您觉得我的博客对您有用，看过之后，麻烦点个赞，毕竟顶一下又不会怀孕，因为很多人看过之后，也没有一点表示，不管怎么说，写博客既花时间，也耗费一点精力，毕竟也是在分享知识啊，在这个知识付费的时代，免费分享也不易，点个赞，只是鼠标一抖的事而已，谢谢！


Android 平台的Python——编译Python解释器
2018年09月24日 19:58:44 血色--残阳 阅读数：473
版权声明：本文为博主原创文章，转载请注明出处。http://blog.csdn.net/yingshukun https://blog.csdn.net/yingshukun/article/details/82830215
要想将Python解释器移植到Android平台，首先要做的就是将Python源码用NDK工具交叉编译为Android平台的二进制库。目前官方是没有提供对Android平台的支持的，但新的版本已经在考虑对Android提供支持，参考文档 API 24 is the first version where the adb shell is run on the emulator as a shell user instead of the root user previously, and the first version that supports arm64.
Android不是常见的Linux系统，只有Linux内核是共享的，其他一切都是不同的，它使用的C标准库是Bionic，与glibc有很大差异，因此直接使用NDK编译源码会报错。
上一篇博客已经谈到了关于Python第三方库移植的问题，但是 CrytaxNDK中的Python解释器存在一些问题，未支持SSL，导致无法访问HTTPS，这次我们先使用CrytaxNDK重新编译Python


"""
