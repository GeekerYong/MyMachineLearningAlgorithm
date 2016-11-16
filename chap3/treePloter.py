# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 12:08:49 2016

@author: JinYong Liu
@codestyle:PEP8

决策树绘图
所有xxxPt均为坐标，形式为(X,Y)，绘图的顺序为从上到下，从左到右
关键点：
比例化绘图，无需关心输出图形的大小
获取树深度(getTreeDepth)
获取树宽度（叶子节点）(getNumLeafs)
绘制节点(决策节点，叶子节点)，箭头(plotNode)
在箭头中部输出文本(plotMidText)
"""

import matplotlib.pyplot as plt

# 定义叶子，决策，箭头的样式
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(
             nodeTxt, xy=parentPt,  xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def getNumLeafs(myTree):
    numleafs = 0
    firstStr = myTree.keys()[0]
    secDic = myTree[firstStr]
    for key in secDic.keys():
        if type(secDic[key]).__name__ == 'dict':
            numleafs += getNumLeafs(secDic[key])
        else:
            numleafs += 1
    return numleafs


def getTreeDepth(myTree):
    maxDepth = 0
    nowbranDepth = 0
    firstStr = myTree.keys()[0]
    secDic = myTree[firstStr]
    for key in secDic.keys():
        if type(secDic[key]).__name__ == 'dict':
            nowbranDepth = 1 + getTreeDepth(secDic[key])
        else:
            nowbranDepth = 1
    if nowbranDepth > maxDepth:
        maxDepth = nowbranDepth
    return maxDepth


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,
              plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)  # 绘制箭头连线上的文字
    firstStr = myTree.keys()[0]  # 该节点的label文字信息
    plotNode(firstStr, cntrPt, parentPt, decisionNode)  # 绘制当前节点
    secDic = myTree[firstStr]  # 准备绘制当前节点子树或叶子节点
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  # 下一个节点的纵坐标将下移
    for key in secDic.keys():
        if type(secDic[key]).__name__ == 'dict':
            plotTree(secDic[key], cntrPt, str(key))  # 递归调用,绘制子树
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW  # 绘制叶子节点
            plotNode(secDic[key], (plotTree.xOff, plotTree.yOff),
                     cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))  # 为比例化绘图做准备
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
    return listOfTrees[i]
