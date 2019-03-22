# -*- coding: utf-8 -*-
"""
所有的tensor都要命名便于索引和使用，所有的程序都可以放在session中设计，
计算图可以保存和继续训练的关键在于变量tensor的命名始终保持一致，
因为最终也是为了获得更合适的变量。

版本3的改进地方：1、参数初始化改为正太分布（0，1）；2、采用正则化方法增加泛化性能；
3、采用随步数而减小的学习率；4、适当引入tf的高层API；5、是否可以采用抽样降低
训练数据的不对称性造成的损失失衡？。【2、4、5】留着在下一版本中探索研究.
6、AdaGrad，一种先进的梯度下降法，用于重新调整每个参数的梯度，以便有效地为每个参数
指定独立的学习速率；7、特征组合 (feature cross)通过将单独的特征进行组合（相乘或
求笛卡尔积）而形成的合成特征。特征组合有助于表示非线性关系；8、梯度裁剪 (gradient 
clipping)在应用梯度值之前先设置其上限，梯度裁剪有助于确保数值稳定性以及防止梯度爆炸；
9、合页损失函数 (hinge loss)一系列用于分类的损失函数，旨在找到距离每个训练样本都
尽可能远的决策边界，从而使样本和边界之间的裕度最大化， KSVM 使用合页损失函数（或
相关函数，例如平方合页损失函数）；10、L1 损失函数 (L₁ loss)一种损失函数，
基于模型预测的值与标签的实际值之差的绝对值，与 L2 损失函数相比，L1 损失函数对
离群值的敏感性弱一些，L1 正则化 (L₁ regularization)一种正则化，根据权重的绝对值的
总和来惩罚权重。在依赖稀疏特征的模型中，L1 正则化有助于使不相关或几乎不相关的特征的
权重正好为 0，从而将这些特征从模型中移除，与 L2 正则化相对。L2 损失函数 (L₂ loss)请
参阅平方损失函数。L2 正则化 (L₂ regularization)一种正则化，根据权重的平方和来
惩罚权重。L2 正则化有助于使离群值（具有较大正值或较小负值）权重接近于 0，但又
不正好为 0。（与 L1 正则化相对。）在线性模型中，L2 正则化始终可以改进泛化。
11、对数损失函数 (Log Loss)二元逻辑回归中使用的损失函数。12、Metrics API (
tf.metrics)一种用于评估模型的 TensorFlow API。例如，tf.metrics.accuracy 用于
确定模型的预测与标签匹配的频率。在编写自定义 Estimator 时，您可以调用 Metrics API
 函数来指定应如何评估您的模型。13、小批次随机梯度下降法 (SGD, mini-batch 
 stochastic gradient descent)会根据一小部分训练数据来估算梯度。13、动量 (Momentum)
一种先进的梯度下降法，其中学习步长不仅取决于当前步长的导数，还取决于之前一步或多步的
步长的导数。动量涉及计算梯度随时间而变化的指数级加权移动平均值，与物理学中的动量类似
。动量有时可以防止学习过程被卡在局部最小的情况。14、时间序列分析 (time series 
analysis)；15、宽度模型 (wide model)一种线性模型，通常有很多稀疏输入特征。我们
之所以称之为“宽度模型”，是因为这是一种特殊类型的神经网络，其大量输入均直接与
输出节点相连。与深度模型相比，宽度模型通常更易于调试和检查。虽然宽度模型无法通过
隐藏层来表示非线性关系，但可以利用特征组合、分桶等转换以不同的方式为非线性关系建模。
与深度模型相对。16、Estimator (tf.estimator)	高级 OOP API。
tf.layers/tf.losses/tf.metrics	用于常见模型组件的库。
TensorFlow	低级 API
17、先映射到可视化空间、再分类；
"""

import pymysql as pdb
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from scipy.special import comb
#import statsmodels.api as sm #导入统计模型，可以和numpy、pandas紧密搭配使用


def to_db(db="fund_train"):
    return pdb.connect(host="localhost",
                      port=3306,
                      user="root",
                      passwd="123456",
                      db=db,
                      charset="utf8")

ft=to_db("wangkaibiao")
ft_cursor=ft.cursor()

ft_cursor.execute("show tables")
train_table=ft_cursor.fetchall()[0][0]
print(train_table)
  

def visual_bp_fund(X,Y,x_size=60,k1=1,k11=2,step=200*100,log_dir_n="aaa",
            lr=0.001,save="y",g_name="visual_bp_fund"):
    with tf.Graph().as_default() as g_name:
        samp_size=len(Y)
        Xtrain= tf.placeholder(tf.float32,[samp_size,x_size],
                                   name="Xtrain") 
        Ytrain= tf.placeholder(tf.float32,[samp_size,1],name="Ytrain")
        
        
        #①处理数据、先映射到二维空间
        weights1=tf.Variable(tf.truncated_normal(
                [x_size,x_size+1+k1],stddev=1.0),name="weights1")
           #切刀至高维面
        tf.summary.histogram("h_weights1",weights1)
        biass1=tf.Variable(tf.truncated_normal(
                [1,x_size+1+k1],stddev=1.0),name="biass1")
        tf.summary.histogram("h_biass1",biass1)

        neural_num=int(comb(x_size+1+k1,x_size+1))

        weights2=tf.Variable(tf.truncated_normal(
                [x_size+1+k1,neural_num],stddev=1.0),name="weights2")
           #组合高维面到高维体
        tf.summary.histogram("h_weights2",weights2)
        biass2=tf.Variable(tf.truncated_normal(
                [1,neural_num],stddev=1.0),name="biass2")
        tf.summary.histogram("h_biass2",biass2)
        
        weights3=tf.Variable(tf.truncated_normal(
                [neural_num,2],stddev=1.0),name="weights3")
           #高维体组合映射到二维空间
        tf.summary.histogram("h_weights3",weights3)
        biass3=tf.Variable(tf.truncated_normal(
                [1,2],stddev=1.0),name="biass3")
        tf.summary.histogram("h_biass3",biass3)
        
        
        #②再从二维空间划分（原理仍是重复上面）
        weights11=tf.Variable(tf.truncated_normal(
                [2,2+1+k11],stddev=1.0),name="weights11")
        tf.summary.histogram("h_weights11",weights11)
        biass11=tf.Variable(tf.truncated_normal(
                [1,2+1+k11],stddev=1.0),name="biass11")
        tf.summary.histogram("h_biass11",biass11)

        neural_num2=int(comb(2+1+k11,2+1))

        weights21=tf.Variable(tf.truncated_normal(
                [2+1+k11,neural_num2],stddev=1.0),name="weights21")
        tf.summary.histogram("h_weights21",weights21)
        biass21=tf.Variable(tf.truncated_normal(
                [1,neural_num2],stddev=1.0),name="biass21")
        tf.summary.histogram("h_biass21",biass21)
        
        weights31=tf.Variable(tf.truncated_normal(
                [neural_num2,1],stddev=1.0),name="weights31")
        tf.summary.histogram("h_weights31",weights31)
        biass31=tf.Variable(tf.truncated_normal(
                [1,1],stddev=1.0),name="biass31")
        tf.summary.histogram("h_biass31",biass31)       


        #③开始设计具体网络结构，首尾不变、变的只是中间的结构，也不影响数据结构
        l1_out=tf.tanh(tf.matmul(Xtrain,weights1)+biass1,name="l1_out")
        #tf.nn.relu    tf.sigmoid     # relu是激励函数的一种
        l2_out=tf.tanh(tf.matmul(l1_out,weights2)+biass2,name="l2_out")
        visual_predic_op=tf.nn.relu(tf.matmul(l2_out,weights3)+biass3,
                             name="visual_predic_op")
        tf.summary.histogram("visual_predic_op",visual_predic_op)
        
        l11_out=tf.tanh(tf.matmul(visual_predic_op,weights11)+biass11,
                        name="l11_out")
        l21_out=tf.tanh(tf.matmul(l11_out,weights21)+biass21,name="l21_out")
        predic_op=tf.sigmoid(tf.matmul(l21_out,weights31)+biass31,
                             name="predic_op")#加上这条才能在预测时调用
        tf.summary.histogram("predic_op",predic_op)
        
        loss = tf.reduce_mean(tf.square(Ytrain-predic_op),
                              name="loss_reduce_mean")
        tf.summary.scalar("s_loss",loss)
        tf.summary.histogram("h_loss",loss)
        
#            train=tf.train.MomentumOptimizer(lr,0.9).minimize(loss)
        train=tf.train.AdamOptimizer(
                learning_rate=lr,beta1=0.9,
                beta2=0.999, epsilon=1e-08).minimize(loss)
        
        merged = tf.summary.merge_all()
        #收集数据但也需要数据来计算，也是图的元素之一
        
        model_dir="a_fund_trade/tf_continue_train/"+log_dir_n
        saver = tf.train.Saver()#模型建立之后再定义saver
        with tf.Session() as sess:
            try:
                run="try"
                saver.restore(sess,model_dir+"/bp_fund-200")
                print("该步执行的是try加载参数模型")
            except:#★★★非常关键的一步：决定模型能否持续★★★
                run="except"
                tf.global_variables_initializer().run()
                print("该步执行的是except新建参数")
                
            writer = tf.summary.FileWriter(model_dir+"/",graph=sess.graph)
            
            for i in range(step):
#                lr_t=lr*(1-i/step)#学习率随步数减少，这种损失呈现线性递减
#                #还一种学习率是：lr/sqrt(i)，这种损失应该呈现非线性递减
#                train=tf.train.GradientDescentOptimizer(lr_t).minimize(loss) 
#                # 选择梯度下降法  
                sess.run(train,feed_dict={Xtrain:X,Ytrain:Y})  
                if (i+1)%200 == 0:
                    print(i,"步：学习率为 %s"%"lr_t",
                          " ；损失为 %s"%sess.run(loss,
                                              feed_dict={Xtrain:X,Ytrain:Y}))
                    rs=sess.run(merged,feed_dict={Xtrain:X,Ytrain:Y})          
                    writer.add_summary(rs,(i+1))
                    #writer必须配合独立新Graph使用，否则会报错没有给占位符传入数据 
                    if run=="try" and save=="y":
                        saver.save(sess,model_dir+"/bp_fund",
                                   global_step=200,write_meta_graph=False)
                    #此处的路径不能用占位符来替换、但能用加号连接字符串
                    #"+log_dir_n+"，否则运行之后会报错，也可能是write_meta_graph
                    #每次都操作的原因，所以加上if判断。此外文件夹名字不能太短
                    if run=="except" and save=="y":
                        saver.save(sess,model_dir+"/bp_fund",
                                   global_step=200,write_meta_graph=True)
            
            #训练结束，执行一次预测过程，如果结果太大就要避免计算占用过多内存            
            print("predic:","sess.run(predic_op,{Xtrain:X,Ytrain:Y})"
                  ,"__loss:",sess.run(loss,feed_dict={Xtrain:X,Ytrain:Y})) 
            #sess.close()#with情况下不需要


#运行上面的代码，在当前目录下新生成一个名为logs的文件夹，里边有汇总的记录
#打开cmd，加载D:\pymoney\DeepLearn35，输入tensorboard --logdir logs
#生成一个链接http://LAPTOP-CF0R75NC:6006，复制在google浏览器（火狐也行）粘贴显示


#实际训练学习
def average_continue_train(tb="1mon_ave_aft_2week_divided_3day_ave",smp=200000,
                           avg_rate=0.05,raten="3",
                   x_size=60,k1=1,k11=2,step=200*5,log_dir_n="aaa",lr=0.001,
                   save="y",g_name="visual_bp_fund"):
    count_sql='select count(*) from %s'%tb
    ft_cursor.execute(count_sql)
    count_train=ft_cursor.fetchall()
    batchs=count_train[0][0] // smp#整除是往上取，实际上是多出一部分的
    
    for i in range(batchs+1):
        #slsql="select * from grow_rate1 limit 7,6 "#从第8条开始取,取6条
        if i == batchs:
            break#不要尾巴数据了
#            samp_num=count_train[0][0]-smp*i                 
        else:
            samp_num=smp
        slsql="select * from %s limit %d,%d "%(tb,smp*i,samp_num)
        print(slsql)        
        ft_cursor.execute(slsql)#16613
        res=np.array(ft_cursor.fetchall())
        #准备训练的Y数据
        if raten=="3":#使用1个月比3个月的数据
            rate3_1=[eval(rate) for rate in res[:,1]]
#        max(rate3_1),min(rate3_1)# (0.63950136964548, -0.358762528334373)
        if raten=="2":#使用1个月比2个月的数据
            rate3_1=[eval(rate) for rate in res[:,2]]
        if raten=="1":#使用1个月比1个月的数据
            rate3_1=[eval(rate) for rate in res[:,3]]
        samples=len(rate3_1)##16613
#        plt.scatter(np.arange(0,samples,1),rate3_1)
#        plt.hist(rate3_1,bins=np.arange(-0.3,0.4,0.05))    
        Ytrain=np.zeros((samples,1))
        for i in range(samples):
            if rate3_1[i]>avg_rate:
                Ytrain[i]=1
#        plt.hist(Ytrain,bins=np.arange(-1,3,0.5))#1占25%左右        
        #准备训练的X数据
        nets=[eval(net)[0:x_size]  for net in res[:,2]]
#        nets[0]
        Xtrain=np.array(nets)
        #开始训练
        visual_bp_fund(Xtrain,Ytrain,x_size=x_size,k1=k1,k11=k11,step=step,
                       g_name=g_name,log_dir_n=log_dir_n,lr=lr,save=save)

        
def del_str_x(x_train,y_train):
#    tt=np.array(["1","2","我","4","5"]).astype("float32")
#    #ValueError: could not convert string to float: '我'
#    type(tt[0])#numpy.float32
#    type(x_train[0][0])#numpy.str_
#    x_train[0].astype("float32")#可以执行
#    np.shape(y_train)#(123170,)
#    np.shape(x_train)#(123170, 60)
#    test=np.delete(x_train,[1,2,3])
#    np.shape(test)#(7390197,)
#    test1=np.delete(x_train,[1,2,3],axis=0)#axis=0表示行，axis=1表示列
#    np.shape(test1)#(123167, 60)
    contain_str_index=[]
    i=0
    for x in x_train:
        try:
            x.astype("float32")
        except:
            contain_str_index.append(i)             
        i+=1
    new_x_train=np.delete(x_train,contain_str_index,axis=0).astype("float32")
    new_y_train=np.delete(y_train,contain_str_index,axis=0)
    return new_x_train,new_y_train,len(contain_str_index)
        
def max_continue_train(tb="grow_rate_randorder",smp=200000,max_rate=0.04,
                       raten="1",x_size=60,k1=1,k11=2,step=200*5,
                       log_dir_n="qqq",lr=0.001,save="y",g_name="bp_fund_max"):
    count_sql='select count(*) from %s'%tb
    ft_cursor.execute(count_sql)
    count_train=ft_cursor.fetchall()
    batchs=count_train[0][0] // smp#整除是往上取，实际上是多出一部分的
    
    for i in range(batchs+1):
        #slsql="select * from grow_rate1 limit 7,6 "#从第8条开始取,取6条
        if i == batchs:
            break#不要尾巴数据了
#            samp_num=count_train[0][0]-smp*i                 
        else:
            samp_num=smp
#        i=0
        slsql="select * from %s limit %d,%d "%(tb,smp*i,samp_num)
        print(slsql)        
        ft_cursor.execute(slsql)#16613
        res=np.array(ft_cursor.fetchall())
        #ValueError: could not convert string to float: 
        #说明里边肯定有字符串
#        type(float(res[:,1:2][0][0])-1)
        if raten=="3":#使用1个月比3个月的数据
            y_train=res[:,3:4]
#        max(rate3_1),min(rate3_1)# (0.63950136964548, -0.358762528334373)
        if raten=="2":#使用1个月比2个月的数据
            y_train=res[:,2:3]
        if raten=="1":#使用1个月比1个月的数据
            y_train=res[:,1:2]        
        x_train=res[:,4:] 
#        print(np.shape(x_train),np.shape(y_train))#(200000, 60) (200000, 1)
        #删除无效数据
        new_x_train,new_y_train,dels=del_str_x(x_train,y_train)
#        float(new_y_train[0])
#        type(new_x_train[0])
        print(np.shape(new_x_train),np.shape(new_y_train))
        #(199997, 60) (199997, 1)
#        print(len(new_x_train[0:1,0:][0]))#60
        #准备训练的Y数据
        samples=samp_num-dels#199997
#        plt.scatter(np.arange(0,samples,1),rate3_1)
#        plt.hist(rate3_1,bins=np.arange(-0.3,0.4,0.05))    
        Ytrain=np.zeros((samples,1))
        for i in range(samples):
            if float(new_y_train[i])>max_rate:
                Ytrain[i]=1
#        plt.hist(Ytrain,bins=np.arange(-1,3,0.5))#1占25%左右        
        #开始训练
        visual_bp_fund(new_x_train,Ytrain,x_size=x_size,k1=k1,k11=k11,
                       step=step,g_name=g_name,log_dir_n=log_dir_n,lr=lr,
                       save=save)
        
        
average_continue_train(smp=20000,avg_rate=0.01,raten="3",x_size=60,
                       g_name="visual_bp_fund",k1=1,k11=3,step=200*70,
                       log_dir_n="vaaa",lr=0.001,save="y")

max_continue_train(smp=200000,max_rate=0.04,raten="3",x_size=60,
                       g_name="bp_fund_max",k1=1,k11=6,step=200*70,
                       log_dir_n="vbbb",lr=0.001,save="y")       


def average_test_predict(tb="grow_rand",raten="3",x_size=20,smp=200000,
                         avg_rate=0.03,standard=0.95,log_dir_n="fff"):
    #用剩下的尾巴数据测试准确率
    count_sql='select count(*) from %s'%tb
    ft_cursor.execute(count_sql)
    count_train=ft_cursor.fetchall()
    batchs=count_train[0][0] // smp#整除是往上取，实际上是多出一部分的。=7    
    samp_num=count_train[0][0]-smp*batchs                 

    slsql="select * from %s limit %d,%d "%(tb,smp*batchs,samp_num)
    print(slsql)        
    ft_cursor.execute(slsql)#36613
    res=np.array(ft_cursor.fetchall())
    print("test样本数量为：%s"%len(res))#36613
    #准备测试的Y数据
    rate1=[eval(rate) for rate in res[:,1]]
    rate2=[eval(rate) for rate in res[:,1]]
    rate3=[eval(rate) for rate in res[:,1]]
    if raten=="3":#使用1个月比3个月的数据
        rate3_1=rate1
#        max(rate3_1),min(rate3_1)# (0.63950136964548, -0.358762528334373)
    if raten=="2":#使用1个月比2个月的数据
        rate3_1=rate2
    if raten=="1":#使用1个月比1个月的数据
        rate3_1=rate3
    samples=len(rate3_1)##16613
#        plt.scatter(np.arange(0,samples,1),rate3_1)
#        plt.hist(rate3_1,bins=np.arange(-0.3,0.4,0.05))    
    Ytest=np.zeros((samples,1))
    for i in range(samples):
        if rate3_1[i]>avg_rate:
            Ytest[i]=1
#        plt.hist(Ytrain,bins=np.arange(-1,3,0.5))#1占25%左右        
    #准备测试的X数据
    nets=[eval(net)[0:x_size]  for net in res[:,2]]
#        nets[0]
    Xtest=np.array(nets)
    #检验算法的正确性
    try:
        nets_remain=[eval(net)[x_size:x_size+20]  for net in res[:,2]]
        sum_nets_remain=np.array(
                [np.sum(nets_remain[i]) for i in range(samples)])
        sum_nets=np.array([np.sum(nets[i]) for i in range(samples)])
        cal_false=np.sum(np.sqrt(np.square(
                sum_nets_remain/sum_nets*x_size/20-1-rate3_1)))
        print("x维度为%s、样本量为%s时的总算法失误为:%s"%(x_size,
                                          samples,cal_false))
    except:
        print("try必须配合except使用，当前x_size=60")    
    #开始测试 
    Ypre=np.zeros((samples,1))    
    with tf.Graph().as_default() as bp_fund:#这条必须得加
        with tf.Session() as sess:
            #先加载图和参数变量
            model = tf.train.import_meta_graph(
                    "a_fund_trade/tf_continue_train/"+log_dir_n+"/bp_fund-200.meta")
            model.restore(sess, tf.train.latest_checkpoint(
                    "a_fund_trade/tf_continue_train/"+log_dir_n))
            graph = tf.get_default_graph()
            # 访问placeholders变量，并且创建feed-dict来作为placeholders的新值
            weights1=graph.get_tensor_by_name("weights1:0")            
            biass1=graph.get_tensor_by_name("biass1:0")           
            weights2=graph.get_tensor_by_name("weights2:0")           
            biass2=graph.get_tensor_by_name("biass2:0")
            weights3=graph.get_tensor_by_name("weights3:0")
            biass3=graph.get_tensor_by_name("biass3:0")       
#           X_test = graph.get_tensor_by_name("Xtrain:0")#这样必须同原模型的参数
            X_test= tf.placeholder(tf.float32,[samples,x_size])
            Y_test= tf.placeholder(tf.float32,[samples,1])
            #接下来，访问你想要执行的op
            l1_out=tf.tanh(tf.matmul(X_test,weights1)+biass1)
            #tf.nn.relu         # relu是激励函数的一种
            l2_out=tf.tanh(tf.matmul(l1_out,weights2)+biass2)
            predic_op=tf.sigmoid(tf.matmul(l2_out,weights3)+biass3)
            loss = tf.reduce_mean(tf.square(Ytest-predic_op))
            
            pre_loss=sess.run(loss,feed_dict ={X_test:Xtest,Y_test:Ytest} )
            print("测试损失为：%s"%pre_loss)

            pre=sess.run(predic_op,feed_dict ={X_test:Xtest} )
            plt.hist(pre,bins=np.arange(0,1,0.05))
            for i in range(samples):
                if pre[i]>standard:
                    Ypre[i]=1
            plt.scatter(Ytest,Ypre)#有4个分布的点就说明预测不是百分之百的准确
#            plt.hist(Ypre,bins=np.arange(-1,2,0.05))
#            plt.hist(Ytest,bins=np.arange(-1,2,0.05))
            #计算预测准确率：预测为1中实际为1的占比
            Ypre_1_count=0
            YY_1_count=0            
            for i in range(samples):
                if Ypre[i]==1:
                    Ypre_1_count +=1
                    if Ytest[i]==1:
                        YY_1_count +=1
            print("预测准确率为：%s%%"%round(YY_1_count/Ypre_1_count*100,2))
            ft.close()
            
            
def max_test_predict(tb="grow_rate_randorder",raten="1",x_size=60,
                     smp=200000,max_rate=0.04,standard=0.95,
                     log_dir_n="qqq",g_name="bp_fund_max"):
    #用剩下的尾巴数据测试准确率
    count_sql='select count(*) from %s'%tb
    ft_cursor.execute(count_sql)
    count_train=ft_cursor.fetchall()
    batchs=count_train[0][0] // smp#整除是往上取，实际上是多出一部分的。=7    
    samp_num=count_train[0][0]-smp*batchs                 

    slsql="select * from %s limit %d,%d "%(tb,smp*batchs,samp_num)
    print(slsql)        
    ft_cursor.execute(slsql)
    res=np.array(ft_cursor.fetchall())
    print("test样本数量为：%s"%len(res))#123170
    #准备测试的数据
    if raten=="3":#使用1个月比3个月的数据
        y_test=res[:,3:4]
    if raten=="2":#使用1个月比2个月的数据
        y_test=res[:,2:3]
    if raten=="1":#使用1个月比1个月的数据
        y_test=res[:,1:2]        
    x_test=res[:,4:] 
    #删除无效数据
    new_x_test,new_y_test,dels=del_str_x(x_test,y_test)
    print(np.shape(new_x_test),np.shape(new_y_test))
    samples=samp_num-dels#123170
#        plt.scatter(np.arange(0,samples,1),y_test)
#        plt.hist(y_test,bins=np.arange(-0.3,0.4,0.05))    
    Ytest=np.zeros((samples,1))
    for i in range(samples):
        if float(new_y_test[i])>max_rate:
            Ytest[i]=1
#        plt.hist(Ytest,bins=np.arange(-1,3,0.5))#1占33%左右  
    #检验数据整理的正确性
#    try:
#        nets_remain=[eval(net)[x_size:x_size+20]  for net in res[:,4]]
#        sum_nets_remain=np.array(
#                [np.sum(nets_remain[i]) for i in range(samples)])
#        sum_nets=np.array([np.sum(nets[i]) for i in range(samples)])
#        cal_false=np.sum(np.sqrt(np.square(
#                sum_nets_remain/sum_nets*x_size/20-1-rate3_1)))
#        print("x维度为%s、样本量为%s时的总算法失误为:%s"%(x_size,
#                                          samples,cal_false))
#    except:
#        print("try必须配合except使用，当前x_size=60")    
    #开始测试 
    Ypre=np.zeros((samples,1))    
    with tf.Graph().as_default() as g_name:#这条必须得加
        with tf.Session() as sess:
            #先加载图和参数变量
            model = tf.train.import_meta_graph(
                    "fundlogs/"+log_dir_n+"/bp_fund-200.meta")
            model.restore(sess, tf.train.latest_checkpoint(
                    "fundlogs/"+log_dir_n))
            graph = tf.get_default_graph()
            # 访问placeholders变量，并且创建feed-dict来作为placeholders的新值
            weights1=graph.get_tensor_by_name("weights1:0")            
            biass1=graph.get_tensor_by_name("biass1:0")           
            weights2=graph.get_tensor_by_name("weights2:0")           
            biass2=graph.get_tensor_by_name("biass2:0")
            weights3=graph.get_tensor_by_name("weights3:0")
            biass3=graph.get_tensor_by_name("biass3:0")       
#           X_test = graph.get_tensor_by_name("Xtrain:0")#这样必须同原模型的参数
            X_test= tf.placeholder(tf.float32,[samples,x_size])
            Y_test= tf.placeholder(tf.float32,[samples,1])
            #接下来，访问你想要执行的op
            l1_out=tf.tanh(tf.matmul(new_x_test,weights1)+biass1)
            #tf.nn.relu         # relu是激励函数的一种
            l2_out=tf.tanh(tf.matmul(l1_out,weights2)+biass2)
            predic_op=tf.sigmoid(tf.matmul(l2_out,weights3)+biass3)
            loss = tf.reduce_mean(tf.square(Ytest-predic_op))
            
            pre_loss=sess.run(loss,feed_dict ={X_test:new_x_test,Y_test:Ytest} )
            print("测试损失为：%s"%pre_loss)

            pre=sess.run(predic_op,feed_dict ={X_test:new_x_test} )
            plt.hist(pre,bins=np.arange(0,1,0.05))
            for i in range(samples):
                if pre[i]>standard:
                    Ypre[i]=1
            plt.scatter(Ytest,Ypre)#有4个分布的点就说明预测不是百分之百的准确
#            plt.hist(Ypre,bins=np.arange(-1,2,0.05))
#            plt.hist(Ytest,bins=np.arange(-1,2,0.05))
            #计算预测准确率：预测为1中实际为1的占比
            Ypre_1_count=0
            YY_1_count=0            
            for i in range(samples):
                if Ypre[i]==1:
                    Ypre_1_count +=1
                    if Ytest[i]==1:
                        YY_1_count +=1
            print("预测准确率（而不是完整率）为：%s%%"%round(
                    YY_1_count/Ypre_1_count*100,2))

average_test_predict(tb="1mon_ave_aft_2week_divided_3day_ave",
                     raten="3",x_size=60,smp=20000,
                     avg_rate=0.01,standard=0.95,log_dir_n="vaaa")

max_test_predict(tb="grow_rate_randorder",raten="1",x_size=60,
                     smp=200000,max_rate=0.04,standard=0.99,
                     log_dir_n="qqq",g_name="bp_fund_max")
            





    