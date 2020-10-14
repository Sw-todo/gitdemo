import jieba
from math import log
import numpy as np
from functools import reduce
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from wordcloud import WordCloud
import matplotlib.pyplot  as plt
from sklearn.cluster import KMeans
from itertools import cycle
from sklearn.decomposition import PCA
def partic_ch(ch):
    '''

    :param ch: 字符串，句子
    :return: 列表，存储分词后的东西，仅适用于中文
    '''
    return jieba.lcut(ch)
def partic_en(en):
    '''

    :param en: 字符串，句子
    :return: 列表，存储分词后的东西，仅适用于英文
    '''
    en=en.split(' ')

    if en==['']:
        return en
    if en[0][0]=='@':
        en.pop(0)
    if en[0]=='RT':
        del(en[0:2])
    en=list(t[1:] if len(t)>1 and t[0]=='$' else t for t in en )
    en=list(filter(lambda t:((len(t)>5 and t[0:5]=='https') )==False,en))
    return en
def doc(path,classfication):
    '''

    :param path: 字符串，文本存储地点
    :param classfication: 字符串，语言类别：chinese or english
    :return: 二维列表，存储分词后的句子
    '''
    sentence=list()
    with open(path,encoding="UTF-8") as f:
        f=f.read().split('\n')
        if classfication=='chinese':
            for i in f:
                sentence.append(partic_ch(i))
        else:
            for i in f:
                sentence.append(partic_en(i))
    return(sentence)
def filte(words,split_path):
    '''

    :param words: 二维列表，存储分词后的句子
    :param split_path: 停用词表路径
    :return: 二维列表，存储停用词过滤后的句子
    '''
    assistant=[]
    with open(split_path,encoding="UTF-8") as f:
        f=f.read().split('\n')
        assistant=list(map(lambda x:list(filter(lambda y:y not in f,x)),words))
    return assistant
def static(words):
    '''

    :param words:二维列表，存储过滤停用词后的句子
    :return:字典，key为词汇，value为词频
    '''

    List =sum(words,[])
    arr = np.array(List)
    key = np.unique(arr)
    result = {}
    for k in key:
        mask = (arr == k)
        pos = arr[mask]
        v = pos.size
        result[k] = v
    return result
def focus(dic):
    '''

    :param dic: 字典
    :return:
    '''
    cores=list(filter(lambda x:dic[x]>250,dic.keys()))
    return cores
def vector(stat,filted):
    '''

    :param stat: 字典，存储各词语出现频次
    :param filted:列表，存储过滤后句子
    :return:字典：各词语的TF-IDF值，即代表性程度
    '''
    result={}
    tot=sum(stat.values())
    for word in stat.keys():
        tf=stat[word]/tot
        num=sum(1 for sentence in filted if word in sentence)
        idf=log(len(filted) / (1 + num))
        tfidf=tf*idf
        result[word]=tfidf
    return result
def mapping(filted,ven0,ven):
    '''

    :param filted: 二位列表，存储过滤后的句子
    :param ven0: 字典，存储各词语的代表性
    :param ven: 列表，存储特征向量
    :return: 二维列表，各句子的向量投影
    '''
    result=[]
    for sentences in filted:
        t=[ven0[i]  if i in sentences else 0 for i in ven]
        result.append(t)
    return result
def pre(vens,words,classfication):
    '''

    :param vens: 二位列表：句子向量
    :param words: 二维列表：存储分词后的句子
    :param classfication:字符串：文档类型
    :return: 列表：最具有代表性的句子：以各句子的再各个维度的分量求平方和，即求其向量模的平方以代表该剧自的代表性
    '''
    score=[reduce(lambda z, y: z+y, (map(lambda t: t** 2,x))) for x in vens]
    if str.lower(classfication)=='english':
        print(" ".join(words[score.index(max(score))]))
    else :
        print("".join(words[score.index(max(score))]))
    return words[score.index(max(score))]
def distance(vens):
    '''

    :param vens: 二维列表，句子向量
    :return: 二位列表，距离矩阵
    '''
    distA = pdist(vens, metric='euclidean')
    distB = squareform(distA)
    return distB
def draw_cloud(cores):
    '''

    :param cores: 字典，各词语的词频
    :return: none
    '''
    wc=WordCloud(
        max_words = 200,  # 最多显示词数
        background_color = "white",# 设置背景为白色，默认为黑色
        #max_font_size=100,  # 字体最大值
        font_path='AdobeKaitiStd-Regular.otf',
        width = 1500,  # 设置图片的宽度
        height = 1500,  # 设置图片的高度
        margin = 10  # 设置图片的边缘
    )
    wc.generate_from_frequencies(cores)
    plt.subplot(1,2,1)
    plt.imshow(wc)
    plt.axis('off')  # 关闭坐标轴
    #wc.to_file(fp)  # 保存图片
def cluster(vens,n_clusters=3):
    '''

    :param vens: 二位列表，向量
    :param n_clusters: int，分类个数
    :return: none
    '''
    pca = PCA(n_components=2)
    new_pca = pca.fit_transform(vens)
    row = []
    col = []
    for i in range(len(new_pca)):
        row.append(new_pca[i][0])
        col.append(new_pca[i][1])
    km = KMeans( n_clusters=n_clusters, n_init=10 ,init='k-means++',max_iter=500)
    km.fit(vens)
    mdl= km.labels_
    label_pred = km.labels_
    centroids = km.cluster_centers_
    inertia = km.inertia_
    plt.subplot(1,2,2)
    plt.scatter(row,col,c=label_pred)

def main(path,classfication,path2):
    '''

    :param path: 字符串，文本分析的文件路径
    :param classfication: 字符串，文字类别，english or chinese
    :param path2: 字符串，停用词表路径
    :return:none
    '''

    words=doc(path,classfication)
    filted=filte(words,path2)
    stat=static(filted)#统计词语出现频率
    cores=focus(stat)#统计高频词
    print(cores)
    ven0=vector(stat,filted)#IF-IDF统计分量代表性，形式为字典
    for i in ven0.items():
        print(i)
    sorted_re = sorted(ven0.items(), key=lambda x: x[1], reverse=True)
    ven=[word[0] for word in sorted_re[:10]]#找到特征向量
    print(ven)
    vens=mapping(filted,ven0,ven)#句子投影
    for i in vens:
        print(i)
    pre(vens, words, classfication)
    dist=distance(vens)#距离
    print(dist)
    draw_cloud(stat)
    cluster(vens,n_clusters=10)
    plt.show()
if __name__ =="__main__":
    path=input()
    classfication=input()
    path2=input()
    #classfication ='chinese'
    #path=r'D:\大学资料\大三上资料\现代程序设计\数据\online_reviews_texts.txt'
    #path2=r'D:\大学资料\大三上资料\现代程序设计\数据\stopwords_list.txt'
    main(path=path,classfication=classfication,path2=path2)
