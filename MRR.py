#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import algorithm as alg
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import ndcg as nd

# 转换用，对学者四个因子一行值加和，作为其研究方向的权值
def sumReward(valueList):
    sumOutput = []
    for i in range(len(valueList)):
        sumOutput.append(sum(valueList[i]))
    return sumOutput


#获取title信息的tfidf值并输出这个矩阵构造的对称矩阵(两两之间相互的相似值相同)，对角线全是1
def getTitle():
    f = open("titleBasedNewReal", "r")#各学者的文献的title信息
    txtList = []
    tempHolder = ''
    count = 0
    for line in f:
        if "............" in line:
            txtList.append(tempHolder)
            tempHolder = ''
        else:
            tempHolder = tempHolder + str(line)
    vect = TfidfVectorizer(min_df=1)#tfidf算法实现
    tfidf = vect.fit_transform(txtList)
    finalMatrix = (tfidf * tfidf.T).A
    np.savetxt("titlefinalMatrix", finalMatrix,fmt="%f")#写入文件
    return finalMatrix

#获取content信息的tfidf值并输出这个矩阵构造的对称矩阵(两两之间相互的相似值相同)，对角线全是1
def getContent():
    f = open("contentBasedNew", "r")
    txtList = []
    tempHolder = ''
    count = 0
    for line in f:
        if "............" in line:
            txtList.append(tempHolder)
            tempHolder = ''
        else:
            tempHolder = tempHolder + str(line)
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(txtList)
    finalMatrix = (tfidf * tfidf.T).A
    np.savetxt("contentfinalMatrix", finalMatrix,fmt="%f")
    return finalMatrix

#获取keyword信息的tfidf值并输出这个矩阵构造的对称矩阵(两两之间相互的相似值相同)，对角线全是1
def getKeyword():
    f = open("keywordSim", "r")
    txtList = []
    tempHolder = ''
    count = 0
    for line in f:
        if "............" in line:
            txtList.append(tempHolder)
            tempHolder = ''
        else:
            tempHolder = tempHolder + str(line)
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform(txtList)
    finalMatrix = (tfidf * tfidf.T).A
    np.savetxt("keyfinalMatrix.txt", finalMatrix,fmt="%f")
    return finalMatrix

#获取学者在那些会议上出现过的信息（一个编号代表一个会议），并计算两两之间的相似性，计算方法为两行数据的交集除以并集
def getProc():
    f = open("procSim", "r")
    txtList = []
    tempHolder = ''
    count = 0
    for line in f:
        if "............" in line:
            txtList.append(tempHolder)
            tempHolder = ''
        else:
            tempHolder = tempHolder + str(line)
    valueList=[]
    lineValueList=[]
    # for i in range(10):
    for i in range(len(txtList)):
        listA = txtList[i].replace("\n", "").split(" ")#将回车去掉并根据空格分隔开
        listA = listA[1:]#去掉首元素空（‘’）
        for j in range(len(txtList)):
            # print len(txtList)
            listB = txtList[j].replace("\n","").split(" ")
            listB = listB[1:]

            if listA != [] and listB != []:
                outer =np.union1d(listA,listB)#获得并集
                inner = np.intersect1d(listA,listB)#获得交集
                lineValueList.append((float(len(inner))/float(len(outer))))#获得计算值
            else:
                lineValueList.append(0)#自己与自己的相似值标记为0
        valueList.append(lineValueList)
    np.savetxt("procfinalMatrix", valueList, fmt="%f")
    return valueList

def titleSimEvaluation(actionSelectList,listss,
                       valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, testAuthorList):
    num = 0
    total = 0.0
    count = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    finalMatrix = getTitle()

    for i in range(len(testAuthorList)):
        if Author2Num[testAuthorList[i]] in b2s:
            startPoint = b2s[Author2Num[testAuthorList[i]]]
            num = num + 1
            #print num
        else:
            continue
        singleTotal = []
        singleAct,finalList = alg.contentBased(valueList,startPoint,finalMatrix)#找到finalMatrix[startPoint]这一行的最
                                                                                # 大和前十的下标

        r = []
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                r.append(1)
            else:
                r.append(0)
        ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
        ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
        ndcg10 = ndcg10 + nd.ndcg_at_k(r,10)

        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count = count + 1

        for l in range(3):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count3 = count3 + 1


        for l in range(5):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count5 = count5 + 1

        rank = 11
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                rank = l
                print rank
                break
        total = total+ 1.0/float(rank+1)
    print total, count, count3, count5,ndcg3,ndcg5,ndcg10
    return total, count, count3, count5,ndcg3,ndcg5,ndcg10

def contentSimEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, testAuthorList):
    num = 0
    total = 0.0
    count = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    finalMatrix = getContent()

    for i in range(len(testAuthorList)):
        if Author2Num[testAuthorList[i]] in b2s:
            startPoint = b2s[Author2Num[testAuthorList[i]]]
            num = num + 1
            #print num
        else:
            continue
        singleTotal = []
        singleAct,finalList = alg.contentBased(valueList,startPoint,finalMatrix)

        r = []
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                r.append(1)
            else:
                r.append(0)
        ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
        ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
        ndcg10 = ndcg10 + nd.ndcg_at_k(r,10)

        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count = count + 1

        for l in range(3):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count3 = count3 + 1


        for l in range(5):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count5 = count5 + 1

        rank = 11
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                rank = l
                print rank
                break
        total = total+ 1.0/float(rank+1)
    return total, count, count3, count5,ndcg3,ndcg5,ndcg10

def procSimEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, testAuthorList):
    num = 0
    total = 0.0
    count = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    finalMatrix = getProc()

    for i in range(len(testAuthorList)):
        if Author2Num[testAuthorList[i]] in b2s:
            startPoint = b2s[Author2Num[testAuthorList[i]]]
            num = num + 1
            #print num
        else:
            continue
        singleTotal = []
        singleAct,finalList = alg.procBased(valueList,startPoint,finalMatrix)

        r = []
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                r.append(1)
            else:
                r.append(0)
        ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
        ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
        ndcg10 = ndcg10 + nd.ndcg_at_k(r,10)

        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count = count + 1

        for l in range(3):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count3 = count3 + 1


        for l in range(5):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count5 = count5 + 1

        rank = 11
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                rank = l
                print rank
                break
        total = total+ 1.0/float(rank+1)
    return total, count, count3, count5,ndcg3,ndcg5,ndcg10

def keywordSimEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, testAuthorList):
    num = 0
    total = 0.0
    count = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    finalMatrix = getKeyword()

    for i in range(len(testAuthorList)):
        if Author2Num[testAuthorList[i]] in b2s:
            startPoint = b2s[Author2Num[testAuthorList[i]]]
            num = num + 1
            #print num
        else:
            continue
        singleTotal = []
        ssingleAct,finalList = alg.contentBased(valueList,startPoint,finalMatrix)

        r = []
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                r.append(1)
            else:
                r.append(0)
        ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
        ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
        ndcg10 = ndcg10 + nd.ndcg_at_k(r,10)

        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count = count + 1

        for l in range(3):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count3 = count3 + 1


        for l in range(5):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count5 = count5 + 1

        rank = 11
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                rank = l
                print rank
                break
        total = total+ 1.0/float(rank+1)
    return total, count, count3, count5,ndcg3,ndcg5,ndcg10

def linkSimEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, testAuthorList):
    num = 0
    total = 0.0
    count = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    for i in range(len(testAuthorList)):
        if Author2Num[testAuthorList[i]] in b2s:
            startPoint = b2s[Author2Num[testAuthorList[i]]]
            num = num + 1
            #print num
        else:
            continue
        singleTotal = []
        singleAct,finalList = alg.linkedBase(actionSelectList,listss,valueList,startPoint)

        r = []
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                r.append(1)
            else:
                r.append(0)
        ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
        ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
        ndcg10 = ndcg10 + nd.ndcg_at_k(r,10)

        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count = count + 1

        for l in range(3):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count3 = count3 + 1


        for l in range(5):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count5 = count5 + 1

        rank = 11
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                rank = l
                print rank
                break
        total = total+ 1.0/float(rank+1)
    return total, count, count3, count5,ndcg3,ndcg5,ndcg10


def singleAgentEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, testAuthorList):
    num = 0
    total = 0.0
    count = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    for i in range(len(testAuthorList)):
        if Author2Num[testAuthorList[i]] in b2s:
            startPoint = b2s[Author2Num[testAuthorList[i]]]
            num = num + 1
            #print num
        else:
            continue
        singleTotal = []
        singleAct,finalList = alg.singleRL(actionSelectList,listss,valueList,startPoint)


        r = []
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                r.append(1)
            else:
                r.append(0)
        ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
        ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
        ndcg10 = ndcg10 + nd.ndcg_at_k(r,10)

        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count = count + 1

        for l in range(3):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count3 = count3 + 1


        for l in range(5):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                count5 = count5 + 1

        rank = 11
        for l in range(10):
            if Num2Author[s2b[finalList[l]]] in AuthorMatch[testAuthorList[i]]:
                rank = l
                print rank
                break
        total = total+ 1.0/float(rank+1)
    return total, count, count3, count5, ndcg3,ndcg5,ndcg10

def mutliWithEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, verfiyAgentList, testAuthorList):
    count = 0
    total = 0.0
    last = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    for i in range(len(testAuthorList)):
        print i
        indexValue = verfiyAgentList.index(testAuthorList[i])
        if indexValue < 15:
            initAgent = verfiyAgentList[indexValue:indexValue + 20]
        elif indexValue > 900:
            initAgent = verfiyAgentList[indexValue-20:indexValue]
        else:
            initAgent = verfiyAgentList[indexValue-10:indexValue + 10]

        #multiRLwithoutAct = alg.multiRLwithoutCompete(actionSelectList,listss,valueList,initAgent)
        multiRLwithAct,finalList = alg.multiRLwithCompete(actionSelectList,listss,valueList,initAgent)
        for j in range(20):
            singleAct = finalList[j]
            rank = 11
            for l in range(10):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    rank = l
                    break
            total = total+ 1.0/float(rank+1)

        for j in range(20):
            singleAct = finalList[j]
            r = []
            for l in range(10):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    r.append(1)
                else:
                    r.append(0)

            ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
            ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
            ndcg10 =ndcg10 + nd.ndcg_at_k(r,10)



        for j in range(20):
            singleAct = finalList[j]
            for l in range(10):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    count = count + 1
        for j in range(20):
            singleAct = finalList[j]
            for l in range(3):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    count3 = count3 + 1
        for j in range(20):
            singleAct = finalList[j]
            for l in range(5):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    count5 = count5 + 1
    return total, count, count3, count5, ndcg3,ndcg5,ndcg10


def mutliWithoutEvaluation(actionSelectList,listss,valueList, AuthorList, AuthorMatch, Author2Num, Num2Author, s2b,b2s, verfiyAgentList, testAuthorList):
    count = 0
    total = 0.0
    last = 0
    count3 = 0
    count5 = 0
    ndcg3 = 0
    ndcg5 = 0
    ndcg10 = 0
    for i in range(len(testAuthorList)):
        print i
        indexValue = verfiyAgentList.index(testAuthorList[i])
        if indexValue < 15:
            initAgent = verfiyAgentList[indexValue:indexValue + 20]
        elif indexValue > 900:
            initAgent = verfiyAgentList[indexValue-20:indexValue]
        else:
            initAgent = verfiyAgentList[indexValue-10:indexValue + 10]

        multiRLwithoutAct,finalList = alg.multiRLwithoutCompete(actionSelectList,listss,valueList,initAgent)
        #multiRLwithAct = alg.multiRLwithCompete(actionSelectList,listss,valueList,initAgent)
        for j in range(20):
            singleAct = finalList[j]
            rank = 11
            for l in range(10):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    rank = l
                    break
            total = total+ 1.0/float(rank+1)

        for j in range(20):
            singleAct = finalList[j]
            r = []
            for l in range(10):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    r.append(1)
                else:
                    r.append(0)

            ndcg3 = ndcg3 + nd.ndcg_at_k(r,3)
            ndcg5 = ndcg5 + nd.ndcg_at_k(r,5)
            ndcg10 =ndcg10 + nd.ndcg_at_k(r,10)


        for j in range(20):
            singleAct = finalList[j]
            for l in range(10):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    count = count + 1

        for j in range(20):
            singleAct = finalList[j]
            for l in range(3):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    count3 = count3 + 1
        for j in range(20):
            singleAct = finalList[j]
            for l in range(5):
                if Num2Author[s2b[singleAct[l]]] in AuthorMatch[Num2Author[s2b[initAgent[j]]]]:
                    count5 = count5 + 1
    return total, count, count3, count5,ndcg3,ndcg5,ndcg10

if __name__=="__main__":
    getProc()
    # getKeyword()
    # getContent()
    # getTitle()
