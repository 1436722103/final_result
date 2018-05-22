
import numpy as np
def recommend(select,similarity):
    n,m=select.shape
    terminal=False
    recomed_index=[0]*n
    while not terminal:
        terminal=True
        al_recom=[-1]*n
        for i in range(n):
            recomed=int(select[i][recomed_index[i]])
            if al_recom[recomed]==-1:
                al_recom[recomed]=i
            else:
                terminal=False
                pri_recomed=al_recom[recomed]
                if similarity[pri_recomed][recomed]>similarity[i][recomed]:
                    recomed_index[i]+=1
                    # if recomed_index[i]>9:
                    #     recomed_index[i]=9
                    #     similarity[i][recomed_index[i]]=2.0
                else:
                    recomed_index[pri_recomed]+=1
                    al_recom[recomed]=i
                    # if recomed_index[pri_recomed]>9:
                    #     recomed_index[pri_recomed]=9
                    #     similarity[pri_recomed][recomed_index[pri_recomed]]=2.0
    recom_list=[select[j][recomed_index[j]] for j in range(n)]
    return recom_list
if __name__=='__main__':
    fa=np.loadtxt('actionList.file')#第一步获得的推荐列表
    lb=np.loadtxt('envSim.txt')#environment similarity
    re=recommend(fa,lb)
    print(re)
