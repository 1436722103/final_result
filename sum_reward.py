import numpy as np
import sys
reload(sys)
sys.setdefaultencoding("utf8")
def i():
    # f = open("simFile", "r")
    f = open("ListB.txt", "r")
    valueList = []
    k = 0
    for line in f:
        lineList = line.split(' ')
        # print lineList
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

    # f = open("valueListFile", "w")
    # f.write(valueList)
    # f.close()#

    print valueList.shape
   # print valueList[4419][4419]

    # tranValueList = valueList.T

    # valueSumList = []
    # allValueSumList = []
    # for i in range(len(valueList)):
    #     for j in range(len(valueList)):
    #         temp = valueList[i][j]
    #         # temp = valueList[i][j] + tranValueList[i][j]
    #         # print "temp="+temp
    #         valueSumList.append(temp)
    #     allValueSumList.append(valueSumList)

   # print allValueSumList.shape
    #
    #
    f = open("newSumSimFile", "w")
    f.write("\n".join(map(lambda x: str(x), valueList)))
    f.close()


if __name__ == '__main__':
    i()
    