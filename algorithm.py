#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import utils
import copy as cp

def procBased(valueList,init,finalMatrix):
    print "Proc based"

    contentActionListFinal = []
    startAct = init
    currentAct = startAct
    for i in range(1):

        stateList = finalMatrix[currentAct]

        max_idx = np.argmax(stateList)
        stateListCopy = cp.deepcopy(stateList)
        currentAct = max_idx
        contentActionListFinal.append(currentAct) #获取每行有效值中最大值的下标

        finalActionList = []
        for j in range(10):
            maxIndex = np.argmax(stateListCopy)
            stateListCopy[maxIndex] = 0
            finalActionList.append(maxIndex) #获取有效值中的前十的下标，该十个数值作为比较对象
    return contentActionListFinal, finalActionList

def contentBased(valueList,init,finalMatrix):
    print "Content based"

    contentActionListFinal = []
    startAct = init
    currentAct = startAct
    for i in range(1):

#找到每一行的最大值,操作对象为下标为init的这一行
        stateList = finalMatrix[currentAct]

        max_idx = np.argmax(stateList)
        while stateList[max_idx] >= 0.9:  #把对称矩阵中值为1 的元素置0
            stateList[max_idx] = 0.0
            max_idx = np.argmax(stateList)
        stateListCopy = cp.deepcopy(stateList) #复制当前的stateList，即无效值归零后的stateList
        '''
        while max_idx in contentActionListFinal:

            stateList[max_idx] = 0.0
            max_idx = np.argmax(stateList)
        '''
        currentAct = max_idx

        contentActionListFinal.append(currentAct)
        finalActionList = []
        for j in range(10):  #找到权值最大的前十进行比较
            maxIndex = np.argmax(stateListCopy)
            stateListCopy[maxIndex] = 0.0
            finalActionList.append(maxIndex)



    #outRes = utils.performanceEvaluation(contentActionListFinal,startAct,valueList)

    return contentActionListFinal, finalActionList  #contentActionListFinal：对称矩阵中每行的有效数值中最大的数对应的下标
                                                    #finalActionList: 有效值的前十的下标，

def linkedBase(actionSelectList,listss,valueList,init):#同上，找到最大和前十
    print "Linked based"
    startAct = init
    currAct = startAct
    alreadyList = []
    linkedActionListFinal = []
    for i in range(1):
        alreadyList.append(currAct)
        currAct,actionList = utils.simActionSelct(actionSelectList,listss, valueList, currAct, startAct,[])
        linkedActionListFinal.append(currAct)
    #print valueList[startAct][linkedActionListFinal[9]] + valueList[linkedActionListFinal[9]][startAct]
    #outRes = utils.performanceEvaluation(linkedActionListFinal,startAct,valueList)
    return linkedActionListFinal, actionList



def singleRL(actionSelectList,listss,valueList,init):  #singleRL计算，获得最大
     #choice a start agent for single agent Reinforcement Learning
    print "Single RL"
    SingleActionListFinal = []
    startAct = init
    currAct = startAct
    finalList = []
    for i in range(10):
        actionSelctList = utils.actionSelctList(actionSelectList,listss, valueList, currAct, startAct)
        j = 0
        while actionSelctList[j] in []:
            j = j + 1
        #currAct = utils.actionSelct(actionSelectList,listss, valueList, currAct, startAct)
        #print actionSelctList
        currAct = actionSelctList[j]
        SingleActionListFinal.append(currAct)
        finalList = actionSelctList
    #print valueList[startAct][SingleActionListFinal[9]] + valueList[SingleActionListFinal[9]][startAct]
    #outRes = utils.performanceEvaluation(SingleActionListFinal,startAct,valueList)
    finalList = actionSelctList
    return SingleActionListFinal, finalList

def multiRLwithoutCompete(actionSelectList,listss,valueList,initAgent):#考虑多因素且在没有竞争的环境中找到最佳
    print "Mutli RL without Compete"
    mutipAction = []
    finalList = []
    for k in initAgent:
        SingleActionListFinal = []
        currAct = k
        startAct = currAct
        for i in range(10):
            actionSelctList = utils.actionSelctList(actionSelectList,listss, valueList, currAct, startAct)#获取actionSelectList
            #currAct = utils.actionSelct(actionSelectList,listss, valueList, currAct, startAct)
            #print actionSelctList
            j = 0
            while actionSelctList[j] in []:
                j = j + 1
            currAct = actionSelctList[j]
            SingleActionListFinal.append(currAct)
        mutipAction.append(SingleActionListFinal)
        finalList.append(actionSelctList)
    #print mutipAction
   # totalRank = []
    #for i in range(len(initAgent)):
        ##totalRank.append(outRes[9])
    return mutipAction,finalList

def multiRLwithCompete(actionSelectList,listss,valueList, initAgent):#考虑竞争性
    #Mutiple agent reinforcement Leanring with compete
    print "Mutli RL with Compete"
    actionAll = []
    finalList = []
    currentAgent = initAgent
    for i in range(10):
        actionRangeList = []
        for j in range(len(currentAgent)):
            startAct = initAgent[j]
            currAct = currentAgent[j]
            actionSelctList = utils.actionSelctList(actionSelectList,listss, valueList, currAct, startAct)
            actionRangeList.append(actionSelctList)
        if i == 9:
            finalList = actionRangeList
        oldactionRangeList = actionRangeList
        actionRangeList = np.array(actionRangeList).T
        currentAgent = actionRangeList[0]
        for m in range(len(currentAgent)):
            singAgent = currentAgent[m]
            level = 0
            takeList = []
            for k in range(len(currentAgent)):
                compareAgent = currentAgent[k]
                if m != k:
                        if compareAgent == singAgent:
                            #print 'compete'
                            singValue = valueList[initAgent[m]][singAgent] + valueList[singAgent][initAgent[m]]
                            compareValue = valueList[initAgent[k]][compareAgent] + valueList[compareAgent][initAgent[k]]
                            if singValue < compareValue:
                                if level < 9:
                                    level = level + 1
                                temp = actionRangeList[level][m]
                                while temp in currentAgent[:m] and level < 9:
                                    level = level + 1
                                    temp = actionRangeList[level][m]
                                    #print temp
                                currentAgent[m] = temp
                                singAgent = currentAgent[m]
        #print 'next round'
        #print currentAgent
        actionAll.append(currentAgent.tolist())
    actionAll = np.array(actionAll).T
    actionAll = actionAll.tolist()
    '''
    totalValues = 0
    for i in range(len(initAgent)):
        totalValues = totalValues + valueList[initAgent[i]][actionAll[i][9]] + valueList[actionAll[i][9]][initAgent[i]]
    averageValue = totalValues/len(initAgent)
    print averageValue
    '''
    #totalRank = []
    #for i in range(len(initAgent)):
        #outRes = utils.performanceEvaluation(actionAll[i],initAgent[i],valueList)
        #totalRank.append(outRes[9])
    return actionAll, finalList



'''
    nextAgent = []

    for i in range(100):
        nextAgent.append(-1)


    competeList = finds(currentAgent, np.unique(currentAgent))
    for k in range(len(competeList)):
        print competeList[k]
        if len(competeList[k]) != 1:
            holdList = []
            for m in range(len(competeList[k])):
                holdList.append(valueList[initAgent[competeList[k][m]]][currentAgent[m]])
            nextAgent[competeList[k][np.argmax(holdList)]] = currentAgent[competeList[k][np.argmax(holdList)]]
            currentAgent[competeList[k][np.argmax(holdList)]] = -1
            tempMax = np.argmax(holdList)
            for l in range(len(competeList[k])):
                if l != np.argmax(holdList):
                    currentAgent[competeList[k][l]] = currentAgent[competeList[1][l]]
        else:
            nextAgent[competeList[k][0]] = currentAgent[competeList[k][0]]
            currentAgent[competeList[k][0]] = -1
    count = 2
    while np.unique(currentAgent) !=1:
        competeList = finds(currentAgent, np.unique(currentAgent))
        for k in range(1, len(competeList)):
            print competeList[k]
            if len(competeList[k]) != 1:
                holdList = []
                for m in range(len(competeList[k])):
                    holdList.append(valueList[initAgent[competeList[k][m]]][currentAgent[m]])
                nextAgent[competeList[k][np.argmax(holdList)]] = currentAgent[competeList[k][np.argmax(holdList)]]
                currentAgent[competeList[k][np.argmax(holdList)]] = -1
                tempMax = np.argmax(holdList)
                for l in range(len(competeList[k])):
                    if l != np.argmax(holdList):
                        currentAgent[competeList[k][l]] = currentAgent[competeList[count][l]]
                        count = count + 1
            else:
                nextAgent[competeList[k][0]] = currentAgent[competeList[k][0]]
                currentAgent[competeList[k][0]] = -1
    break



'''