import jieba
from os import listdir
import re
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import plugins
import math
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率
def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret
def gcj02towgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat
def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:经度
    :param lat:维度
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False
def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return(vTEXT)
def doc(path,*partic_path):
    '''
    
    :param path:字符串，要求处理的文件路径 
    :param partic_path:字符串，存储分类标签的文件或文件夹，
    :return: 返回两个结构，先返回dataframe结构的data，储存经过处理的原文档，后返回字典：mood，存储情绪字典
    '''
    sentence=list()
    mood=dict()
    for i in partic_path:# 读入partic_path的情绪字典
        if i[-3:]=='txt':
            jieba.load_userdict(i)
            with open(i,encoding="UTF-8") as f:
                f=f.read().split('\n')
                mood[i.split("\\")[-1][:-4]]=f
        else:
            for j in listdir(i):
                j=i+"\\"+j
                jieba.load_userdict(j)
                with open(j,encoding="UTF-8") as f:
                    f=f.read().split('\n')
                    mood[j.split("\\")[-1][:-4]]=f
    columns=["text","long","lati","time"]
    with open(path,encoding="UTF-8") as f:# 读入微博原始数据
        f=f.read().split('\n')
        for i in f:
            sentence.append(remove_urls(i).split("\t"))
    sentence.pop(-1)
    data=pd.DataFrame(data=sentence,columns=columns)# 将数据转化为dataframe
    data = data.astype({"lati":'float','long':'float'})# 将地址转化为小数
    data [["long","lati"]] =list(data.apply(lambda x: gcj02towgs84(x['long'],x["lati"]), axis=1)) # 将地址转化
    data['time'] = pd.to_datetime(data['time']) # 时间格式转化为datatime格式
    return(data,mood)
def flite(data,split_path):
    """
    
    :param data:dataframe结构，由doc函数产生；
    :param split_path: 字符串，分词字典
    """
    flited=[]
    with open(split_path,encoding="UTF-8") as f:
            f=f.read().split('\n')
            flited=list(list(list(filter(lambda y:y not in f,jieba.lcut(x))) for x in data["text"]))
    data["flited_text"]=flited
def emotion(mood):
    """
    
    :param mood:字典，情绪字典
    :return: 闭包，返回内函数
    """
    def vens(flited):
        """

        :param flited:列表，存储分词后的文本
        :return: 字符串：文本的情绪或"None"
        """
        nonlocal mood
        result={}
        key=mood.keys()
        for k in key:
            v= sum(list(1 if x in mood[k] else 0 for x in flited))
            result[k]=v
        if sum(result.values())!=0:
            max_value=max(result.values())
            max_list=[]
            for m, n in result.items():       # 遍历字典一遍找对应的 key 值
                if n == max_value:
                    max_list.append(m)
            return " and ".join(max_list)
        else:
            return "None"
    return vens
def turn(a):#求列表中个各元素占比
    b=sum(a)
    return [x/b for x in a]
def time_stat_hour(data,moods):
    """
    
    :param data:dataframe结构，由doc函数产生；
    :param moods: 列表，情绪类型
    :return: dataframe结构，各时间段各个情绪的出现频次，列名为情绪
    """
    data['time_hour'] = data["time"].apply(lambda x: x.hour)
    hours=range(24)
    stat=pd.DataFrame(columns=["hour"]+moods)
    for i in range(24):
        score=[]
        score.append(i)
        for j in moods:
            score.append(data[(data["time_hour"]==i) & data["emotion"].str.contains(j)].count()[2])
        stat.loc[i]=score
    stat.plot(x="hour",title='Frequency of each emotion',xticks=range(24))
    a=list(stat.apply(lambda x: turn(list(x[1:])), axis=1)) # 将地址转化
    tt=pd.DataFrame(data=a,columns=list(moods))
    tt.plot(title='Frequency of each emotion ',xticks=range(24))
    plt.show()
    return stat
def space_stat(data,path,time_begin=0,time_end=23,moods=['anger', 'disgust', 'fear', 'joy', 'sadness'],*colors):
    '''
    
    :param data:dataframe结构，由doc函数产生；
    :param path:字符串，存储图片的路径；
    :param time_begin:int 开始时间段，默认值为0点；
    :param time_end:int 结束时间段，默认值为23点；
    '''
    weibo_map = folium.Map(location=[data['lati'].mean(), data['long'].mean()], zoom_start=10)
    marker_cluster =folium.plugins.MarkerCluster().add_to(weibo_map)
    colors=list(*colors)
    colors_use=[i for i in colors]
    colors_back=["red","blue","black","green","orange"]
    if len(colors)<len(moods):
        colors_use.extend(colors_back[i] for i in range(len(moods)-len(colors))  if colors_back[i] not in colors)
    for name,row in data[(data["time_hour"]>=time_begin) & (data["time_hour"]<=time_end) ].iterrows():
        for j in row["emotion"].split(" and "):
            if j in moods:
                folium.Marker([row["lati"], row["long"]], popup="{0}:{1}".format(row["emotion"], name),icon=folium.Icon(color=colors_use[moods.index(j)],icon='info-sign')).add_to(marker_cluster) 
    #display(weibo_map)
    weibo_map.save(path)
def main():
    data,mood=doc("D:\大学资料\大三上资料\现代程序设计\数据\weibo.txt","D:\大学资料\大三上资料\现代程序设计\数据\Anger makes fake news viral online-data&code\data\emotion_lexicon")
    print(data.head(5))
    print(mood.keys())
    flite(data,"D:\大学资料\大三上资料\现代程序设计\数据\stopwords_list.txt")
    print(data.head(5))
    k=emotion(mood)
    vens=[]
    for i in data["flited_text"]:
        vens.append(k(i))
    data["emotion"]=vens
    stat=time_stat_hour(data,list(mood.keys()))
    path='D:\大学资料\大三上资料\现代程序设计\map.html'
    space_stat(data,path,5,7)
if __name__== '__main__':
    main()
