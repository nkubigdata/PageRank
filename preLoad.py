#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/28 下午4:08
# @Author  : ChenJie
# @File    : preLoad.py
# @Software: PyCharm

import numpy as np
import time
src = 'WikiData.txt'
outPath = './output/block'

# def load_data(path):
#     f=open(path,'r')
#     data=[]
#     for line in f:
#         x,y =line.split()
#         data.append([int(x),int(y)])
#     data=np.array
#     f.close()
#     return data

def ID_list(path,num_block):
    index=[]
    max_node=0
    for i in range(num_block):
        block=path+str(i)+'.txt'
        f=open(block,'r')
        for line in f:
            x,y=line.split()
            if max_node<int(x):
                max_nodex=int(x)
            if max_node<int(y):
                max_node=int(y)
            index.append(int(x))
            index.append(int(y))
        f.close()
    index=list(np.unique(index))
    return index,max_node

def out_degree(path,num_blocks,index,sign):
    out = np.zeros(len(index))
    for i in range(num_blocks):
        block=path+str(i)+'.txt'
        data=np.loadtxt(block)
        for j in range(len(data)):
            out[int(sign[int(data[j][0])])]+=1
    return out

def block_data(path ,splitLen):
    # splitLen=2000
    # outputpath='./output/block'
    input=open(src,'r')
    count=0
    block_num=0
    dest=None

    for line in input:
        if count % splitLen == 0:
            if dest:
                dest.close()
            dest=open(path+str(block_num)+'.txt','w')
            block_num+=1
        dest.write(line)
        count+=1
    return block_num
def preprocess(index,max_node):
    #ID 编码
    sign=np.zeros(max_node+1)
    sign=list(sign)
    for i in range(len(index)):
        sign[index[i]]=i;
    r=np.ones(len(index))/len(index)
    return sign ,r

if __name__ == '__main__':
    block_size=2000

    num_blocks = block_data(outPath, block_size)

    index, max_node = ID_list(outPath, num_blocks)

    sign, r = preprocess(index, max_node)

    out=out_degree(outPath,num_blocks,index,sign)

    print(index)
    print(max_node)