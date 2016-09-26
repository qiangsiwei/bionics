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
s = np.array([[70,40]]+[[a,b] for a,b in zip(x,y)])*np.pi/180
d = np.zeros((len(s),len(s)))
for i in xrange(len(s)):
	for j in xrange(len(s)):
		d[i,j] = d[j,i] = 6370*np.arccos(np.cos(s[i,0]-s[j,0])*np.cos(s[i,1])*np.cos(s[j,1])+np.sin(s[i,1])*np.sin(s[j,1]))

numant = numcity = len(s); numiter = 50
alpha = 1; beta = 1; rho = 0.5; Q = 1
heutable = 1.0/(d+np.diag([1e10]*numcity))
phetable = np.ones((numcity,numcity))
len_min = float('inf'); path_min = None

# 蚁群模拟
for _iter in xrange(numiter):
	# 初始化
	pathtable = np.zeros((numant,numcity))
	pathtable[:,0] = np.random.permutation(numcity); length = np.zeros(numant)
	# 轮盘赌
	for i in range(numant):
		visiting = pathtable[i,0]
		unvisited = range(numcity); unvisited.remove(visiting)
		for j in range(1,numcity):
			probtrans = np.array([phetable[visiting][unvisited[k]]**alpha * heutable[visiting][unvisited[k]]**beta for k in range(len(unvisited))])
			probtranscumsum = (probtrans/probtrans.sum()).cumsum() - np.random.rand()
			k = unvisited[np.where(probtranscumsum>0)[0][0]]
			pathtable[i,j] = k; unvisited.remove(k)
			length[i] += d[visiting][k]
			visiting = k
		length[i] += d[visiting][pathtable[i,0]]
	# 更新
	if length.min() < len_min:
		len_min = length.min(); path_min = pathtable[length.argmin()].copy().astype(int)
	# 信息素释放
	phetabledelta = np.zeros((numcity,numcity))
	for i in range(numant):
		for j in range(numcity-1):
			phetabledelta[pathtable[i,j]][pathtable[i,j+1]] += Q/d[pathtable[i,j]][pathtable[i,j+1]]
		phetabledelta[pathtable[i,-1]][pathtable[i,0]] += Q/d[pathtable[i,-1]][pathtable[i,0]]
	phetable = (1-rho)*phetable + phetabledelta

# 绘图
path_min = np.hstack([path_min,[path_min[0]]])
a, b = s[path_min][:,0], s[path_min][:,1]
plt.plot(a, b, '-', linewidth=2)
plt.plot(s[:,0], s[:,1], '*')
plt.show()
