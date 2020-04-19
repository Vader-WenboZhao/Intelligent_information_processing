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
data = pd.read_csv('/Users/zhaowenbo/Downloads/crawl_ouban/newtest.csv', encoding='utf-8')

#约为整数
data['演员颜值'] = data['演员颜值'].astype(int)

result = {}
count = 0

print(len(data['演员颜值']))
for i in range(data['演员颜值'].min(), data['演员颜值'].max()):
    for j in range(len(data['演员颜值'])):
        if data['演员颜值'][j] == i:
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
    print(i)

print(result)
#draw_bar(result.keys(), result.values())
broken_line_chart(result.keys(), result.values(), "face_value", "score")
