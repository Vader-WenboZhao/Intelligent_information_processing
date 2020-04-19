import pandas as pd                         #导入pandas包

def deal_data():

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

    #数据处理

    #导演
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[0][1] != '' and float(list[0][2])>=2):
        n=0
        for n in range(length): #对每个电影遍历
            if(data.loc[n,'导演'] ==list[0][1]):
                data.loc[n,'导演']=1
            else:
                data.loc[n, '导演']=0
    else:
        data=data.drop(columns='导演')

    #演员
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[1][1] != '' and float(list[1][2])>=2):
        n=0
        for n in range(length): #对每个电影遍历
            l=data.loc[n, '演员'].lstrip('[\' ').rstrip(' \'] ').split("', '")
            if(list[1][1] in l):
                rank = l.index(list[1][1])
                #根据演员位置给予不同的等级评分(线性函数)
                data.loc[n,'演员']=1-rank/len(l)
            else:
                #不在其中则直接为0
                data.loc[n, '演员']=0
    else:
        data=data.drop(columns='演员')

    #评分
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[2][1] != '' and float(list[2][2])>=2):
        n=0
        range1 = data.loc[:, '评分'].max() -data.loc[:, '评分'].min() #评分范围
        for n in range(length): #对每个电影遍历
            data.loc[n, '评分']=1 - abs(data.loc[n,'评分']-float(list[2][1]))/range1
    else:
        data=data.drop(columns='评分')

    #年份
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[3][1] != '' and float(list[3][2])>=2):
        n=0
        max=0
        min=10000
        for n in range(length):  # 对每个电影遍历
            now = int(data.loc[n, '年份'].lstrip("['").rstrip("']"))
            if(now>max):
                max=now
            if(now<min):
                min=now
        range1=max-min #计算年份最大范围
        n=0
        for n in range(length): #对每个电影遍历
            w=int(data.loc[n, '年份'].lstrip("['").rstrip("']"))
            data.loc[n, '年份']=1 - abs(w-int(list[3][1]))/range1
    else:
        data=data.drop(columns='年份')


    #类型
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[4][1] != '' and float(list[4][2])>=2):
        n=0
        for n in range(length): #对每个电影遍历
            l=data.loc[n, '类型'].lstrip('[\' ').rstrip(' \'] ').split("', '")
            if(list[4][1] in l):
                rank = l.index(list[4][1])
                #根据类型位置给予不同的等级评分(线性函数)
                data.loc[n,'类型']=1-rank/len(l)
            else:
                #不在其中则直接为0
                data.loc[n, '类型']=0
    else:
        data=data.drop(columns='类型')

    #电影时长
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[5][1] != '' and float(list[5][2])>=2):
        n=0
        range1 = data.loc[:, '电影时长'].max() -data.loc[:, '电影时长'].min() #电影时长范围
        for n in range(length): #对每个电影遍历
            data.loc[n, '电影时长']=1 - abs(float(data.loc[n,'电影时长'])-float(list[5][1]))/range1
    else:
        data=data.drop(columns='电影时长')


    #评价人数
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[6][1] != '' and float(list[6][2])>=2):
        n=0
        range1 = data.loc[:, '评价人数'].max() -data.loc[:, '评价人数'].min() #评价人数范围
        for n in range(length): #对每个电影遍历
            data.loc[n, '评价人数']=1 - abs(float(data.loc[n,'评价人数'])-float(list[6][1]))/range1
    else:
        data=data.drop(columns='评价人数')


    #语言
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[7][1] != '' and float(list[7][2])>=2):
        n=0
        for n in range(length): #对每个电影遍历
            if(data.loc[n,'语言'] ==list[7][1]):
                data.loc[n,'语言']=1
            else:
                data.loc[n, '语言']=0
    else:
        data=data.drop(columns='语言')


    #地区
    #排除 重要性过低的属性 或 没有给出明确值的属性
    if(list[8][1] != '' and float(list[8][2])>=2):
        n=0
        for n in range(length): #对每个电影遍历
            if(data.loc[n,'地区'] ==list[0][1]):
                data.loc[n,'地区']=1
            else:
                data.loc[n, '地区']=0
    else:
        data=data.drop(columns='地区')


    cnum=data.shape[1] #列数
    rnum=data.shape[0]-1 #行的最后一个索引
    newrows=[1] * cnum
    newrows[-1]='X'
    data.loc[rnum+1] = newrows #添加新的电影（用户电影X）

    weight=[] #记录权重
    for i in list:
       weight.append(i[2])

    return data,weight

print(deal_data()[0])
print(deal_data()[1])
