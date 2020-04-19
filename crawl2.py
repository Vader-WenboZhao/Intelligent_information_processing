import time
import requests
import json
import random
import re
from bs4 import BeautifulSoup
import pandas as pd
from face_score import face_score

#定义豆瓣的索引页的headers，cookies以模拟浏览器，从而不会出现403Forbidden
headers_index = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36'}
cookies_index= {'cookies':'bid=UusQw4pyBc4; ll="118220";'
                                                   ' __yadk_uid=1dCQeaOd50cFklfk5qMLRqge0ZNbW4oq;'
                                                   ' _vwo_uuid_v2=D6421FBE1439F2AC795A251BEF9B6B73F|37cfcfe50ba563d5e181b50d24da9efd; '
                                                   'trc_cookie_storage=taboola%2520global%253Auser-id%3Df0cff8aa-6fa7-4a30-b204-5c37abeee3e4-tuct49600d5;'
                                                   ' gr_user_id=b65236fe-bc14-481a-9af0-082b5ed4b724;'' viewed="2170253_30359816_30253818_30239493_27596650_30347055_30263007"; __gads=Test; '
                                                   '_ga=GA1.2.1335124964.1570881276; __utmc=30149280; __utmc=223695111; _gid=GA1.2.1470771987.1572080187; '
                                                   '__utmz=30149280.1572080200.6.5.utmcsr=m.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/home_guide; '
                                                   '__utmz=223695111.1572080201.7.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.'
                                                   '4cf6=%5B%22%22%2C%22%22%2C1572138952%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; '
                                                   '_pk_id.100001.4cf6=f3b928208e5e38ef.1570881180.8.1572138952.1572099244.; _pk_ses.100001.4cf6=*; ap_v=0,6.0;'
                                                   ' __utma=30149280.1335124964.1570881276.1572096386.1572138953.8; __utmb=30149280.0.10.1572138953;'
                                                   ' __utma=223695111.84077698.1570881180.1572096386.1572138953.9; __utmb=223695111.0.10.1572138953'}

#定义详情页headers
headers_detail = {'User-Agent':'Mozilla/5.0 '}
# cookies_analysis = {'cookies':''}

#获取索引页的http响应
def get_index_page(html):
    try:
        response = requests.get(url=html,headers=headers_index,cookies=cookies_index)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.json() #转为字典（json）类型，仅有一个键值对,key为'data'，value为 [{},{},{}]  （列表里是字典）
        return None
    except requests.exceptions.RequestException:
        print('获取索引页出错')
        time.sleep(3)
        return get_index_page(html)

# 解析索引页面，获取详情页url返回列表 (直接调用了get_index_page返回响应并进行处理)
def analysis_index_page(html):
    id_list = []  #用于存放 url
    r = get_index_page(html)  #接收返回的字典
    # print(r)
    for i in r['data']:   #对r的值（为列表）里每个字典
        id_list.append(i['url'])
    return id_list

#获取电影详情页http响应
def get_detail_page(html):
    try:
        response = requests.get(url=html, headers=headers_detail)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except requests.exceptions.RequestException:
        print('获取详情页出错')
        time.sleep(3)
        return get_detail_page(html)

#解析response文本，传入的参数为text
list_all=[] #用于存放总的所有电影信息
def analysis_detail_page(text):
    list = []  #存放电影信息
    # soup = BeautifulSoup(text, 'html.parser')

    #电影名称
    name_pattern = re.compile('<span property="v:itemreviewed">(.*?)</span>')
    # name_pattern example: re.compile('<span property="v:itemreviewed">(.*?)</span>')
    name = re.findall(name_pattern, text)
    # name example: ['国际市场 국제시장']
    list.append(name[0].split(' ')[0])
    print(name[0].split(' ')[0])

    #电影导演(有的电影导演有多个，为列表)
    director_pattern = re.compile('rel="v:directedBy">(.*?)</a>')
    # director_pattern example: re.compile('rel="v:directedBy">(.*?)</a>')
    director = re.findall(director_pattern,text)
    # dorector example: ['长峰达也']
    list.append(director[0])

    # 获取演员(也有多个，为列表)
    actor_pattern = re.compile('rel="v:starring">(.*?)</a>')
    actor = re.findall(actor_pattern, text)
    # actor example: ['黄政民', '金允珍', '吴达洙', '张荣男', '郑镇荣', '罗美兰', '金瑟祺', '郑允浩', 'Stella Choe']
    if(len(actor)>=5):
        list.append(actor[0:5])
    else:
        list.append(actor)

    #获取电影评分
    score_pattern = re.compile('rating_num" property="v:average">(.*?)</strong>')
    score = re.findall(score_pattern, text)
    # score example: ['8.4']
    list.append(score[0])

    #获取电影年份
    year_pattern = re.compile('<span class="year">\((.*?)\)</span>')
    year = re.findall(year_pattern, text)
    # year example: ['2014']
    if (len(year) >= 3):
        list.append(year[0:3])
    else:
        list.append(year)

    # 获取类型（多个，为列表）
    type_pattern = re.compile('property="v:genre">(.*?)</span>')
    type = re.findall(type_pattern, text)
    # type example: ['动作', '动画', '奇幻', '冒险']
    list.append(type)

    #获取电影时长
    try:
        time_pattern = re.compile('property="v:runtime" content="(.*?)"')
        time = re.findall(time_pattern, text)
        # time example: ['126']
        list.append(time[0])
    except:
        list.append('1')

    # 获取电影评价人数
    comment_pattern = re.compile('property="v:votes">(.*?)</span>')
    comment = re.findall(comment_pattern, text)
    # comment example: ['44727']
    list.append(comment[0])

    # 获取语言
    language_pattern = re.compile('pl">语言:</span>(.*?)<br/>')
    language = re.findall(language_pattern, text)
    # language example:[' 韩语 / 英语 / 德语']
    a=language[0].split(' ')[1]
    list.append(a)

    # 获取地区
    area_pattern = re.compile(' class="pl">制片国家/地区:</span>(.*?)<br/>')
    area = re.findall(area_pattern, text)
    # area example:[' 韩国']
    list.append(area[0].split(' /')[0])


    # 获取演员颜值
    pic_url_set = set()
    actorpic_pattern = re.compile(r'background-image: url((.*?))"')
    actorpic = re.findall(actorpic_pattern, text)
    score = 0.0
    if len(actorpic)>3:
        actorpic = actorpic[:3]
    number = len(actorpic)
    temp_set = set()
    for i in actorpic:
        temp_set.add(i[0])
    for j in temp_set:
        pic_url_set.add(j.lstrip('(').rstrip(')'))
    for actor_pic_url in pic_url_set:
        score += face_score(actor_pic_url)
    print(score/number)
    list.append(score/number)


    list_all.append(list)


cmp_count = 0
count = 30
for i in range(5*count+1,5*(count+1)+1): # 1-160
    print("Now is ", i)
    url_index = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={num}'.format(num=i*20)
    # r =get_index_page(url_index)
    # print(url_index)

    try:
        id_list = analysis_index_page(url_index)
        print(id_list)
        for k in id_list:  #对每个url
            text = get_detail_page(k)
            analysis_detail_page(text)
        time.sleep(3+random.random())
    except Exception:
        continue

column=['名称','导演','演员','评分','年份','类型','电影时长','评价人数','语言','地区','演员颜值']
test=pd.DataFrame(columns=column,data=list_all)
test.to_csv('/Users/zhaowenbo/Downloads/crawl_ouban/test_new_' + str(count) + '.csv')
cmp_count = count
