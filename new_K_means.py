import pandas as pd                         #导入pandas包
import numpy as np
import random
from statistics import score_range
from statistics import year_range
from statistics import time_range
from statistics import people_range
#计算两个list的杰卡德系数
def jaccard(x,y):
    x=set(x)
    y=set(y)
    a=x&y
    b=x|y
    return len(a)+1/len(b)

def findcenter(dataset,weight):
    a,b=dataset.shape
    min=999999
    index=-1
    for i in range(a):
        sum=0
        for j in range(a):
            d=distance(dataset[i],dataset[j],weight)
            sum=sum+d
        if sum<min:
            index =i
            min=sum
    return index


# 计算两数据之间距离
def distance(x,y,weight):
    l=len(x)
    sum=0
    for i in range(l):
        if i==0: #导演
            if x[i]!=y[i]:  #导演不相同，距离加1 * weight
                sum=sum + weight[i] * 1
        if i==1: #演员
            a=x[i].lstrip('[\' ').rstrip(' \'] ').split("', '")
            b=y[i].lstrip('[\' ').rstrip(' \'] ').split("', '")
            j=jaccard(a,b)
            sum=sum + weight[i] * j
        if i==2: #评分
            a=float(x[i])
            b=float(y[i])
            sum=sum + weight[i] * abs(a-b)/score_range
        if i==3: #年份
            a=int(x[i].lstrip("['").rstrip("']"))
            b=int(y[i].lstrip("['").rstrip("']"))
            if x[i]!=y[i]:
                sum=sum + weight[i] * abs(b-a)/year_range
        if i==4: #类型
            a = x[i].lstrip('[\' ').rstrip(' \'] ').split("', '")
            b = y[i].lstrip('[\' ').rstrip(' \'] ').split("', '")
            j = jaccard(a, b)
            sum = sum + weight[i] * j
        if i==5: #电影时长
            a = float(x[i])
            b = float(y[i])
            sum = sum + weight[i] * abs(a - b) / time_range
        if i==6: #评价人数
            a = float(x[i])
            b = float(y[i])
            sum = sum + weight[i] * abs(a - b) / people_range
        if i==7: #语言
            if x[i]!=y[i]:
                sum=sum + weight[i] * 1
        if i==8: #地区
            if x[i]!=y[i]:
                sum=sum + weight[i] * 1
    return sum

#随机选取k个中心点
def randCent(dataset,k):
    a,b=dataset.shape
    center = np.array([['a',[1],1,1,1,1,1,1,1]])
    num=0
    list=[]
    while num<k:
        w=random.randint(0,a-1) #选中的中心编号
        if w in list: continue   #防止重复
        list.append(w)
        center=np.insert(center,0,dataset[w,:],axis=0)
        num=num+1
    print("选中的中心编号:")
    print(list)
    return center[:-1]


# k-means
def k_means(dataset,k,w):
    a,b=dataset.shape #a行，b列

    cluster=np.zeros((a,2)) #第一列表示所属类别（所属中心点）的索引，第二列为该点与所属中心点相差距离
    b=0  #表示中心是否被更新
    center=randCent(dataset,k) #随机产生k个中心
    while b<= 3 :
        b=b+1
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

        # 更新中心点，如果有改变则改b为True
        for j in range(k):
            gather = dataset[np.nonzero(cluster[:, 0] == j)[0]]  # 属于同一类别（同一中心点）的点 的集合
            if (len(gather) == 0):
                print(k, '个中心点时发生退化')
                continue
            newindex = findcenter(gather,weight)
            new =gather[newindex]
            center[j, :] = new[:]

    print("Finish")
    return center,cluster

# data = pd.read_csv("test.csv",encoding='GBK')
data = pd.read_csv("/Users/zhaowenbo/Downloads/crawl_ouban/test.csv",encoding='GBK')
length=len(data) #电影个数

data = data.drop(columns='Unnamed: 0')  # 去掉无用索引列
#调整列的顺序，便于后面的K-means
order=['导演','演员','评分','年份','类型','电影时长','评价人数','语言','地区','名称']
data=data[order]



list=[]
for line in open("/Users/zhaowenbo/Downloads/crawl_ouban/user_info.txt",encoding="utf-8"):
    if(line[0]=='('):
        break
    print(line)
    l=line.strip('\n').split(',')
    list.append(l)



weight=[] #记录权重
for i in list:
   weight.append(i[2])
#str转为float
for i in range(len(weight)):
    weight[i]=float(weight[i])
#权重归一化
all=sum(weight)
for i in range(len(weight)):
    weight[i]=weight[i]/all

dataset_pre=data.values
dataset=dataset_pre[:,:-1]

k=15 #聚类簇数
a,b=k_means(dataset,k,weight)

list1=[]
c = [ '导演', '演员', '评分', '年份', '类型', '电影时长', '评价人数', '语言', '地区','名称']

for j in range(k):
    gather = dataset_pre[np.nonzero(b[:, 0] == j)[0]]  # 属于同一类别（同一中心点）的点 的集合
    for i in gather:
        list1.append(i)
    list1.append([ '导演', '演员', '评分', '年份', '类型', '电影时长', '评价人数', '语言', '地区','名称'])

test = pd.DataFrame(columns=c, data=list1)
test.to_csv('/Users/zhaowenbo/Downloads/crawl_ouban/result_1.csv')
