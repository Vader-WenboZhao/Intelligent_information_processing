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
from tools import *


# 如果用pandas打不开数据，可以使用记事本打开把编码格式改成utf-8另存
data = pd.read_csv('/Users/zhaowenbo/Downloads/crawl_ouban/test.csv', encoding='GBK')


data['年份'] = data['年份'].str.extract(r'\'(.+?)\'')
data['年份'] = data['年份'].astype(float)
result = {}
count = 0
print(len(data['年份']))
for i in range(1925, 2020):
    for j in range(len(data['年份'])):
        if data['年份'][j] == i:
            if i not in result.keys():
                result[i] = 0
                result[i] += data['评分'][j]
                count += 1
            else:
                result[i] += data['评分'][j]
                count += 1
    if count != 0:
        result[i] /= float(count)
    count = 0

print(result)
#draw_bar(result.keys(), result.values())
broken_line_chart(result.keys(), result.values(), "year", "score")



data['评价人数'] = data['评价人数'].astype(int)
min = data['评价人数'].min()
max = data['评价人数'].max()
result = {}
count = 0
print(len(data['评价人数']))
for i in range(int(min/10), int(max/10)):
    for j in range(len(data['评价人数'])):
        if data['评价人数'][j]/10 == i:
            if i not in result.keys():
                result[i] = 0
                result[i] += data['评分'][j]
                count += 1
            else:
                result[i] += data['评分'][j]
                count += 1
    if count != 0:
        result[i] = float(result[i])/float(count)
    count = 0
    print(i)

print(result)
#draw_bar(result.keys(), result.values())
broken_line_chart(result.keys(), result.values(), "s", "score")
