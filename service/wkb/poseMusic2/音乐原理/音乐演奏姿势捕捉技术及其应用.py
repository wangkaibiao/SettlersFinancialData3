#音乐演奏姿势捕捉技术及其应用
"""
时间：2018-06-05 08:25:14   来源：中国演艺科技网   作者：梁晓晶
在音乐演奏中，演奏者的表演姿势对于音乐情感的表达具有重要的作用。关于音乐与姿势（gesture）的关系，自20世纪90年代以来有着较为集中和广泛的讨论，其中较为著名的学者为加拿大麦吉尔大学的Marcelo M.Wanderley教授，他曾在国际范围内多次领导和组织了与音乐姿势相关的会议和讨论，并拥有诸多研究成果。

现代国际上关于音乐与姿势的研究主要分为两类，一类研究着眼于演奏姿势与音乐表达之间的关联，其中包含演奏姿势与声学特征的关系、演奏者个性化的演奏习惯、以及某种风格或作品演奏中具有共性的姿势等，该类研究主要运用在音乐信息检索领域以及器乐的可视化教学中；另一类研究则将姿势数据转化为交互式音乐表演或新型乐器的输入参数，通过设计姿势数据与声音参数的映射关系，进行由姿势控制声音的交互设计探索。对音乐演奏姿势进行采集和分析，不仅可以为音乐表演的研究和教学提供便利，还可以为新型乐器的设计以及音乐信息学的研究提供更为丰富、立体的视角。本文着重从音乐演奏姿势的捕获技术和应用两大方面分别进行介绍。

1 音乐演奏姿势的捕捉技术

音乐演奏过程中，演奏者通过不断地控制和调整自己的肌肉紧张程度以及各个关节的空间位置及运动速度来使乐器（或嗓音）发出声音，传达音乐的情感或意图。在这一过程中，音乐演奏的主体是人，音乐演奏姿势捕捉技术也主要来自于人机交互领域对于人体动作的捕捉技术。

一般而言，要捕捉人体的运动姿势，必须在一个固定的空间内测量身体每一个部分线性及角度的运动情况，通过空间和角度信息，便可以得到各个相邻关节的相对角度、速度以及加速度。在空间位置、角度、速度和加速度这几种信息中，并非所有的信息都一定需要直接测量得到，通常只需要在位置、速度、加速度中直接获取其中一个信息，其他信息由运动变量通过数学方法计算出来。

在一些运动捕捉的应用中，人的整个身体被看作一个质点，例如在小组体育运动中，人们倾向于忽略关节之间的相对运动，更加关注宏观尺度的运动信息。而在音乐演奏姿势中，人们关注的信息往往是较为微观的运动，正是这些微小的动作差别，导致了演奏出的音乐“味道”的差异，将专业演奏家和普通演奏者区分开来。

在音乐表演中，虽然绝大多数表演形式都涉及到共同的身体部位，如手指、上肢、腰部，带踏板及打击类乐器可能还涉及下肢运动，但它们对演奏的重要程度可能并不相同。例如，在弓弦乐器中，持弓的手腕关节、肘关节、肩关节前后的身体部位以及左手掌指部分运动可能对于音乐情感的表达具有更为重要的作用；而在吹管乐器中，手腕关节的运动复杂程度可能不及弓弦类乐器，对音乐表达的影响则没有那么显著。在另一些情况下，一些肢体运动是演奏家的个人喜好，但它们对于音乐本身的表达可能并不起特殊的作用，可以称作“非音乐相关姿势”，例如一些爵士钢琴演奏家有一只脚打节奏的习惯，再如摇滚吉他手有时会为了现场气氛增加一些较为夸张的表演性动作，这些动作如果去掉或者幅度减小，并不影响音乐在声音上的效果。

按照演奏姿势被识别的方式，音乐表演姿势的捕捉技术主要分为直接识别、间接识别以及生理信号识别三类。

直接识别：直接识别采用压力、线性位移、角度位移、加速度传感器以及摄像头加机器视觉的方法进行数据处理，直接获得关于身体部位的运动信息。直接识别相比于间接识别获取数据更加简单，且这些变量是相互独立的，不会互相干扰，故可获得独立的数据流，但缺点也正是由于其独立性，可能会低估各种变量之间的相互依赖关系。此外，麦吉尔大学的Anne-Marie Burns博士采用机器视觉的方法，利用摄像头进行图像特征的提取，进行吉他左手演奏姿势的研究。

间接识别：间接识别，是指通过提取声音信号中的结构性信息来反推姿势数据，利用信号处理技术，分析声音的基频、短时能量、频谱包络、振幅、调制深度等，得出演奏者的姿势信息，此时，姿势识别系统的传感器就是传声器。由于音频信号的复杂性，通常需要使用多种技术将由演奏动作引起的效果与其他因素引起的效果区分开来，如室内声学特性或乐器自身特性。对于一些姿势参数，往往首先用加装传感器的测量系统对某种姿势所对应的声学特征进行研究分析，再采用结构性的分析方法或者机器学习的方法，利用计算机进行处理判断姿势运动的情况。例如，在伦敦大学玛丽女王学院数字音乐中心的梁贝茨所做的研究中，研究者使用了在键盘和踏板处分别安装有触摸式传感器和位移传感器的特制钢琴，声音信息和踏板位移信息通过高质量、超短时响应的音频计算平台Bela将传感信号传入计算机。通过研究踏板与音频声学特性的关系，实现对于一段给定音频，系统可较为准确地判断出何处踩了踏板以及其踩下的深度。

生理信号识别：生理信号识别最为典型的是表面肌电信号（EMG），目前表面肌电测量采集系统已有许多商业化的产品，这些系统大多为运动学研究而设计，精度已达到较为理想的程度，常常为提高运动训练的精确度提供辅助。在音乐表演中，肌肉力量的提高以及学会某些肌肉的放松往往是需要花很长时间进行体会的，例如钢琴演奏时，初学者往往很难做到手臂和手腕关节及其相关肌肉的放松，弓弦类乐器学习过程中，上肢肌肉的控制也需要长时间的练习和体会。

2 音乐姿势捕捉技术的应用

以下主要从音乐辅助教学、音乐信息检索以及交互式声音装置设计三个领域来介绍姿势捕捉技术在音乐领域的应用。

2.1音乐辅助教学

演奏姿势对乐器的演奏具有重要影响，琴童们每天长时间练琴，有很大一部分的精力实际是在建立肌肉的记忆，若能在学习的早期阶段，尽快采用技术手段介入到器乐学习者的姿势引导和实时反馈上，会对训练的效率有所提升。2017年的国际新型音乐表达接口会议（NIME: New Interface for Music Expression）上，有研究者为长笛加装多种传感装置，设计了乐器增强的功能，从嘴唇的放置位置、吹气气流的角度、唇孔形状等角度对初学者的演奏状况进行实时可视化，帮助初学者更快吹出稳定的声音。近年来，麦吉尔大学对吉他、打击乐器、单簧管等乐器的演奏姿势进行研究分析，还运用三维重建技术将演奏者的演奏动作进行重建，使人能更加直观地重现演奏家的演奏姿势。此外，辅助钢琴、小提琴以及指挥的系统也已经有相关研究，并正逐步商业化进入到大众的音乐生活中。

2.2音乐信息检索

音乐信息检索（MIR: Music Information Retrieval）是指提取音乐中信息的技术，涉及音乐声学、信息学、音乐学、心理学等学科，是一个蓬勃发展中的交叉领域，其应用包含音乐推荐系统、多轨音频分离、自动音乐记谱、音乐自动分类、自动音乐生成等。

在前文描述的间接识别中，研究者首先邀请多位钢琴家在踏板以及键盘表面安装有多种传感器的“增强钢琴”上演奏，采集演奏姿势数据，之后通过机器学习的方法，让计算机自动把演奏时的姿势参数分析出来，这是一个“系铃”和“解铃”的过程。在这个过程中，音乐姿势捕捉的数据成为了进行该项音乐信息提取的前期工序。

另一项较为精细的演奏姿势研究是2017国际计算机音乐会议（ICMC：International Computer Music Conference）上的古琴左手姿势研究。来自新加坡和新西兰的研究者研制了一副具有内含多类传感器的手套，他们对三位专业古琴演奏者的左手姿势数据进行了采集。该手套在除去大拇指的四个手指的指掌关节处，放置有微型的二轴加速度传感器及陀螺仪，其中加速度传感器记录手指左右、上下两轴空间移动，陀螺仪记录旋转角度，设计时考虑尽可能减少手套对古琴演奏者的影响，故采用非常微型的传感器，并通过无限传输模块传送给计算机进行处理（图1）。该研究的主要目的在于探讨这套姿势识别系统是否能够对古琴的左手演奏技法进行自动分类和识别。结果表明，该姿势识别系统识别五项左手技法的正确率大于85%。



2.3交互式声音装置设计

利用运动姿势来控制声音的参数最早从国际上人机交互领域的讨论分离出来，成为一个单独的领域。在该类装置设计中，人体的运动姿势由动作捕捉系统捕捉，由输入设备输送给动作识别系统进行识别，再将各运动参数映射到不同的声学参数上（例如音高、音量、音色、混响时间等），最终通过发声系统发出声音。以ICMC的案例为例，古琴姿势识别系统设计者还创作了这样一部作品，一位古琴演奏者现场佩戴含有12个传感器的手套演奏古琴，传感器的参数通过无线传输方式传入计算机后，由Max/MSP进行数据处理，并导出给另一台控制声音机械装置的计算机。该计算机将传感器数据映射至多个机械动作，通过单片机控制舵机驱动多个声音装置发出声音。其中一个线性位移驱动机连接有不锈钢的“止音棒”，利用安装在舵机上的吉他拨片，配合止音棒，机械可以拨弦发出一定音高的声音。但由于没有设计共鸣腔，现场更多的是听见舵机带动拨片和止音棒的声音，作品构成了古琴与现代机械声相互交错的“古今之声”，颇有趣味。

在一位意大利人的作品中，创作者利用MyoSpat手环测量肌电数据，竖琴演奏者的左手肌电信号传输给映射工具，映射后的数据进入Pure Data传送给扬声器，同时将灯光控制信号输送给灯具控制颜色等参数，实现动作、音乐与灯光的相互关联。

由达特茅斯大学Bregman工作室的樊健宇设计的“声太极”（Sonic Taiji），利用手机自带的陀螺仪、加速度传感器，将手机附在表演者的手上进行姿势采集，使演奏者在练习太极拳的过程中，还能获得听觉上的享受。

虽然利用人体姿势数据的交互作品层出不穷，但部分作品设计仍有生硬之感，如何将人体的姿势动作与声音以及人们的心理预期有机地结合起来，创作出具有趣味性的作品仍是一个值得深入思考的问题。用于音乐表达的输入系统的评价方面，学术界也一直展开着讨论。2002年，由Marcelo M. Wanderley等人提出应将“易学性”、“探索性”、“可控性”、“时间控制性”等因素考虑进来，设计者可通过主观评价实验，及时对设计做出合理的评估和优化。

3 结语

正如美国文化学者Richard Leppert在《声音的模样：音乐、表示、以及身体的历史》（The Sight of Sound: Music, Representation, and the History of the Body）一书中所说，“正因为音乐的声音是抽象、无形和空灵的……产生音乐的视觉过程（即指演奏姿势随时间的演变）在该社会和文化背景下对于音乐家和观众，与进行音乐活动的空间和位置有同等重要的地位……音乐，虽然是关于声响的精妙艺术，但它仍与舞蹈和戏剧类似，是一项可具象化的活动。”21世纪以前的音乐学研究中，身体姿势与音乐的关系始终没有得到足够的重视。然而，随着姿势捕捉技术的日趋成熟以及人体动作与乐器发声的过程可以相互独立开来，人们已经可以以新的视角来审视音乐与姿势的关系。相信在未来，演奏姿势捕捉技术可以服务于更多的音乐学习者、艺术创作者及乐器设计者，将人们引向更加丰富、精彩和饶有趣味的未来。

选自《演艺科技》2018年第5期  梁晓晶《音乐演奏姿势捕捉技术及其应用》，转载请标注：演艺科技传媒。更多详细内容请参阅《演艺科技》。"""
