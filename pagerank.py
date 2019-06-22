#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 上午9:34
# @Author  : ChenJie
# @File    : pagerank.py
# @Software: PyCharm
import numpy as np
from tqdm import tqdm
def load_data(path):
    f=open(path,'r')
    data=[]
    for line in f:
        x,y =line.split()
        data.append([int(x),int(y)])
    data=np.array(data)
    # print(data.shape)
    f.close()
    return data

def get_edges(data,sign):
    # print(int(np.shape(data)))
    # print(data.shape)
    #以稀疏形式保存，只存储非零的链接
    edges=np.zeros(data.shape)
    for i in range(len(data)):
        edges[i]=[sign[data[i][0]],sign[data[i][1]]]
    return edges

def block_stripe_page_rank(path,num_blocks,index,sign,r,out,beta):
    """
    :param num_blocks: total/bloclsize
    :param index: 标号
    :param sign: 索引
    :param r: pagerank_matrix
    :param out: 出度
    :param beta: 0.85
    :return:
    """
    print("\n [*]read blocks...")

    r_old=r
    while True:
        r_new= np.zeros(len(index))
        for i in tqdm(range(num_blocks)):
            # 读取数据执行pagerank算法，每次读取一个分块的数据，以达到节省内存的效果
            block = path+str(i)+'.txt'
            data = load_data(block)
            edges=get_edges(data,sign)
            for edge in edges:
                r_new[int(edge[1])]+=r_old[int(edge[0])]*beta/out[int(edge[0])]
        r_sum=sum(r_new)
        r_sub=np.ones(len(index))*(1-r_sum)/len(index)
        r_cur=r_new + r_sub
        s=np.sqrt(sum((r_cur-r_old)**2))
        # 当小于1e-8时，判断pagerank收敛，跳出循环

        if s<=1e-8:
            r_old=r_cur
            break

        else:
            r_old=r_cur
    print("\n [*]finished...")

    return r_old

def get_top(num,r,sign):
    """
    :param num: 100
    :param r: matrix
    :return:
    """
    # 获取top100的节点及其pagerank值
    r_index=r.argsort()[::-1][:num]
    ## 返回排序后的索引，从大到小100

    top_index=np.zeros(num)
    for i in range(num):
        top_index[i]=sign.index(r_index[i])
    ## 字符串转列表
    top_index = [int(i) for i in top_index]

    r.sort()
    top_r=r[::-1][:num]

    for i in range(num):
        print(top_index[i],top_r[i])
    return top_index,top_r

def write_out(top_index,top_r):
    print('[*]prepare to write result ...')
    f=open('./result/result.txt','w')

    for i in range(len(top_index)):
        f.write(str(top_index[i])+' '+str(top_r[i])+'\n')

    f.close()
    print('[+]finish to write result...')
    return

