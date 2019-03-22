# -*- coding: UTF-8 -*- 
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
#import os
#import tensorflow as tf
#os.environ["CUDA_VISIBLE_DEVICES"] = "6"
#gpu_options = tf.GPUOptions(allow_growth=True)
#sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
from keras.utils import plot_model
#from matplotlib import pyplot as plt
from keras import backend as B


def resnet50(img_path = "/home/bdai/.keras/dog.jpeg"):
    # 【0】ResNet50模型，加载预训练权重
    weight_path="/home/bdai/.keras/resnet50_weights_tf_dim_ordering_tf_kernels.h5"
    model = ResNet50(weights=weight_path, include_top=True)#model = ResNet50(weights='imagenet') 
    #print(model.summary())                              # 打印模型概况
    #plot_model(model,to_file = 'a simple convnet.png')  # 画出模型结构图，并保存成图片
    
    # 【1】从网上下载一张图片，保存在当前路径下
    #'./elephant.jpg'          
    img = image.load_img(img_path, target_size=(224, 224))
    
    # 【2】显示图片
    #plt.imshow(img)
    #plt.show()
    
    #【3】将图片转化为4d tensor形式
    x = image.img_to_array(img)
    #print(x.shape) #(224, 224, 3)
    x = np.expand_dims(x, axis=0)
    #print(x.shape) #(1, 224, 224, 3)
    
    # 【4】数据预处理
#    """
#    def preprocess_input(x, data_format=None, mode='caffe'):
#       Preprocesses a tensor or Numpy array encoding a batch of images.
#    
#        # Arguments
#            x: Input Numpy or symbolic tensor, 3D or 4D.
#            data_format: Data format of the image tensor/array.
#            mode: One of "caffe", "tf".
#                - caffe: will convert the images from RGB to BGR,
#                    then will zero-center each color channel with
#                    respect to the ImageNet dataset,
#                    without scaling.
#                - tf: will scale pixels between -1 and 1,
#                    sample-wise.
#    
#        # Returns
#            Preprocessed tensor or Numpy array.
#    
#        # Raises
#            ValueError: In case of unknown `data_format` argument.
#    """
    x = preprocess_input(x) #去均值中心化，preprocess_input函数详细功能见注释
    
    # 【5】测试数据
    preds = model.predict(x)
    #print(preds.shape)  # (1,1000)
    
    B.clear_session()
    #如果在Keras内部多次使用同一个Model，例如在不同的数据集上训练同一个模型进而得到结果，会存在内存泄露的问题。
    #在运行几次循环之后，就会报错OOM。解决方法是在每个代码后面接clear_session()函数，显示的关闭TFGraph，再重启。
    
    # 【6】将测试结果解码为如下形式：
    # [(class1, description1, prob1),(class2, description2, prob2)...]
    #print('Predicted:', decode_predictions(preds, top=1)[0][0][1])
    #'Predicted:', [(u'n02504458', u'African_elephant', 0.8791098), 
    #(u'n02504013', u'Indian_elephant', 0.066597864), 
    #(u'n01871265', u'tusker', 0.054188617)]
    #Exception: URL fetch failure on https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json: 
    #        None -- [Errno -2] Name or service not known """
    prodict=decode_predictions(preds, top=1)[0][0]
    return "王婭馨，這有%s成很像%s"%(int(prodict[2]*10),prodict[1])
    
    #resnet50()