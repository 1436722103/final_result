#coding:utf8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import math
import random
import numpy as np
import json
from MRR import *

N = 4420
alpha = 10e-14
gamma = 0.9
theta = 10e-8
actionSelectList = []
with open("neibors-2005-2014.file", "r") as inputfile:#neibors的前十个，形如actionSelectList这个文件
	for line in inputfile:
		line=line.strip().split('\t')
		res=eval(line[1])[:10]
		actionSelectList.append(res)
    # actionSelectList = json.load(inputfile)
    # inputfile.close()


def init():
    global N
    V = [0]*N
    S = range(0,N)
    Pi = [0]*N
    return V,S,Pi

def execute_action(s,a,V,gamma,valueList):
    v=0
    reward = valueList[a]
    v = reward + gamma * V[a]

    return v

def update(gamma,V,s,valueList):
    global N
    action_list = actionSelectList[s]
    new_v = []

    for a in action_list:
        v = execute_action(s,a,V,gamma,valueList)
        new_v.append(v)#第一轮加速V[]=0：new_v[]=valueList[a]

    max_value = max(new_v)
    t = max(new_v)
    max_set = []
    for i in range(len(new_v)):#标记每一组（10个）中的最大
        if new_v[i] == t:
            max_set.append(i)#max_v对应actionSelectList中每一行里对应的valueList[a]最大的actionSelectList中的值的下标


    random.shuffle(max_set)
    action = action_list[max_set[0]]#action对应actionSelectList中每一行里对应的valueList[a]最大的actionSelectList中的值

    return max_value,action



def main_iteration(V,S,Pi,W,inputList):

    print 'start'
    global gamma, theta, alpha
    delta = 9999
    i = 0
    util = np.dot(np.array(inputList).T,np.array(W)).tolist()  #dot是np中的矩阵乘法，tolist()是将矩阵/数组转化成列表的函数
    while delta >= theta:
        i += 1
        W = np.array(W) - np.dot(alpha,np.dot(np.array(inputList),np.array(util)))
        util = np.dot(np.array(inputList).T,np.array(W)).tolist()
        for s in S:
            value = V[s]
            V[s], Pi[s] = update(gamma,V,s,util)
            delta = max(delta, math.fabs(value - V[s]))
        if i == 500:
            break
    # np.savetxt("Pi_sum.list",Pi,fmt="%d")
    return V,W


if __name__ == '__main__':
    V,S,Pi = init()
    W=[1,1,1,1]

#这几个文件的格式和titlefinalMatrix等是一样的
    contentlist = sumReward(np.loadtxt('ListB_abstract.txt'))  # abstract
    proclist = sumReward(np.loadtxt('ref_value.file'))  # reference
    titlelist = sumReward(np.loadtxt('ListB_title.txt'))  # title
    keywordlist = sumReward(np.loadtxt('keyw_value.file'))  # keyword


    inputList = [contentlist,proclist,titlelist, keywordlist]

    print "haha"




    (V, W) = main_iteration(V, S, Pi, W, inputList)
    print W
    # W=[0.49084937  0.98613076  0.9109054   0.96451163]
    (V, W) = main_iteration(V, S, Pi, W, inputList)
    print W
    with open('V.txt', 'w') as file:
        for i in v:
            file.writer(str(i) + '\n')




