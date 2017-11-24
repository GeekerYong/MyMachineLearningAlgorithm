# -*- coding: utf-8 -*-
"""
Support Vector Machines
author:Liu Jy
data:2017年11月20日 10:23:27
"""
import random
import numpy as np
def loadDataSet(path):
    '''
    读取数据
    '''
    dataMat = [];
    labelMat = [];
    fr = open(path)
    for line in fr.readlines():
        lineArr = line.strip().split("\t")
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    fr.close()
    return dataMat, labelMat

def selectJrand(i, num_of_alp):
    '''
    随机挑选样本
    '''
    j = i
    while(j==i):
        j = int(random.uniform(0,num_of_alp))
    return j

def clipAlpha(aj, H, L):
    '''
    门限函数，控制alpha不过分修改
    '''
    if aj>H:
        aj = H
    if aj<L:
        aj = L
    return aj

def smoSimple(dataMatIn ,classLabel ,C ,toler ,maxIter):
    '''
    简化版SMO算法
    '''
    dataMat = np.mat(dataMatIn) # m*n的矩阵
    labelMat = np.mat(classLabel).transpose() # m*1的列向量
    iter = 0
    b = 0
    m,n = np.shape(dataMat)
    alphas = np.mat(np.zeros((m,1))) # m*1的列向量
    while(iter < maxIter):
        alphaPairsChanged = 0 # 标记位，代表本轮中是否进行了优化
        for i in range(m):
            fXi = np.float(np.multiply(alphas, labelMat).T*(dataMat*dataMat[i,:].T)) + b
            Ei = fXi - np.float(labelMat[i]) # 预测值与标签的误差
            if( ((alphas[i]<C) and (labelMat[i]*Ei <-toler))  or ((labelMat[i]*Ei >toler) and (alphas[i]>0)) ):
                j = selectJrand(i, m)
                fXj = float(np.multiply(alphas, labelMat).T*(dataMat*dataMat[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if(labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j]-alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H:
                    print("L==H")
                    continue
                eta = 2.0*dataMat[i,:]*dataMat[j,:].T - \
                        dataMat[i,:]*dataMat[i,:].T - \
                        dataMat[j,:]*dataMat[j,:].T #alpha[j]的最优修改量
                if eta>=0:
                    print("eta>=0")
                    continue
                alphas[j] -= labelMat[j]*(Ei-Ej)/eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if(abs(alphas[j] - alphaJold) < 0.00001):
                    print("j not move enough")
                    continue
                alphas[i] += labelMat[i]*labelMat[j]*(alphaJold- alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i]-alphaIold)*\
                            dataMat[i,:]*dataMat[i,:].T - \
                            labelMat[j]*(alphas[j]-alphaJold)*\
                            dataMat[i,:]*dataMat[j,:].T
                b2 = b - Ej - labelMat[i]*(alphas[i]-alphaIold)*\
                            dataMat[i,:]*dataMat[j,:].T - \
                            labelMat[j]*(alphas[j]-alphaJold)*\
                            dataMat[j,:]*dataMat[j,:].T
                if((0<alphas[i]) and (C>alphas[i])):
                    b = b1
                elif((0<alphas[j]) and (C>alphas[j])):
                    b = b2
                else:
                    b = (b1+b2)/2.0
                alphaPairsChanged +=1
                print("iter: %d , i:%d  pairs changed %d" %(iter, i, alphaPairsChanged))
        if(alphaPairsChanged ==0):
            iter +=1
        else:
            iter = 0
        print("iteration number %d" % iter)
    return b,alphas
                
if __name__ == '__main__':
    dataMat, labelMat = loadDataSet("./data/testSet.txt")
    b ,alphas = smoSimple(dataMat,labelMat,0.6,0.001,40)
    
    
