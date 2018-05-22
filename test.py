import numpy as np
import copy as cp
f = open("SimFile", "r")
valueList = []
k = 0

def npmax(l):
    max_idx = np.argmax(l)

    l[max_idx] = -1
    max_idx1 = np.argmax(l)

    l[max_idx1] = -1
    max_idx2 = np.argmax(l)

    l[max_idx2] = -1
    max_idx3 = np.argmax(l)

    l[max_idx3] = -1
    max_idx4 = np.argmax(l)

    l[max_idx4] = -1
    max_idx5 = np.argmax(l)

    l[max_idx5] = -1
    max_idx6 = np.argmax(l)

    l[max_idx6] = -1
    max_idx7 = np.argmax(l)

    l[max_idx7] = -1
    max_idx8 = np.argmax(l)

    l[max_idx8] = -1
    max_idx9 = np.argmax(l)

    return [max_idx, max_idx1, max_idx2, max_idx3, max_idx4,max_idx5, max_idx6, max_idx7, max_idx8, max_idx9]


def value():
    global valueList
    for line in f:
        lineList = line.split(' ')
        lineValueList = []
        for i in range(len(lineList)):
            if i == 0:
                temp = lineList[i].replace('[','')
            elif i == len(lineList)-1:
                temp = lineList[i].replace(']','')
            else:
                temp = lineList[i]
            lineValueList.append(temp)
        valueList.append(lineValueList)
    valueList = np.array(valueList)
    tranValueList = valueList.T
    valueSumList = []
    valueList1=[]
    for i in range(len(valueList)):
        for j in range(len(valueList)):
            temp = valueList[i][j] + tranValueList[i][j]
            valueSumList.append(temp)
        valueList1.append(valueSumList)
    return
    valueSumList = []
    allValueSumList = []
    actionList = []
    for i in range(len(valueList)):
        valueSumList = []
        for j in range(len(valueList)):
            temp = valueList[i][j] + tranValueList[i][j]
            valueSumList.append(temp)

        # print valueSumList[i]
        new = npmax(valueSumList)
        # new = npmax(valueList[i])
        #print new
        allValueSumList.append(new)
    # print len(allValueSumList)
    # np.savetxt("newSumSimFile",allValueSumList,fmt="%d")
    return
