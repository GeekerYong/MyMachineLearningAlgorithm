# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 09:32:40 2016

@author: JinYong Liu
@codestyle:PEP8

决策树(ID3划分)
优点：计算复杂度不高，输出结果易于理解，中间值缺失不敏感，可处理不相关的特征
缺点：容易过拟合
使用数据类型：数值型(CART)和标称型(ID3)
"""

import math
import operator


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}
    for featVec in dataSet:  # 统计每一个类别的样例数目
        currentLabel = featVec[-1]
        if currentLabel not in labelCount.keys():
            labelCount[currentLabel] = 0
        labelCount[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCount:  # 按公式求熵
        prob = float(labelCount[key])/numEntries
        shannonEnt -= prob*math.log(prob, 2)
    return shannonEnt


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


def chooseBestFeatToSplit(dataSet):
    baseEnt = calcShannonEnt(dataSet)  # 最初的无序度量值
    numFeat = len(dataSet[0])-1  # 去除label的长度
    bestInfoGain = 0.0
    bestFeat = -1
    for i in range(numFeat):
        featList = [example[i] for example in dataSet]  # 获取第i个特征的所有样本值
        uniqueVals = set(featList)  # python的神奇魔法,获取列表唯一元素值最6的方法
        newEnt = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))  # 依据信息增益的计算公式需要
            newEnt += prob*calcShannonEnt(subDataSet)
        infoGain = baseEnt - newEnt
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeat = i
    return bestFeat


def majorityCnt(classList):  # 多数决
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def creatTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):  # 递归结束条件1
        return classList[0]
    if len(dataSet[0]) == 1:  # 递归结束条件2
        return majorityCnt(classList)
    bestFeat = chooseBestFeatToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVal = set(featValues)
    for value in uniqueVal:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = creatTree(splitDataSet\
        (dataSet, bestFeat, value),subLabels)  # 字典嵌套式创建树
    return myTree
   
def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


if __name__ == "__main__":
    dataSet, labels = createDataSet()
    calcShannonEnt(dataSet)
    print chooseBestFeatToSplit(dataSet)
    print majorityCnt(classlist)
    