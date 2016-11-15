# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 19:06:45 2016

@author: JinYong Liu
"""

from numpy import *

#数组与矩阵
#看起来相似，但计算过程中可能会得到不同的结果。
#generate random array
A = random.rand(4,4)
print '数组:',A
#transform into matrix
B = mat(A)
print '矩阵：',B
#output the inverse of matrix
invB = B.I
print '矩阵逆:',invB
#mul between matrix
AmulB = invB*B
print "B*B/'",AmulB
#creat I martix
print '4x4 I矩阵',eye(4)

