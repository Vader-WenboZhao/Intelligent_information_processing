import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import types
import string
import jieba
from math import isnan
import os
import sys
import time

def pretreatment_1():

    # 如果用pandas打不开数据，可以使用记事本打开把编码格式改成utf-8另存
    data = pd.read_csv('/Users/zhaowenbo/Downloads/crawl_ouban/test.csv', encoding='GBK')


    # 将'地区'因素量化并归一化
    # 地区字典
    region_dict = {}
    count = 0
    for i in data['地区']:
        if i in region_dict.keys():
            region_dict[i] += 1
        else:
            region_dict[i] = count
            count += 1

    # 按电影数量排序, 电影数量一定程度上反映了该地区电影受影迷欢迎的程度
    sorted_region_list = sorted(zip(region_dict.values(), region_dict.keys()))
    print(type(sorted_region_list))

    new_sorted_region_list = []
    original_len = len(sorted_region_list)

    max = 0
    for i in range(original_len):
        new_sorted_region_list.append((sorted_region_list[i][1], i))
        max = i+1
    print(max)

    new_region_dict = dict(new_sorted_region_list)
    print(new_region_dict)

    # 写回文件
    numHu = data['地区'].shape[0]
    for i in range(0, numHu):
        # 归一化
        data['地区'][i] = float(new_region_dict[data['地区'][i]])/float(max)
        if(i%100 == 0):
            print(i)



    # 将'语言'因素量化并归一化
    language_dict = {}
    count = 0
    for i in data['语言']:
        if i in language_dict.keys():
            language_dict[i] += 1
        else:
            language_dict[i] = count
            count += 1

    # 按电影数量排序, 电影数量一定程度上反映了该语种电影受影迷欢迎的程度
    sorted_language_list = sorted(zip(language_dict.values(), language_dict.keys()))
    print(type(sorted_language_list))

    new_sorted_language_list = []
    original_len = len(sorted_language_list)

    max = 0
    for i in range(original_len):
        new_sorted_language_list.append((sorted_language_list[i][1], i))
        max = i+1
    print(max)

    new_language_dict = dict(new_sorted_language_list)
    print(new_language_dict)

    # 写回文件
    numHu = data['语言'].shape[0]
    for i in range(0, numHu):
        # 归一化
        data['语言'][i] = float(new_language_dict[data['语言'][i]])/float(max)
        if(i%100 == 0):
            print(i)



    # 将'年份'量化并归一化
    data['年份'] = data['年份'].str.extract(r'\'(.+?)\'')
    data['年份'] = data['年份'].astype(float)
    min = data['年份'].min()
    max = data['年份'].max()
    print(min, max)
    for i in range(len(data['年份'])):
        # 归一化
        data['年份'][i] = float((data['年份'][i]-min))/float(max-min)
        if(i%100 == 0):
            print(i)

    # 将电影时长归一化
    data['电影时长'] = data['电影时长'].astype(float)
    min = data['电影时长'].min()
    max = data['电影时长'].max()
    print(min, max)
    for i in range(len(data['电影时长'])):
        data['电影时长'][i] = float((data['电影时长'][i]-min))/float(max-min)
        if(i%100 == 0):
            print(i)

    # 将评价人数归一化
    data['评价人数'] = data['评价人数'].astype(float)
    min = data['评价人数'].min()
    max = data['评价人数'].max()
    print(min, max)
    for i in range(len(data['评价人数'])):
        data['评价人数'][i] = float((data['评价人数'][i]-min))/float(max-min)
        if(i%100 == 0):
            print(i)



    # 将评分归一化
    data['评分'] = data['评分'].astype(float)
    min = data['评分'].min()
    max = data['评分'].max()
    print(min, max)
    for i in range(len(data['评分'])):
        data['评分'][i] = float((data['评分'][i]-min))/float(max-min)
        if(i%100 == 0):
            print(i)


    return data

data = pretreatment_1()
data.to_csv('/Users/zhaowenbo/Downloads/crawl_ouban/test_2.csv', sep=',', index=False, header=True)
