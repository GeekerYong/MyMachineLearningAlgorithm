# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:42:12 2016

@author: JinYong Liu
@codestyle:PEP8

朴素贝叶斯分类模型
优点：数据量小的情况下依旧有效，可处理多类别问题
缺点：对于数据的输入方式敏感
适用数据类型：标称型
"""
import numpy as np
import os
import random
#############################文档处理####################################


def textParse(bigString):  #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]


def loadData():
    dataSet = []
    labels = []
    posFileNameSet = os.listdir('email/ham')
    for name in posFileNameSet:
        fr = open('email/ham/' + name)
        docVec = textParse(fr.read())
        dataSet.append(docVec)
        labels.append(1)
    negFileNameSet = os.listdir("email/spam")
    for name in negFileNameSet:
        fr = open('email/spam/' + name)
        docVec = textParse(fr.read())
        dataSet.append(docVec)
        labels.append(0)
    return dataSet, labels


def creatWordList(dataSet):  # 创建文档词汇集合
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # '|'为并集符号
    return list(vocabSet)


def setOfWord2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word %s not in vocabList" % word
    return returnVec


def bagOfWord2Vec(vocabList, inputSet):
    reuturnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            reuturnVec[vocabList.index(word)] += 1
        else:
            print "the word %s not in vocabList" % word
############################END 文档处理##################################

############################分类器构建####################################


def trainNB(trainMartix, trainClassLabel):
    numTrainExp = len(trainMartix)
    numWords = len(trainMartix[0])
    p0Num = np.zeros(numWords)  # 初始化概率
    p1Num = np.zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainExp):
        if trainClassLabel[i] == 1:  # 统计当分类为1类时，特征的分布
            p1Num += trainMartix[i]  # 这样写可以兼容两种不同的文本表示模型
            p1Denom += sum(trainMartix[i])  # 1类文档的总词数
        else:
            p0Num += trainMartix[i]
            p0Denom += sum(trainMartix[i])
    p1Vect = np.log(p1Num/p1Denom)  # 取对数 防止有一项概率为零或过于小出现下溢出
    p0Vect = np.log(p0Num/p0Denom)
    pPos = sum(trainClassLabel)/float(numTrainExp)  # 计算Pos的概率
    return p1Vect, p0Vect, pPos


def classify(p1Vect, p0Vect, pPos, inputVec):
    p1 = sum(p1Vect*inputVec) + np.log(pPos)
    p0 = sum(p0Vect*inputVec) + np.log(1.0 - pPos)
    if p1 > p0:
        return 1
    else:
        return 0
##########################end 分类器构建##################################
if __name__ == "__main__":
    dataSet, labels = loadData()
    wordList = creatWordList(dataSet)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMatrix = []
    trainClass = []
    for docIndex in trainingSet:
        trainMatrix.append(setOfWord2Vec(wordList, dataSet[docIndex]))
        trainClass.append(labels[docIndex])
    p1V, p0V, pPos = trainNB(trainMatrix, trainClass)
    errorCount = 0
    for docIndex in testSet:
        testVec = setOfWord2Vec(wordList, dataSet[docIndex])
        if classify(p1V, p0V, pPos, testVec) != labels[docIndex]:
            errorCount += 1
    print "the error Rate: ",float(errorCount)/len(testSet)

