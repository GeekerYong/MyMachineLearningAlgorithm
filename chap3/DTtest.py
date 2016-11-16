# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:34:11 2016

@author: JinYong Liu
@codestyle:PEP8

决策树分类测试
"""
import decisionTree
import treePloter


def classify0(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    featIndex = featLabels.index(firstStr)  # 找到第一个用于分类特征的位置
    secDic = inputTree[firstStr]
    for key in secDic.keys():
        if testVec[featIndex] == key:
            if type(secDic[key]).__name__ == 'dict':
                classLabel = classify0(secDic[key], featIndex, testVec)
            else:
                classLabel = secDic[key]
    return classLabel


#  利用pickle来进行持久化存储
def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()


def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)


if __name__ == "__main__":
    fr = open('data/lenses.txt')
    lenses = [example.strip().split('\t') for example in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = decisionTree.creatTree(lenses, lensesLabels)
    treePloter.createPlot(lensesTree)