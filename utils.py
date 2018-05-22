#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import numpy as np
import copy as cp
#import DynamicTimeWarping as dtw


#sort the combimlist to a matrix of timeseris
def sortToTimeSeries(combineList):
    #get the min and max year for all the author's publication length

    uniqueAuthor = np.unique(combineList[:, 0])
    np.savetxt('author.txt',uniqueAuthor.astype(int),fmt='%i')
    lenAuthor = len(uniqueAuthor)

    uniqueYear = np.unique(combineList[:, 1])
    lenYear = len(uniqueYear)
    uniqueCategory = np.unique(combineList[:, 2])
    lenCategory = len(uniqueCategory)

    #sort the comList by author
    #combineList = combineList[np.argsort(combineList[:, 0])]

    allAuthorTimeArray = np.zeros((lenAuthor,lenYear,lenCategory))
    for i in range (len(combineList)):
        x = np.where(uniqueAuthor == combineList[i][0])[0][0]
        y = np.where(uniqueYear == combineList[i][1])[0][0]
        z = np.where(uniqueCategory == combineList[i][2])[0][0]
        allAuthorTimeArray[x][y][z] += 1

    return  allAuthorTimeArray


#function used to conver the list of author pubulication and catergory to different set based on the unit limited
def covertListToSet(allAuthorTimeArray,minAmountForEveryUnit):
    timeArrayLenth = len(allAuthorTimeArray)
    x = timeArrayLenth/minAmountForEveryUnit
    y = timeArrayLenth%minAmountForEveryUnit
    firstTimeFLag = True
    for i in range(x):
        if firstTimeFLag:
            singleUnit = allAuthorTimeArray[i*minAmountForEveryUnit:(i+1)*minAmountForEveryUnit,:,:]
            authorList_hashable = map(np.array, [singleUnit])
            firstTimeFLag = False
        else:
            singleUnit = allAuthorTimeArray[i*minAmountForEveryUnit:(i+1)*minAmountForEveryUnit,:,:]
            authorList_hashable.append(singleUnit)

    singleUnit = allAuthorTimeArray[x*minAmountForEveryUnit:timeArrayLenth,:,:]
    authorList_hashable.append(singleUnit)

    return authorList_hashable


#function to compute similarity for each thread
def computeMatrixForEachUnit(authorTimeArrayHash, totalUnit, eachThreadAmount, currentThread, matrixName):
    count = 0
    finished = 0
    if matrixName == 'DTW':
        threadCurrentCount = currentThread * 2
    else:
        threadCurrentCount = currentThread * 2 + 1
    for x in range (totalUnit):
        for y in range(totalUnit):
            if x >= y:
                if count >= currentThread*eachThreadAmount and count < (currentThread+1)*eachThreadAmount:
                    m = dtw.KnnDtw()
                    authorSimMatrix = m._dist_matrix(authorTimeArrayHash[x],authorTimeArrayHash[y])
                    np.savetxt(str(x)+'_'+str(y) +'_'+matrixName+'.txt', authorSimMatrix,fmt="%i")
                    finished = finished + 1
                    print 'Thread - '+ str(threadCurrentCount) + ' finish: ' + str(finished) + '/' + str(eachThreadAmount)
                count = count + 1

def actionSelct(actionSelectList,listss, valueList, currAct, startAct):
    popList = []
    simList = []
    totalList = []
    actions = actionSelectList[currAct]
    for action in actions:
        popValue = listss[action]
        simValue = valueList[currAct][action] + valueList[action][currAct]
        simValue1 = valueList[startAct][action] + valueList[action][startAct]
        totalValue = popValue + simValue + simValue1
        popList.append(popValue)
        simList.append(simValue)
        totalList.append(totalValue)
    selectAct = actions[np.argmax(totalList)]
    return selectAct



def simActionSelct(actionSelectList,listss, valueList, currAct, startAct, alreadyList):
    popList = []
    simList = []
    totalList = []
    actions = actionSelectList[currAct]
    for action in actions:
        popValue = listss[action]
        simValue = valueList[currAct][action] + valueList[action][currAct]
        simValue1 = valueList[startAct][action] + valueList[action][startAct]
        totalValue = simValue
        popList.append(popValue)
        simList.append(simValue)
        totalList.append(totalValue)
    simCopy = cp.deepcopy(simList)
    selectAct = actions[np.argmax(simList)]
    while selectAct in alreadyList:
        simList[np.argmax(simList)] = -1
        selectAct = actions[np.argmax(simList)]#找到最大的
    actList = []
    for i in range(10):#找到前十
        actTemp = actions[np.argmax(simCopy)]
        simCopy[np.argmax(simCopy)] = -1
        actList.append(actTemp)
    print selectAct,actList
    return selectAct,actList



def actionSelctList(actionSelectList,listss, valueList, currAct, startAct):
    popList = []
    simList = []
    totalList = []
    actions = actionSelectList[currAct]
    for action in actions:
        popValue = listss[action]
        simValue = valueList[currAct][action] + valueList[action][currAct]
        simValue1 = valueList[startAct][action] + valueList[action][startAct]
        totalValue = 0.000001*popValue + 1*simValue1
        popList.append(popValue)
        simList.append(simValue)
        totalList.append(totalValue)
    selectActList = []
    for i in range(10):
        selectAct = actions[np.argmax(totalList)]
        totalList[np.argmax(totalList)] = -1
        selectActList.append(selectAct)
    return selectActList




def compputeRank(inputAgent):
    f = open("simFile", "r")
    valueList = []
    k = 0
    for line in f:
        lineList = line.split(',')
        lineValueList = []
        for i in range(len(lineList)):
            if i == 0:
                temp = lineList[i].replace('[','')
            elif i == len(lineList)-1:
                temp = lineList[i].replace(']','')
            else:
                temp = lineList[i]
            lineValueList.append(np.float64(temp))
        valueList.append(lineValueList)
    valueList = np.array(valueList)
    tranValueList = valueList.T

    allValueSumList = []
    i = inputAgent
    valueSumList = []
    for j in range(len(valueList)):
        temp = valueList[i][j] + tranValueList[i][j]
        valueSumList.append([temp,j])
    allValueSumList.append(valueSumList)
    allValueSumList = sorted(allValueSumList,key=lambda x: x[0])
    output = []
    for j in range(len(valueList)):
        output.append(allValueSumList[1])
    return output

def performanceEvaluation(actionList, agent, valueList):
    valueList = np.array(valueList)
    tranValueList = valueList.T
    valueSumList = []
    for j in range(len(valueList)):
        temp = valueList[agent][j] + tranValueList[agent][j]
        valueSumList.append(temp)
    #print valueSumList
    seq = sorted(valueSumList,reverse=True)
    index = [seq.index(v) for v in valueSumList]
    outIndex = [index[a] for a in actionList]
    return outIndex



