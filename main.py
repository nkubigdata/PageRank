#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/22 上午10:09
# @Author  : ChenJie
# @File    : main.py
# @Software: PyCharm

import numpy as np
import time
import preLoad
import pagerank

from tqdm import tqdm

src = 'WikiData.txt'
outPath = './output/block'
block_size=2000

start = time.clock()

print('[*]Pagerank with block stripe matrix...')
# 数据分块，返回块数
num_blocks = preLoad.block_data(outPath, block_size)

# 返回标号 和max_node
index, max_node = preLoad.ID_list(outPath, num_blocks)
#
sign, r = preLoad.preprocess(index, max_node)

out = preLoad.out_degree(outPath, num_blocks, index, sign)

print('[+]Pagerank with block stripe matrix finished!')

# print(out)
#index,path,num_blocks,sign,r,out,beta

r_final = pagerank.block_stripe_page_rank(outPath, num_blocks, index, sign, r, out, 0.85)

print('\n-----------------------')

top_index, top_r = pagerank.get_top(100, r_final,sign)

pagerank.write_out(top_index, top_r)
end = time.clock()

print('time cost: ', str(end - start), 's')
