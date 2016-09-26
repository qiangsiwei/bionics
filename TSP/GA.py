# -*- coding: utf-8 -*-

import re
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

# 改良圈
w, g = 50, 100
J = np.zeros((w,len(s)))
for k in xrange(w):
	c = np.hstack([[0],np.random.permutation(len(s)-2)+1,[len(s)-1]])
	for _ in xrange(len(s)):
		flag = 0
		for m in xrange(1,len(s)-2):
			for n in xrange(m+2,len(s)-1):
				if d[c[m],c[n]]+d[c[m+1],c[n+1]] < d[c[m],c[m+1]]+d[c[n],c[n+1]]:
					c[m+1:n+1] = c[m+1:n+1][::-1]; flag = 1
		if flag == 0:
			J[k,c] = np.array(range(len(s))); break

# 遗传变异
J = J/(len(s)-1)
for k in xrange(g):
	# 交叉
	A = J.copy(); c = np.random.permutation(range(w))
	for i in range(w)[::2]:
		F = int(random.random()*(len(s)-1)+1)
		A[c[i],F:], A[c[i+1],F:] = A[c[i+1],F:], A[c[i],F:]
	# 变异
	by = np.where(np.random.uniform(0,1,w)<0.1)[0]
	B = A[by].copy()
	for i in range(len(by)):
		bw = sorted([int(random.random()*(len(s)-1)+1) for _ in range(3)])
		B[i] = np.hstack([B[i][:bw[0]],B[i][bw[1]:bw[2]],B[i][bw[0]:bw[1]],B[i][bw[2]:]])
	# 筛选
	G = np.vstack([J, A, B])
	S = sorted([(sum([d[loop[i]][loop[i+1]] for i in xrange(len(loop)-1)]),index) \
				for index,loop in enumerate(np.argsort(G))], key=lambda x:x[0])[:w]
	J = G[np.array(map(lambda x:x[1], S))].copy()

# 绘图
a, b = s[np.argsort(J[0])][:,0], s[np.argsort(J[0])][:,1]
plt.plot(a, b, '-', linewidth=2)
plt.plot(s[:,0], s[:,1], '*')
plt.show()
