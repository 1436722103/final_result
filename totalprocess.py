#encoding:utf-8
import numpy as np

def npmax(l):
    argList=[]
    for i in range(len(l)):
        max_idx = np.argmax(l)
        l[max_idx] = -1
        argList.append(max_idx)
    return  argList


vlist=np.loadtxt("V.txt")#计算之后得到的finalstatue，每个人的popularity
contentlist = np.loadtxt("contentfinalMatrix")#content因子
proclist =np.loadtxt("procfinalMatrix")#proceedings因子
titlelist =np.loadtxt("titlefinalMatrix")#title因子
keywordlist =np.loadtxt("keyfinalMatrix")#keyword因子

W=[0.49084937,0.98613076,0.9109054,0.96451163]#迭代更新后得到的θ

for i in range(len(contentlist)):#将自身与自身的相关性设为0
    for j in range(len(contentlist)):
        if i==j:
            contentlist[i][j]=0
            proclist [i][j]= 0
            titlelist[i][j] = 0
            keywordlist[i][j] = 0

print "calculation starts"

#下列代码计算了所有学者结合自身属性迭代后的popularity，并获得totalList
totalList=[]#记录每个学者结合自身属性迭代后的popularity
actionList = []#保存第一步的推荐结果
for i in range(len(vlist)):#但我们只需要计算actionSeletList中出现的学者
    finalLineVlist=[]
    for j in range(len(vlist)):
        inputlist=[contentlist[i][j],proclist[i][j],titlelist[i][j], keywordlist[i][j]]
        sum=np.dot(np.array(inputlist).T,np.array(W))#分别计算每个人的自身属性
        sum += vlist[i]#自身属性与popularity加和，数据用于获得最终的finalSelectActionList
        finalLineVlist.append(sum)
    print finalLineVlist
    actionList.append(npmax(finalLineVlist))
    totalList.append(finalLineVlist)
np.savetxt("totalList",totalList,fmt="%.6f")
np.savetxt("actionList.file",actionList,fmt="%d")
print "calculation ended"







