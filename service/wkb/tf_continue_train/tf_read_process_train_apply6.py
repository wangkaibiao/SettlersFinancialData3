# -*- coding: utf-8 -*-
"""
    总体思路：分4部分，目标是每一部分功能清晰、关联但独立，当修改一部分时不会影响其他部分的运行。每一部分也按照这个
思路。这样，在实际应用时，调节好每一部分的参数，总运行即可，可以调整的参数设有默认值即可，不可以调整的参数不设置默认值。
20181028——简化模型至纯数学映射这一可以理解的逻辑，无逻辑不添加；
20181030——尝试映射的本质、先实验纯线性模型，梯度直接消失有时因为样本特征数据和目标数据度量级别差距太大导致参数几乎为零；
20181101——加入单维映射；
20181102——尝试tanh；
"""

import pymysql as pdb
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from scipy.special import comb
import smtplib


#发邮件程序
def sendmail(Text):
#    在python3中该函数出现中文字符会Unicodeencodeerror
    Server = "smtp.qq.com" # QQ邮箱的SMTP服务器地址
    Subject = "znzs"  # 邮件主题，
    To = "cmbc95568@139.com" # 收件人
    From = "780901581@qq.com" # 发件人
    #Text = "This is the email send by xpleaf, from xpleaf@163.com!" 
    # 邮件内容
    Body = '\r\n'.join(("From: %s" % From,
                    "To: %s" % To,
                    "Subject: %s" % Subject,
                    "",
                    Text)) 
    s = smtplib.SMTP()  # 实例化一个SMTP类
    s.connect(Server, '25') # 连接SMTP服务器
    s.starttls()    # 开启TLS（安全传输）模式
    s.login('780901581@qq.com', 'ydbnqlalrowxbecg')# 登陆到163邮件服务器
    s.sendmail(From, [To], Body)    # 发送邮件
    s.quit()    # 退出



"""一、read，读取数据"""
def to_db(db="wangkaibiao"):
    return pdb.connect(host="localhost",
                      port=3306,
                      user="root",
                      passwd="123456",
                      db=db,
                      charset="utf8")

#连接到数据
ft=to_db("wangkaibiao")#ft=fund_train
ft_cursor=ft.cursor()

#观察要训练的数据表
ft_cursor.execute("show tables")
train_table=ft_cursor.fetchall()[2][0]
ft_cursor.execute("describe %s"%train_table)
table_shape=ft_cursor.fetchall()
print(train_table,table_shape)
  


"""二、process，加工数据成为可训练、可测试、可预测的数据"""
#数据表总的结构就固定为：基金编号，增长率，近季度基金净值
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
#    test1=np.delete(x_train,[1,2,3],axis=0)
    #axis=0表示行，axis=1表示列
#    np.shape(test1)#(123167, 60)
    contain_str_index=[]
    i=0
    for x in x_train:
        try:
            x.astype("float32")
        except:
            contain_str_index.append(i)             
        i+=1
    new_x_train=np.delete(
            x_train,contain_str_index,axis=0).astype("float32")
    new_y_train=np.delete(y_train,contain_str_index,axis=0)
    return new_x_train,new_y_train,len(contain_str_index)


#根据理论原理，只把传入的数据生成能训练的数据，同样也可以测试
"""下一步加入单维映射：sin、cos、平方"""
def train_data(select_data,batch_size,x_size=60,tanh=0):
    #观察具体的数据结构
#    select_sql="select * from %s limit %d,%d "%("1mon_ave_aft_2week_divided_3day_ave",0,50000)
#    print(select_sql)        
#    ft_cursor.execute(select_sql)#16613
#    select_data=np.array(ft_cursor.fetchall())
    #摘出要训练的Y标签数据
    rates=[eval(rate) for rate in select_data[:,1]]    
#    Ytrain=np.zeros((batch_size,1))
#    for i in range(batch_size):
#        if rates[i]>divide_rate:
#            Ytrain[i]=1
#plt.hist(Ytrain,bins=np.arange(-1,3,0.5))#1占25%左右        
    #摘出并整理要训练的X数据
    nets=[eval(net)[0:x_size]  for net in select_data[:,2]]
#        nets[0]
    Xtrain=np.array(nets)
    if tanh==0:        
        Ytrain=np.array(rates).reshape(-1,1)*10
        plt.hist(Ytrain)
        plt.show()
        return Xtrain,Ytrain
    else:
        with tf.Session() as sess:
            Ytrain=sess.run(tf.nn.tanh(np.array(rates).reshape(-1,1)*10))
            plt.hist(Ytrain)
            plt.show()
            return Xtrain,Ytrain
        
#train_data(1,1,x_size=60,tanh=0) 
            
        
def transfer_data(x,square=1,sin=1,cos=1):   
  with tf.Session() as sess:
    #x=tf.constant([0.,1.,2.,0.],shape=[2,2])
    if square==1:
      square_x=tf.square(x)
      x_transfer_concat=tf.concat([x,square_x],axis=1)
    else:
      x_transfer_concat=tf.constant(x)
    if sin==1:
      sin_x=tf.sin(x)
      x_transfer_concat=tf.concat([x_transfer_concat,sin_x],axis=1)
    if cos==1:
      cos_x=tf.cos(x)
      x_transfer_concat=tf.concat([x_transfer_concat,cos_x],axis=1)    
    print(sess.run(tf.shape(x_transfer_concat)))
    return sess.run(x_transfer_concat)
  
  
#transfer_data([[0.,1.],[2.,0.]])

"""三、train，达到训练结构和应用一体的目的，多返回内部结果"""
def transfer_tanh_bp(X,Y,k1=1,k11=3,step=1,save="y",graph_name="transfer_tanh_bp"):
    #Graph_name=graph_name #这一步根本没用，模型保存和加载不在乎图的名字
    with tf.Graph().as_default() as Graph_name:#图的名称或许不重要，重要的是图的结构和内容
        data_size=len(Y)
        x_size=np.shape(X)[1]#X=np.array([[1,2,3],[14,5,7]])
        #通过添加占位符，模型就不会受数据样本量变化的影响
        Xtrain= tf.placeholder(tf.float32,[data_size,x_size]) 
        Ytrain= tf.placeholder(tf.float32,[data_size,1])
       
        #①处理数据、映射到1维空间
        weights1=tf.Variable(tf.truncated_normal([x_size,x_size+1+k1],stddev=1.0),name="weights1")
        #---切刀至高维面
        tf.summary.histogram("h_weights1",weights1)
        biass1=tf.Variable(tf.truncated_normal([1,x_size+1+k1],stddev=1.0),name="biass1")
        tf.summary.histogram("h_biass1",biass1)
        neural_num=int(comb(x_size+1+k1,x_size+1))#产生组合数
        weights2=tf.Variable(tf.truncated_normal([x_size+1+k1,neural_num],stddev=1.0),name="weights2")
        #---组合高维面到高维体
        tf.summary.histogram("h_weights2",weights2)
        biass2=tf.Variable(tf.truncated_normal([1,neural_num],stddev=1.0),name="biass2")
        tf.summary.histogram("h_biass2",biass2)        
        weights3=tf.Variable(tf.truncated_normal([neural_num,1],stddev=1.0),name="weights3")
        #---高维体组合映射到1维空间
        tf.summary.histogram("h_weights3",weights3)
        biass3=tf.Variable(tf.truncated_normal([1,1],stddev=1.0),name="biass3")
        tf.summary.histogram("h_biass3",biass3)        
        
#        #②再从二维空间划分（原理仍是重复上面）
#        weights11=tf.Variable(tf.truncated_normal([2,2+1+k11],stddev=1.0),name="weights11")
#        tf.summary.histogram("h_weights11",weights11)
#        biass11=tf.Variable(tf.truncated_normal([1,2+1+k11],stddev=1.0),name="biass11")
#        tf.summary.histogram("h_biass11",biass11)
#        neural_num2=int(comb(2+1+k11,2+1))#产生组合数
#        weights21=tf.Variable(tf.truncated_normal([2+1+k11,neural_num2],stddev=1.0),name="weights21")
#        tf.summary.histogram("h_weights21",weights21)
#        biass21=tf.Variable(tf.truncated_normal([1,neural_num2],stddev=1.0),name="biass21")
#        tf.summary.histogram("h_biass21",biass21)        
#        weights31=tf.Variable(tf.truncated_normal([neural_num2,1],stddev=1.0),name="weights31")
#        tf.summary.histogram("h_weights31",weights31)
#        biass31=tf.Variable(tf.truncated_normal([1,1],stddev=1.0),name="biass31")
#        tf.summary.histogram("h_biass31",biass31)    

        #③开始设计具体网络结构，首尾不变、变的只是中间的结构，也不影响数据结构
        l1_out=tf.tanh(tf.matmul(Xtrain,weights1)+biass1,name="l1_out")
        #tf.nn.relu    tf.sigmoid     # relu是激励函数的一种
        l2_out=tf.tanh(tf.matmul(l1_out,weights2)+biass2,name="l2_out")
#        visual_predic_op=tf.matmul(l2_out,weights3)+biass3#tf.nn.relu(tf.matmul(l2_out,weights3)+biass3)
#        tf.summary.histogram("visual_predic_op",visual_predic_op)        
#        l11_out=tf.tanh(tf.matmul(visual_predic_op,weights11)+biass11,name="l11_out")
#        l21_out=tf.tanh(tf.matmul(l11_out,weights21)+biass21,name="l21_out")
        predic_op=tf.tanh(tf.matmul(l2_out,weights3)+biass3,name="predic_op")#---加上这条才能在预测时调用
        tf.summary.histogram("predic_op",predic_op) 
        
#        arr=np.array([1,1,1,134,45,3,46,45,65,3,23424,234,12,12,3,546,1,2]).reshape(-1,1)
#        index=np.where(arr>=3)[0]
#        arr[index]
#        A = tf.constant(arr)
#        a=tf.gather(A,index)#以index的形状为基础、往里填充数据，和tf.gather_nd不一样
#        with tf.Session() as sess:
#            print(sess.run(a))
        
#        index_0=np.where(Y==0)[0]        
#        index_1=np.where(Y==1)[0]
#        print(index_1)
#        #凡是涉及Tensorflow的tensor按照索引取值的，都要用tf.gather，而不能直接操作
#        loss_0=tf.reduce_mean(tf.square(tf.gather(Ytrain,index_0)-tf.gather(predic_op,index_0)))
#        loss_1=tf.reduce_mean(tf.square(tf.gather(Ytrain,index_1)-tf.gather(predic_op,index_1)))
#        loss=loss_0+loss_1#这样可以防止由于数量失衡造成的误差
        loss=tf.reduce_mean(tf.square(Ytrain-predic_op))
        tf.summary.scalar("s_loss",loss)
        tf.summary.histogram("h_loss",loss)

        #④开始设计训练过程
        #train=tf.train.MomentumOptimizer(lr,0.9).minimize(loss)
        train=tf.train.AdamOptimizer().minimize(loss)        
        merged = tf.summary.merge_all()#收集数据但也需要数据来计算，也是图的元素之一        
        model_dir="a_fund_trade/tf_continue_train/"+graph_name
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
            
            if step==1:#本步只执行预测及返回其他内部结果
                return sess.run(predic_op,{Xtrain:X,Ytrain:Y})
            else:#如果不预测就训练
                for i in range(step):
    #                lr_t=lr*(1-i/step)#学习率随步数减少，这种损失呈现线性递减
    #                #还一种学习率是：lr/sqrt(i)，这种损失应该呈现非线性递减
    #                train=tf.train.GradientDescentOptimizer(lr_t).minimize(loss) 
    #                # 选择梯度下降法  
                    sess.run(train,feed_dict={Xtrain:X,Ytrain:Y})  
                    if (i+1)%200 == 0:
                        now_loss=sess.run(loss,feed_dict={Xtrain:X,Ytrain:Y})
                        print( str(i)+"步：学习率 %s"%"lr_t"+" ；损失 %s"%str(now_loss) )
                        rs=sess.run(merged,feed_dict={Xtrain:X,Ytrain:Y})          
                        writer.add_summary(rs,(i+1))
                        #writer必须配合独立新Graph使用，否则会报错没有给占位符传入数据 
                        if run=="try" and save=="y":
                            saver.save(sess,model_dir+"/bp_fund",global_step=200,write_meta_graph=False)
                        #此处的路径不能用占位符来替换、但能用加号连接字符串
                        #"+log_dir_n+"，否则运行之后会报错，也可能是write_meta_graph
                        #每次都操作的原因，所以加上if判断。此外文件夹名字不能太短
                        if run=="except" and save=="y":
                            saver.save(sess,model_dir+"/bp_fund",global_step=200,write_meta_graph=True)
                        if now_loss < 0.00001:
                            return "训练损失达到要求，提前结束训练"
                        
                        
            
            #训练结束，执行一次预测过程，如果结果太大就要避免计算占用过多内存            
            print("predic:"+"sess.run(predic_op,{Xtrain:X,Ytrain:Y})"
                  ,"__loss:",sess.run(loss,feed_dict={Xtrain:X,Ytrain:Y})) 
            #sess.close()#with情况下不需要

        
        
"""四、apply，训练、测试和应用"""
#分批次实际训练学习
def continue_train(table="table_name",batch_size=30000,start_batch=0,model=transfer_tanh_bp,step=10000):
    #1、根据数据表的情况切分训练数据
    count_sql='select count(*) from %s'%table
    ft_cursor.execute(count_sql)
    data_size=ft_cursor.fetchall()
        #整除是往上取，实际上是多出一部分的
    batchs=data_size[0][0] // batch_size
    start_batch=min([start_batch,batchs])
    
    #2、开始训练每一批次batch的数据
    for i in range(start_batch,batchs+1):
        if i == batchs:
            print("终止循环，不要尾巴数据了")
            break#终止循环，不要尾巴数据了
        select_sql="select * from %s limit %d,%d "%(table,batch_size*i,batch_size)
        print(select_sql)        
        ft_cursor.execute(select_sql)#16613
        select_data=np.array(ft_cursor.fetchall())
        
        Xtrain,Ytrain=train_data(select_data,batch_size,tanh=1)
        Xtrain=transfer_data(Xtrain)
        #开始训练
        #return model(Xtrain,Ytrain)
        #return会打断for循环，可用于观察模型内部数据
        model(Xtrain,Ytrain,step=step)
    

#continue_train("1mon_ave_aft_2week_divided_3day_ave",batch_size=10000,start_batch=90,step=100000)


def test_predict(table="table_name",batch_size=60000,model=transfer_tanh_bp,divide_predict=0.9):
    #用剩下的尾巴数据测试准确率
    count_sql='select count(*) from %s'%table
    ft_cursor.execute(count_sql)
    count_train=ft_cursor.fetchall()
    batchs=count_train[0][0] // batch_size
    test_size=count_train[0][0]-batch_size*batchs                 

    select_sql="select * from %s limit %d,%d "%(
            table,batch_size*batchs,test_size)
    print(select_sql)        
    ft_cursor.execute(select_sql)#36613
    select_data=np.array(ft_cursor.fetchall())
    print("test样本数量为：%s"%len(select_data))#36613
    
    Xtest,Ytest=train_data(select_data,test_size,tanh=1)
    Xtest=transfer_data(Xtest)
    
#    return model(Xtest,Ytest)#逐步调试

    #开始测试 :计算预测准确率：预测为1中实际为1的占比
    Ypre=model(Xtest,Ytest,step=1)
#    Ypre_1_count=0.#预测为1的数量，一定要用浮点数
#    YY_1_count=0.#预测为1中实际为1的数量           
#    for i in range(test_size):
#        if Ypre[i]>divide_predict:
#            Ypre_1_count +=1.
#            if Ytest[i]==1:
#                YY_1_count +=1.
#    #★★★一定要记住：/在Python3中直接是除以，在Python2中、1/2=0、1./2.=0.5
#    print("预测准确率为：%s%%"%round(YY_1_count/Ypre_1_count*100,3))
    Ytest=Ytest.reshape(-1)#把矩阵转为行向量
    Ypre=Ypre.reshape(-1)
    print("预测和实际的相关系数为:%s"%np.corrcoef(Ytest,Ypre))
    #ft.close()
    plt.scatter(Ytest,Ypre)
    plt.show()
    return Ytest.max(),Ypre.max()

#test_predict("1mon_ave_aft_2week_divided_3day_ave",batch_size=20000)            


def can_buy(start_d="2017-10-18",end_d="2018-02-18",x_size=60,model=transfer_tanh_bp,divide_predict=0.5):
    select_sql='select fundid,sumnet from fundnets \
    where netdate>=%s and netdate<=%s \
    order by netdate'
    ft_cursor.execute(select_sql,[start_d,end_d])
    select_data=np.array(ft_cursor.fetchall())#['750005' '1.6261']
     #a[np.where((a[:,0]==0)*(a[:,1]==1))]#数组筛选符合条件的行
    #读取目标基金、并生成列表
    fundid_str=open("a_fund_trade//fundid.txt")
    fundid=eval(fundid_str.read()) #eval的列表字符串中不能有回车，即列表元素要紧挨着
    print(len(fundid)) 
    useful_nets=[]
    unuseful_nets=[]
    for fi in fundid:
        #筛选出包含fi的行，然后取第二列的累计净值
        finet_a=select_data[np.where(select_data[:,0]==fi)][:,1]
        if len(finet_a) >= x_size:
            finet_60=np.append(finet_a[-x_size:-1],finet_a[-1])
            #finet_60.shape (60, 1)
            finet_60T=np.reshape(finet_60,(-1, x_size))
            #plt.scatter(np.arange(0,60,1),finet_60T)
            #-1表示根据已知的形状推断剩下的形状
            #finet_60T.shape #(1, 60)
            try:
                finet_60T.astype("float32")#保证数据的可用性，只是试探
                useful_nets.append(np.append(finet_60T,fi))#★没有追加改变类型的数据，还是字符型的数字
            except:
                unuseful_nets.append(np.append(finet_60T,fi))
    useful_nets=np.array(useful_nets)
    #useful_nets.shape#(1269, 61)
    all_predict=model(transfer_data(useful_nets[:,0:60].astype("float32")),
                      np.zeros([useful_nets.shape[0],1]),
                      step=1)
    print("最大的预测值为：%s"%max(all_predict))
    
    #开始挑选合适的基金
    canbuy=[]
    for i in range(useful_nets.shape[0]):
        if all_predict[i] > divide_predict:
            canbuy.append(useful_nets[i,-1])    
    print(canbuy)
    print(len(canbuy)-1)
    s=",\n".join(canbuy)#别出现中文字符，结果有换行效果
    sendmail(s)
    plt.hist(all_predict)
    return canbuy            

can_buy(start_d="2018-07-03",end_d="2018-11-03",x_size=60,divide_predict=0.95)



    