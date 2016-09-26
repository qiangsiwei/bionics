# -*- coding: utf-8 -*-

import re
import math
import random
import fileinput
import numpy as np
import matplotlib.pyplot as plt

# 数据导入
data = np.array([map(lambda x:float(x), \
					re.split(r'\s+',line.strip().decode('utf-8'))) \
						for line in fileinput.input('data.txt')])

# 距离计算
x, y = np.hstack(data[:,0::2].T), np.hstack(data[:,1::2].T)
s = np.array([[70,40]]+[[a,b] for a,b in zip(x,y)]+[[70,40]])*np.pi/180
d = np.zeros((len(s),len(s)))
for i in xrange(len(s)):
	for j in xrange(len(s)):
		d[i,j] = d[j,i] = 6370*np.arccos(np.cos(s[i,0]-s[j,0])*np.cos(s[i,1])*np.cos(s[j,1])+np.sin(s[i,1])*np.sin(s[j,1]))

# 初始解
path_min, length_min = None, float("inf")
for _ in xrange(1000):
	path = np.hstack([[0],np.random.permutation(len(s)-2)+1,[len(s)-1]])
	length = sum([d[path[i]][path[i+1]] for i in xrange(len(path)-1)])
	if length < length_min:
		path_min, length_min = path, length

def compute_len(array):
	return sum([d[array[i]][array[i+1]] for i in xrange(len(array)-1)])

# 退火过程
e = 0.1**30; L = 20000; at = 0.999; T = 1
for k in xrange(L):
	c = sorted([int(random.random()*(len(s)-2)+1) for _ in range(2)])
	df = d[path_min[c[0]-1]][path_min[c[1]]]+d[path_min[c[0]]][path_min[c[1]+1]] - (d[path_min[c[0]-1]][path_min[c[0]]]+d[path_min[c[1]]][path_min[c[1]+1]])
	if df<0 or math.exp(-df/T)>random.random():
		path_min[c[0]:c[1]+1] = path_min[c[0]:c[1]+1][::-1]
	T *= at
	if T < e:
		break

# 绘图
a, b = s[path_min][:,0], s[path_min][:,1]
plt.plot(a, b, '-', linewidth=2)
plt.plot(s[:,0], s[:,1], '*')
plt.show()
