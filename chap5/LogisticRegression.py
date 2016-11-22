# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 12:13:42 2016

@author: JinYong Liu
Logistic回归
优点：计算代价低，容易实现
缺点：容易欠拟合，分类精度不够高
"""
import numpy as np
import os


os.chdir(u"F:\\Python\\机器学习实战\\chap5")


def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('data/testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def rndGradAscent(dataMat, labelMat, numIter = 150):
    row, col = np.shape(dataMat)
    weights = np.ones(col)
    for j in range(numIter):  # 确定有限的迭代次数
        dataIndex = range(row)
        for i in range(row):
            alpha = 4/(1.0 + j + i) + 0.0001  # 保证alpha越来越小但不至于0
            randIndex = int(np.random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMat[randIndex] * weights))
            error = labelMat[randIndex] - h
            weights = weights + alpha * error * dataMat[randIndex]
            del(dataIndex[randIndex])
    return weights


def gradAscent(dataMatIn, labelMatIn):  # 梯度上升优化算法
    dataMat = np.mat(dataMatIn)
    labelMat = np.mat(labelMatIn).transpose()
    row, col = np.shape(dataMat)
    alpha = 0.001
    maxCycles = 500
    weights = np.ones((col, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMat * weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMat.transpose() * error
    return weights


def plotBestFit(wei):
    import matplotlib.pyplot as plt
    weights  = wei
    dataMat, labelMat=loadDataSet()
    dataArr = np.array(dataMat)
    n = np.shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i])== 1:
            xcord1.append(dataArr[i, 1])
            ycord1.append(dataArr[i, 2])
        else:
            xcord2.append(dataArr[i, 1])
            ycord2.append(dataArr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]  # 令sigmoid为0，解出关系式
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()


def classifyVector(X, weights):
    prob = sigmoid(sum(X * weights))
    if prob > 0.5:
        return 1.0
    else:
        return 0.0


def colicTest():
    frTrain = open('data/horseColicTraining.txt')
    frTest = open('data/horseColicTest.txt')
    trainSet = []
    testSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        cuurLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(cuurLine[i]))
        trainSet.append(lineArr)
        trainingLabels.append(float(cuurLine[21]))
    trainWeights = rndGradAscent(np.array(trainSet), trainingLabels, 500)
    errorCount = 0
    numTestVec = 0
    for line in frTest.readlines():
        numTestVec += 1
        cuurLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(cuurLine[i]))
        testVec = np.array(lineArr)
        if int(classifyVector(testVec, trainWeights)) != int(cuurLine[21]):
            errorCount += 1
    errorRate = float(errorCount)/numTestVec
    print "错误率为: %f" %errorRate
    return errorRate


def Test():
    numTest = 10;
    errorSum = 0.0
    for k in range(numTest):
        errorSum += colicTest()
    print "在 %d 次迭代后，平均错误率为 %f" %(numTest, errorSum/float(numTest))


def main():
    Test()

if __name__ == '__main__':
    main()
