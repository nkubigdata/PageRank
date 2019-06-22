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
    edges=np.zeros(data.shape)
    for i in range(len(data)):
        edges[i]=[sign[data[i][0]],sign[data[i][1]]]
    return edges

def block_stripe_page_rank(path,num_blocks,index,sign,r,out,beta):
    r_old=r
    while True:
        r_new= np.zeros(len(index))

        for i in tqdm(range(num_blocks)):
            block = path+str(i)+'.txt'
            data = load_data(block)
            edges=get_edges(data,sign)
            for edge in edges:
                r_new[int(edge[1])]+=r_old[int(edge[0])]*beta/out[int(edge[0])]
        r_sum=sum(r_new)
        r_sub=np.ones(len(index))*(1-r_sum)/len(index)
        r_cur=r_new + r_sub
        s=np.sqrt(sum((r_cur-r_old)**2))

        if s<=1e-8:
            r_old=r_cur
            break
        else:
            r_old=r_cur
    return r_old

def get_top(num,r,sign):
    r_index=r.argsort()[::-1][:100]
    r.sort()
    top_r=r[::-1][:num]
    top_index=np.zeros(num)
    for i in range(num):
        top_index[i]=sign.index(r_index[i])
    top_index = [int(i) for i in top_index]
    for i in range(num):
        print(top_index[i],top_r[i])
    return top_index,top_r

def write_out(top_index,top_r):
    f=open('./result/result.txt','w')
    for i in range(len(top_index)):
        f.write(str(top_index[i])+' '+str(top_r[i])+'\n')
    f.close()
    return

