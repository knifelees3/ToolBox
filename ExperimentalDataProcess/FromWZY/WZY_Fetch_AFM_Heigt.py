# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 12:01:18 2019

@author: admin
"""

import numpy as np
import os as os
import matplotlib.pylab as plt

Path = os.getcwd() + '\\'


#Filename = '0.4%_PMMA_QD_WATER_6000_01_heightMeasured_trace_300_30x700_30_17.cross'
Filename = '/Data_JPK/FLIM_13_000.jpk'
Pathname = Path + Filename

n = 0
Infor = []
x, y = [], []
with open(Pathname, 'r') as f:
    for line in f:
        n = n + 1
        if n < 5:
            Infor.append(map(str, line.split()))
        else:
            x.append(map(float, line.split())[0])
            y.append(map(float, line.split())[1])
x = np.array(x)
y = np.array(y)
x1 = x * 1e9
y1 = y * 1e9

y1 = y1 - np.min(y1)


# x1=x1[31:374]
# x1=x1-np.min(x1)
# y1=y1[31:374]-0.5
# x1=x1[341:682]
# x1=x1-np.min(x1)
# y1=y1[341:682]-4.5
F1 = plt.figure(figsize=(8, 5))
F1ax1 = F1.add_subplot(111)
F1ax1.plot(x1, y1, 'k')
# F1ax1.set_ylim(-0.5,12)
F1ax1.set_xlabel(r'x(um)')
F1ax1.set_ylabel('Height(nm)')
F1ax1.legend(loc='best')
F1.show()
