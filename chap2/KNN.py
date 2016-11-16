# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 19:33:49 2016 %%

@author: JinYong Liu
@codestyle:PEP8

KNN Algorithm
优点: 精度高，异常值不敏感，无输入数据假定
缺点：计算复杂度高，空间复杂度高
数据范围：数值型，标称型
"""
import os
import numpy as np
import operator
import matplotlib.pyplot as plt


def classify0(X, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]  # shape read col len
    diffMat = np.tile(X, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistance = sqDiffMat.sum(axis=1)
    Distance = sqDistance**0.5   # compute distance between X and sample
    sortedDistIndicies = Distance.argsort()
    print sortedDistIndicies
    classCount = {}
    for i in range(k):
        voteILabel = labels[sortedDistIndicies[i]]
        classCount[voteILabel] = classCount.get(voteILabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def img2vector(filename):
    fr = open(filename)
    returnVec = np.zeros((1, 1024))
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):  # 每幅图一共是32x32，转化为1024的向量
            returnVec[0, 32*i+j] = int(lineStr[j])
    return returnVec


def file2Matrix(filename):
    fr = open(filename)
    arrayLines = fr.readlines()
    numberOfLines = len(arrayLines)
    returnMat = np.zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]  # the number of row
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    normDataSet = normDataSet/np.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def plotMain():  # 数据绘图练习
    fig = plt.figure()
    ax = fig.add_subplot(111)
    datingDataMat, datingLabels = file2Matrix('data/datingTestSet2.txt')
    ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2],
               15.0*np.array(datingLabels), 15.0*np.array(datingLabels))
    ax.axis([-2, 25, -0.2, 2.0])
    plt.xlabel('Percentage of Time Spent Playing Video Games')
    plt.ylabel('Liters of Ice Cream Consumed Per Week')
    plt.show()


def datingClassTest():  # 约会数据集测试
    holdRatio = 0.10  # 数据集划分为两部分，前10%用于测试，后90%用于计算距离。
    datingDataMat, dataingLabels = file2Matrix('data/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*holdRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :],
                                     dataingLabels[numTestVecs:m], 3)
        print "分类器结果为: %d , 实际结果为: %d" % (classifierResult, dataingLabels[i])
        if (classifierResult != dataingLabels[i]):
            errorCount += 1.0
    print "总体错误率为: %f" % (errorCount/float(numTestVecs))


def classifyperson():  # 约会分类实战
    resultList = ['not at all', 'in small doses', 'in large doses']
    perc = float(raw_input(unicode("玩电脑游戏的时间比例？", 'utf-8').encode('gbk')))
    flym = float(raw_input(unicode("每年获得的飞行里程数？", 'utf-8').encode('gbk')))
    icec = float(raw_input(unicode("每年吃多少冰淇淋？", 'utf-8').encode('gbk')))
    X = np.array([flym, perc, icec])
    datingDataMat, datingLabels = file2Matrix('data/datingTestSet2.txt')
    normDataMat, ranges, minVals = autoNorm(datingDataMat)
    classifierResult = classify0((X - minVals)/ranges,
                                 normDataMat, datingLabels, 3)
    print "你可能会觉得这个人: ", resultList[classifierResult-1]


def hdwClassTest():  # 手写体识别
    trainingFileList = os.listdir('data/trainingDigits')
    m = len(trainingFileList)
    traingMat = np.zeros((m, 1024))
    hwLabel = []
    for i in range(m):
        fileNameStr = 'data/trainingDigits/%s' % trainingFileList[i]
        traingMat[i, :] = img2vector(fileNameStr)
        hwLabel.append(int(trainingFileList[i].split('_')[0]))
    errorCount = 0.0
    testFileList = os.listdir('data/testDigits')
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = 'data/trainingDigits/%s' % testFileList[i]
        testVec = img2vector(fileNameStr)
        testLab = int(testFileList[i].split('_')[0])
        classifierResult = classify0(testVec, traingMat, hwLabel, 3)
        print '分类器结果: %d, 实际标签: %d' % (classifierResult, testLab)
        if (classifierResult != testLab):
            errorCount += 1.0
        print "错误率为：%f" % (errorCount/float(mTest))

if __name__ == "__main__":
    #plotMain()
    #datingClassTest()
    #classifyperson()
    hdwClassTest()
