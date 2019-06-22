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

from tqdm import  tqdm

def block_data(path ,splitLen):
    # splitLen=2000
    # outputpath='./output/block'
    ## 分块写入，每块长度splitLen
    input=open(src,'r')
    count=0
    block_num=0
    dest_file=None

    for line in input:
        if count % splitLen == 0:
            if dest_file:
                dest_file.close()
            dest_file=open(path+str(block_num)+'.txt','w')
            block_num+=1

        dest_file.write(line)
        count+=1
    return block_num

def ID_list(path,num_block):
    ## 返回list,最大编号
    index=[]
    max_node=0
    for i in tqdm(range(num_block)):
        block=path+str(i)+'.txt'
        f=open(block,'r')
        for line in f:
            x,y=line.split()
            if max_node<int(x):
                max_node=int(x)
            if max_node<int(y):
                max_node=int(y)
            index.append(int(x))
            index.append(int(y))
        f.close()
    index=list(np.unique(index))
    return index,max_node

def preprocess(index,max_node):
    #ID索引编码,初始化矩阵
    #index[x]=索引号
    sign=np.zeros(max_node+1)
    sign=list(sign)
    for i in range(len(index)):
        sign[index[i]]=i;
    initial_matrix=np.ones(len(index))/len(index)
    return sign ,initial_matrix

def out_degree(path,num_blocks,index,sign):
    #出链
    out = np.zeros(len(index))
    for i in range(num_blocks):
        block=path+str(i)+'.txt'
        data=np.loadtxt(block)
        for j in range(len(data)):
            #print(data[j][0]) x->y ，x=data[j][0]
            out[int(sign[int(data[j][0])])]+=1
    return out


if __name__ == '__main__':
    block_size=2000
    # 数据分块，返回块数
    num_blocks = block_data(outPath, block_size)
    # 返回标号 和max_node
    index, max_node = ID_list(outPath, num_blocks)
    #
    sign, r = preprocess(index, max_node)
    # print(index)
    # print(sign)
    # print(r)
    out=out_degree(outPath,num_blocks,index,sign)
    print(out)
