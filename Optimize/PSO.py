# -*- coding: utf-8 -*-

import random
import numpy as np
  
birds = 10; xnum = 5
w = 0.8; c1 = 2; c2 = 2; r1 = 0.6; r2 = 0.3
birdsbestpos = None

def GenRandVec():
    return [random.randrange(1,100) for _ in xrange(xnum)]

pos, speed = np.array([GenRandVec() for i in range(birds)]), np.array([GenRandVec() for i in range(birds)])
bestpos = pos.copy()

def CalDis(array): 
    return sum([i**2 for i in array])

def FindBirdsBestPos():
    return sorted([(bestpos[i], CalDis(bestpos[i])) for i in xrange(birds)], key=lambda x:x[1])[0][0]
  
def UpdateSpeed():
    global speed, birdsbestpos
    birdsbestpos = FindBirdsBestPos()
    speed = w*speed+c1*r1*(bestpos-pos)+c2*r2*(birdsbestpos-pos)
          
def UpdatePos():
    global pos, bestpos
    pos = pos+speed
    for i in range(birds):
        if CalDis(pos[i]) < CalDis(bestpos[i]):
            bestpos[i] = pos[i].copy()

for i in range(100):
    UpdateSpeed(); UpdatePos()
    print CalDis(birdsbestpos), birdsbestpos
