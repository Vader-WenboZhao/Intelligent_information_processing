import numpy as np
import random
from deal_data import deal_data
import pandas as pd
import matplotlib.pyplot as plt


# 计算欧氏距离
def distance(x,y,weight):
    l=len(x)
    sum=0
    for i in range(l):
        sum=sum + float(weight[i])*(float(x[i])-float(y[i]))**2
    return sum ** 0.5

#随机选取k个中心点
def randCent(dataset,k):
    a,b=dataset.shape
    center = np.zeros((k, b))
    num=0
    list=[]
    while num<k:
        w=random.randint(0,a-1) #选中的中心编号
        if w in list:
            continue   #防止重复
        list.append(w)
        center[num,:]=dataset[w,:]
        num=num+1
    print("选中的中心编号:")
    print(list)
    return center


# k-means
def k_means(dataset,k,w):
    a,b=dataset.shape #a行，b列

    cluster=np.zeros((a,2)) #第一列表示所属类别（所属中心点）的索引，第二列为该点与所属中心点相差距离
    b=True  #表示中心是否被更新
    center=randCent(dataset,k) #随机产生k个中心
    while b:
        b=False
        for i in range(a): #对每个点
            minDist=999999.0
            minIndex= -1 #索引范围是0-k-1
            for j in range(k):  #对每个中心点
                dis=distance(dataset[i,:],center[j,:],w)
                if dis <minDist: #如果距离更小
                    minDist=dis
                    minIndex=j
            #更新每个样本的所属及距离
            cluster[i,:]=minIndex,minDist

        #更新中心点，如果有改变则改b为True
        for j in range(k):
            gather =dataset[np.nonzero(cluster[:,0] == j)[0]] #属于同一类别（同一中心点）的点 的集合
            if (len(gather)==0):
                print(k,'个中心点时发生退化')
                continue
            new = np.mean(gather,axis=0) #新的中心点
            for i in range(len(new)):
                if new[i] !=center[j,i]:
                    b=True #标志中心点被更新
            center[j,:] = new[:]

    print("Finish")
    return center,cluster

def changeK(dataset,weight):
    '''
    尝试k取10-20，每个k执行8次k-means（即12次 随机选取 初始中心点）
    得到 SSE 随k的变化图，根据手肘法则判断
    '''
    avg = []
    for i in range(10,20):  # 表示中心点个数（分类数）
        sum = 0
        for j in range(8):
            center, cluster = k_means(dataset, i,weight)
            sum = sum + np.sum(cluster ** 2, axis=0)[1]
        avg.append(sum / 8)

    x_label = range(10,20)

    plt.plot(x_label, avg)
    plt.show()


data,weight = deal_data()
data = data.values #转为numpy
dataset=data[:,:-1]
#str转为float
for i in range(len(weight)):
    weight[i]=float(weight[i])
#判断是否有被舍去的属性，有则去掉
remember=[] #用于存放可用的属性的索引，从而最后用于取属性名字，便于输出
for i in range(len(weight)):
    if(weight[i]==1):
        continue
    else:
        weight.append(weight[i])
        remember.append(i)
all=sum(weight)
#权重归一化
for i in range(len(weight)):
    weight[i]=weight[i]/all


# changeK(dataset,weight)
#17

center,cluster=k_means(dataset,3,weight)

list_all=[]
#用户电影所在分类
user_class = cluster[-1,0]
for i in range(len(cluster)-1):
    if cluster[i,0]==user_class:
        list_all.append(data[i])

c = [ '导演', '演员', '评分', '年份', '类型', '电影时长', '评价人数', '语言', '地区','名称']
column=[]
for i in remember:
    column.append(c[i])
column.append(c[-1])
test = pd.DataFrame(columns=column, data=list_all)
test.to_csv('/Users/zhaowenbo/Downloads/crawl_ouban/result_2.csv')

# print(np.sum(b,axis=0)[1])
