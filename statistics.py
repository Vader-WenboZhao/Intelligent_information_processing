import pandas as pd                         #导入pandas包

# /Users/zhaowenbo/Downloads/crawl_ouban/test.csv
# data = pd.read_csv("test.csv",encoding='GBK')
data = pd.read_csv("/Users/zhaowenbo/Downloads/crawl_ouban/test.csv",encoding='GBK')
length=len(data) #电影个数

data = data.drop(columns='Unnamed: 0')  # 去掉无用索引列
#调整列的顺序，便于后面的K-means
order=['导演','演员','评分','年份','类型','电影时长','评价人数','语言','地区','名称']
data=data[order]

b=data.loc[:, '评分'].max()
a=data.loc[:, '评分'].min()
score_range=b-a
print('评分范围是:',a,b)

max=0
min=10000
for n in range(length):  # 对每个电影遍历
    now = int(data.loc[n, '年份'].lstrip("['").rstrip("']"))
    if(now>max):
        max=now
    if(now<min):
        min=now
year_range=max-min
print('年份范围是:',min,max)

list=[]
for n in range(length): #对每个电影遍历
    l = data.loc[n, '类型'].lstrip('[\' ').rstrip(' \'] ').split("', '")
    for i in l:
        if i not in list:
            list.append(i)
print('类型取值范围是:',list)

b=data.loc[:, '电影时长'].max()
a=data.loc[:, '电影时长'].min()
time_range=b-a
print('电影时长范围是:',a,b)

b=data.loc[:, '评价人数'].max()
a=data.loc[:, '评价人数'].min()
people_range=b-a
print('评价人数范围是:',a,b)

list=[]
for n in range(length): #对每个电影遍历
    l = data.loc[n, '语言']
    if l not in list:
        list.append(l)
print('语言取值范围是:',list)

list=[]
for n in range(length): #对每个电影遍历
    l = data.loc[n, '地区']
    if l not in list:
        list.append(l)
print('地区取值范围是:',list)
