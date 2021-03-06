# -*- coding: utf-8 -*-
'''
Created on 2017年12月12日
@author: Administrator
'''
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
minst=input_data.read_data_sets('Minst_data',one_hot=True)
bacth_size=100
n_bacth=minst.train.num_examples//bacth_size
# 550
#         直方图

def weight_variable(shape):
    initial=tf.truncated_normal(shape,stddev=0.1)
#     生成一个截断的正态分布
    return tf.Variable(initial)
# 初始化权值
def bias_variable(shape):
    initial=tf.constant(0.1,shape=shape)
    return tf.Variable(initial)
# 初始化偏置
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
# 卷积层
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')


x=tf.placeholder(tf.float32,[None,784],name='x_input')
# 28x28
y=tf.placeholder(tf.float32,[None,10],name='y_input')
x_image=tf.reshape(x,[-1,28,28,1])# 改变x的格式，转化为4d的向量



W_conv1=weight_variable([5,5,1,32])#5x5的采样窗口，32个卷积核从一个平面抽取
b_conv1=bias_variable([32])#每一个卷积核一个偏置值

h_conv1=tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)
h_pool1=max_pool_2x2(h_conv1)#进行max_pooling

# 第二个卷积层
W_conv2=weight_variable([5,5,32,64])#5*5的采样窗口，64个卷积核从32个平面抽取特征
b_conv2=bias_variable([64])

h_conv2=tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
h_pool2=max_pool_2x2(h_conv2)#进行max_pooling

h_pool2_flat=tf.reshape(h_pool2,[-1,7*7*64])#把池化层2的输出偏平化为一维
# 28*28的图片第一次卷积后还是28*28，第一次池化后变为14*14
# 第二次卷积后为14*14，第二次池化后变为了7*7
# 进行上面操作后得到64张7*7的平面

# 初始化第一个全连接层的权值

W_fc1=weight_variable([7*7*64,1024])#上一层有7*7*64个神经元，全连接层有1024个神经元
b_fc1=bias_variable([1024])
h_fc1=tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1)+b_fc1)#第一个全连接层的输出
keep_prob=tf.placeholder(tf.float32)
h_fc1_drop=tf.nn.dropout(h_fc1,keep_prob)

W_fc2=weight_variable([1024,10])#上一层有7*7*64个神经元，全连接层有1024个神经元
b_fc2=bias_variable([10])
prediction=tf.nn.softmax(tf.matmul(h_fc1_drop,W_fc2)+b_fc2)

cross_entropy=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))
train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction=tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

acc_test_list,acc_train_list=[],[]
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(1001):
        bacth_xs,bacth_ys=minst.train.next_batch(bacth_size)
        sess.run(train_step,feed_dict={x:bacth_xs,y:bacth_ys,keep_prob:0.9})
        
        acc_train=sess.run(accuracy,feed_dict={x:bacth_xs,y:bacth_ys,keep_prob:1.0})
        acc_train_list.append(acc_train)
        acc_test=sess.run(accuracy,feed_dict={x:minst.test.images,y:minst.test.labels,keep_prob:1.0})
        acc_test_list.append(acc_test)
plt.figure()
plt.plot(acc_test_list,'r',lw=2)
plt.plot(acc_train_list,'g',lw=1)
plt.show()
print(acc_test_list[-1],acc_train_list[-1])
print('done')
# print(acc_train)
# print('\n')
# print(acc_test)











