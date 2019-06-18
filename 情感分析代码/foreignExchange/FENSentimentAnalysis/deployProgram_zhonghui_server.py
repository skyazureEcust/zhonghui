#!/usr/bin/python
#-*- coding: utf-8 -*-

import time
import re
import jieba
import jieba.posseg as pseg
from sklearn.externals import joblib
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import numpy as np
import pymysql
import ltpmanner
tag = 1
while(tag):
    try:
        db = pymysql.connect(host='118.25.147.13', user='root', port=3306, password='root@2019', db='predict_rmb')
        cursor = db.cursor()
        tag = 0
    except Exception as e:
        print(e)
        continue

def fetchModel():
    # 情感极性分析模型
    clf = joblib.load('../sentimentModel/LogisticRegressionModel.m')

    # 词向量模型
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model
    return clf, word_vec

#读取情感词
def readSentimentWords():
    # 读取情感词（正负情感词）
    sentiWord = []
    with open('../dictionary/sentimentDict/sentimentWordZF.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            sentiWord.append(each.strip())
    return sentiWord

#读取程度词
def readDegreeWords():
    # 读取高程度的程度词
    degWordH = []
    with open('../dictionary/degreeDict/HD.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degWordH.append(each.strip())

    # 读取中等程度的程度词
    degWordM = []
    with open('../dictionary/degreeDict/MD.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degWordM.append(each.strip())

    # 读取低程度的程度词
    degWordL = []
    with open('../dictionary/degreeDict/LD.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degWordL.append(each.strip())

    return degWordH, degWordM, degWordL

def terminologyWords():
    threeWeight_B = []
    highImpactList = []
    with open('../dictionary/terminologyDict/highImpactWords_B.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            highImpactList.append(each)
            threeWeight_B.append(each)

    middleImpactList = []
    with open('../dictionary/terminologyDict/middleImpactWords_B.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            middleImpactList.append(each)
            threeWeight_B.append(each)

    lowImpactList = []
    with open('../dictionary/terminologyDict/lowImpactWords_B.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            lowImpactList.append(each)
            threeWeight_B.append(each)

    return highImpactList, middleImpactList, lowImpactList

# 读取评价对象
def objectList_A():
    threeObject_A = []
    highObjectList = []
    with open('../dictionary/objectDict/highObjectdict_A.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            highObjectList.append(each)
            threeObject_A.append(each)

    middleObjectList = []
    with open('../dictionary/objectDict/middleObjectdict_A.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            middleObjectList.append(each)
            threeObject_A.append(each)

    lowObjectList = []
    with open('../dictionary/objectDict/lowObjectdict_A.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            lowObjectList.append(each)
            threeObject_A.append(each)

    # print(highobjectList)
    # print(middleobjectList)
    # print(lowobjectList)
    # return highObjectList, middleObjectList, lowObjectList, threeObject_A
    return threeObject_A

def readSpecialObject():
    specialObject = []
    with open('../dictionary/specialObject/transformObject.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for each in words:
            each = each.strip()
            specialObject.append(each)
    # print(special_word)
    return specialObject

#读取属性
def readAttribute():
    attrList = []
    with open('../dictionary/attributeDict/attributeWordsDict.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            attrList.append(each)
    return attrList

#从数据库取新闻
def fetchNews():
    idValue = 0
    newsTime = ''
    newsContent = ''
    try:
        sql = "select id, time, news from raw_news where sastatus=0 order by id limit 1"
        cursor.execute(sql)
        # msg = cursor.fetchall()
        msg = cursor.fetchall()
        if msg:
            for each in msg:
                idValue = each[0]
                newsTime = each[1]
                newsContent = each[2]
                # print('id', id)
                # print('newsTime', newsTime)
                # print('newsContent', newsContent)
    except Exception as e:
        #捕获断网情况下
        print(e)

    return idValue,newsTime, newsContent
    # else:
    #     fetchNews()

    # sql2 = "update table wallstreet_sentiment_value set sastatus=0 where time=newsTime"
    # cursor.execute(sql2)


#分割新闻
def splitNewsContent(newsContent):
    sentenceList= []
    sentence = ltpmanner.newssplitsentence(newsContent)  # 返回一条新闻内容被分割的句子列表
    for childNews in sentence:
        sentenceList.append(childNews)
    return sentenceList

def readStopWords():
    #读取停用词
    stopWord = []
    for word in open('../dictionary/stopWordsDict/stopWordsDict.txt', 'r', encoding='utf-8').readlines():
        stopWord.append(word)

    return stopWord

def jieba_pos(newsContent,stopWord):
    seg_list2 = pseg.cut(newsContent)
    # 词性标注词
    words_pseg = []
    # 给词加词性标注
    words_pos = []
    for w in seg_list2:
        if w.word not in stopWord:
            words_pseg.append(w.word)
            words_pos.append(w.flag)
    # print(newsContent)
    # print(words_pseg)
    # print(words_pos)
    return words_pseg, words_pos

#识别评价对象
def identifyObject(newsContent, threeObject_A, special_word, stopWord):
    # print('newsContent111',newsContent)
    # print(words_pseg)
    newsContent_List = []
    newsContent_List2 = []
    objectWordList = []
    objectIndexList = []
    objectDict = {}
    number = 0
    # print(threeObject_A)
    # print(len(threeObject_A))
    for each in special_word:
        if each in newsContent:
            news = newsContent.split(each)
            each = each.replace('/', '兑')
            counter = 0
            for each2 in news:
                if counter == 0:
                    newsContent = ''
                    newsContent = newsContent + each2 + each
                    counter = counter + 1
                else:
                    newsContent = newsContent + each2
    # print('newsContent222',newsContent)

    words_pseg, words_pos = jieba_pos(newsContent, stopWord)
    # print('threeObject_A',threeObject_A)
    # print('words_pseg',words_pseg)
    for each in threeObject_A:
        each = each.strip()
        if each in words_pseg:
            if each in objectWordList:
                continue
            else:
                # 找到了一个评价对象,保存到列表中
                objectWordList.append(each)
                index = words_pseg.index(each)
                objectIndexList.append(index)
                # 以字典的形式存储评价对象和对应的index
                objectDict[each] = index
                number = number + 1

    # 按values排序
    objectDict = sorted(objectDict.items(), key=lambda x: x[1])
    # print('objectDict',objectDict)
    if objectDict:
        if len(objectDict) > 1:
            each = objectDict[0]
            r = 0
            for nextEach in objectDict:
                if r == 0:
                    r = r + 1
                    continue
                # dis = nextEach[1] - each[1]
                vNumber = 0
                for k in range(each[1], nextEach[1]):
                    # print('words_pos[k]',words_pos[k])
                    if words_pos[k] == 'v':
                        vNumber = vNumber + 1
                if vNumber > 0:
                    # print('222',words_pseg)
                    # print('111',words_pseg[each[1]:nextEach[1]])
                    # print('中间段',words_pseg[each[1]:nextEach[1]])
                    newsContent_List.append(words_pseg[each[1]:nextEach[1]])
                    each = nextEach
                    if len(objectDict) - len(newsContent_List) == 1:
                        # print('finally')
                        # print('最后一段',words_pseg[each[1]:])
                        newsContent_List.append(words_pseg[each[1]:])
                else:
                    # 针对多个评价对象共用同一个谓语？？？？
                    later = words_pseg[nextEach[1]+1:]
                    # print('first_later',later)
                    for each3 in objectDict:
                        if each3[0] in later:
                            later.remove(each3[0])

                    later.insert(0,each[0])
                    # print('middle_later',later)
                    newsContent_List.append(later)
                    # 写上最后一段
                    each = nextEach
                    if len(objectDict) - len(newsContent_List) == 1:
                        # print('finally')
                        # print('最后一段',words_pseg[each[1]:])
                        newsContent_List.append(words_pseg[each[1]:])

            # 将分词的结果连成句子
            # print('newsContent_List',newsContent_List)
            if newsContent_List:
                for each in newsContent_List:
                    if each:
                        # print('each',each)
                        news = ''
                        for w in each:
                            # print('wwwww',w)
                            news = news + w
                        # print('news',news)
                        newsContent_List2.append(news)
                # print('newsContent_List2',newsContent_List2)

        elif len(objectDict) == 1:
            newsContent_List2.append(newsContent)
    else:
        newsContent_List2 = newsContent
    # print('newsContent', newsContent)
    # print('objectDict', objectDict)
    # print('newsContent_List2', newsContent_List2)

    return newsContent_List2, objectDict

#识别属性
def findAttr(news, attrList):
    attr = ''
    for attribute in attrList:
        if attribute in news:
            attr = attribute
            break
    if attr == '':
        attr = '价格'  #默认属性为价格

    return attr

# 情感极性分析
def word2vec_W(word_vec, words, sentimentWordsList):
    vec_array = np.zeros(64, dtype=float)  # 一条新闻初始化词向量，为0
    # 循环对词进行向量化
    length = len(words)
    for each in words:
        try:
            if each in sentimentWordsList:
                value = word_vec[each] * 10 / length
                vec_array += value
            else:
                value = word_vec[each] / length
                vec_array += value
        except Exception as e:
            pass
            # print("error:", e)

    # 转成list
    vec_array = vec_array.tolist()
    return [vec_array]

def getPercentage(newsContent):
    global value_0
    # 百分数形式，基点形式
    way1 = re.compile('[^\x00-\xff](\d+\.\d+)%')
    way2 = re.compile('[^\x00-\xff](\d+)%')
    way3 = re.compile('[^\x00-\xff](\d+)点')
    way4 = re.compile('[^\x00-\xff](\d+)基点')
    way5 = re.compile('[^\x00-\xff](\d+)个点')
    way6 = re.compile('[^\x00-\xff](\d+)个基点')
    way7 = re.compile('[^\x00-\xff](\d+\.\d+)点')
    way8 = re.compile('[^\x00-\xff](\d+\.\d+)基点')
    way9 = re.compile('[^\x00-\xff](\d+\.\d+)个点')
    way10 = re.compile('[^\x00-\xff](\d+\.\d+)个基点')

    res1 = way1.findall(newsContent)
    res2 = way2.findall(newsContent)
    res3 = way3.findall(newsContent)
    res4 = way4.findall(newsContent)
    res5 = way5.findall(newsContent)
    res6 = way6.findall(newsContent)
    res7 = way7.findall(newsContent)
    res8 = way8.findall(newsContent)
    res9 = way9.findall(newsContent)
    res10 = way10.findall(newsContent)

    data = value_0 #设置基值，如果新闻中没有百分数时
    if res1:
        # print('newsContent',newsContent)
        for start in res1:
            if '-' in start:
                start = str(start[0]).split('-')[0]
            # print('newsContent', newsContent)
            data = float(start) / 100
            break
    elif res2:
        # print('res2', res2)
        # quantifyValue = quantifyValue + '+' + res2[0] + '%'  #与上面同理
        for start in res2:
            data = float(start) / 100
            break
    elif res3:
        data = float(res3[0]) / 10000

    elif res4:
        data = float(res4[0]) / 10000
    elif res5:
        data = float(res5[0]) / 10000
    elif res6:
        data = float(res6[0]) / 10000
    elif res7:
        data = float(res7[0]) / 10000
    elif res8:
        data = float(res8[0]) / 10000
    elif res9:
        data = float(res9[0]) / 10000
    elif res10:
        data = float(res10[0]) / 10000

    return data

def terminologyWordsWeight(data, newsContent, highImpactList, middleImpactList, lowImpactList):
    global HEW, MEW, LEW
    flag = 0
    for ch in highImpactList:
        if ch in newsContent:
            data = data * HEW
            flag = 1
            break
    if flag == 0:
        for ch in middleImpactList:
            if ch in newsContent:
                data = data * MEW
                flag = 1
                break
    if flag == 0:
        for ch in lowImpactList:
            if ch in newsContent:
                data = data * LEW
                flag = 1
                break
    return data

def degreeWordsWeight(data, newsContent, degWordH, degWordM, degWordL):
    global HDW, MDW, LDW
    flag = 0
    for ch in degWordH:
        if ch in newsContent:
            data = data * HEW
            flag = 1
            break
    if flag == 0:
        for ch in degWordM:
            if ch in newsContent:
                data = data * MEW
                flag = 1
                break
    if flag == 0:
        for ch in degWordL:
            if ch in newsContent:
                data = data * LEW
                flag = 1
                break
    return data

def getLevel(data):
    global w1, w2, w3, w4, w5
    global value_0, value_1, value_2, value_3, value_4
    levelValue = 0
    if data <= value_1:
        levelValue = w1
    elif data <= value_2:
        levelValue = w2
    elif data <= value_3:
        levelValue = w3
    elif data <= value_4:
        levelValue = w4
    elif data > value_4:
        levelValue = w5
    return levelValue

def getObjectIntensity(newsContent, sentenceList, threeObject_A, specialObject, sentimentWordsList, highImpactList, middleImpactList, lowImpactList,degWordH, degWordM, degWordL, stopWord):
    objectIntensityDict = {}
    number = 0
    for childSentence in sentenceList:
        newsContent_List2, objectDict = identifyObject(childSentence, threeObject_A, specialObject, stopWord)
        if len(newsContent_List2) == len(objectDict) and (objectDict):
            for each_news, ob in zip(newsContent_List2, objectDict):
                number = number + 1
                # 识别属性
                # attr = findAttr(each_news,attrList)
                # 得出这条新闻的情感极性
                seg_list = jieba.cut(each_news)
                words = []
                for each2 in seg_list:
                    words.append(each2)
                # print('jieba:',words)
                vec_array = word2vec_W(word_vec, words, sentimentWordsList)
                # pred = clf.predict(vec_array)
                polarity = clf.predict(vec_array)  #预测极性
                print('type',type(polarity))
                # polarity = 1
                polarity = int(polarity)
                print('polarity', polarity)
                # if polarity !=0:
                per = getPercentage(each_news)
                perTerminology = terminologyWordsWeight(per, each_news, highImpactList, middleImpactList, lowImpactList)
                perTerminologyDegree = degreeWordsWeight(perTerminology, each_news, degWordH, degWordM, degWordL)
                level = getLevel(perTerminologyDegree)
                intensity = polarity * level
                print('intensity', intensity)
                objectIntensityDict[ob[0]] = int(intensity)
    if number == 0:  #如果新闻中没有评价对象，另写入一个字典{'empty'：强度值}
        seg_list = jieba.cut(newsContent)
        words = []
        for each2 in seg_list:
            words.append(each2)
        # print('jieba:',words)
        vec_array = word2vec_W(word_vec, words, sentimentWordsList)
        # pred = clf.predict(vec_array)
        polarity = clf.predict(vec_array)  # 预测极性
        print('type', type(polarity))
        # polarity = 1
        polarity = int(polarity)
        # print('polarity', polarity)
        print('polarity', polarity)
        per = getPercentage(newsContent)
        perTerminology = terminologyWordsWeight(per, newsContent, highImpactList, middleImpactList, lowImpactList)
        perTerminologyDegree = degreeWordsWeight(perTerminology, newsContent, degWordH, degWordM, degWordL)
        level = getLevel(perTerminologyDegree)
        intensity = polarity * level
        print('intensity', intensity)
        objectIntensityDict['empty'] = int(intensity)   #没有评价对象的情况

    #计算这条新闻综合强度值
    totalIntensity = 0
    if objectIntensityDict:
        for every in objectIntensityDict:
            totalIntensity = totalIntensity + objectIntensityDict[every]
        totalIntensity = totalIntensity / len(objectIntensityDict)

    objectIntensityDict = str(objectIntensityDict).replace("'", '"')    #解决数据库引号冲突
    return objectIntensityDict, totalIntensity

def updateRecord(idValue,objectIntensityDict, totalIntensity):
    global  db, cursor
    print('dict',str(objectIntensityDict))
    try:
        sql2 = "update raw_news set sastatus=1, satuples='%s', savalue='%d'  where id='%d'"%(str(objectIntensityDict),totalIntensity,idValue)
        print(sql2)
        cursor.execute(sql2)
        db.commit()
    except Exception as e:
        if not cursor:
            try:
                # 重新建立数据库连接
                db, cursor = connAgain()
                sql2 = "update raw_news set sastatus=0, satuples='str2', savalue=2  where id='%d'"%(idValue)
                cursor.execute(sql2)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
        else:
            print(e)
            db.rollback()


def connAgain():
    # 重新建立数据库连接
    db = pymysql.connect(host='118.25.147.13', user='root', port=3306, password='root@2019', db='predict_rmb')
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    return db,cursor

if __name__ == "__main__":
    #设置强度等级
    w1 = 1
    w2 = 2
    w3 = 3
    w4 = 4
    w5 = 5
    #设置划分范围
    value_1 = 0.001
    value_2 = 0.008
    value_3 = 0.015
    value_4 = 0.022
    #设置一个基值，如果新闻中没有百分数，给定一个默认百分数值value_0
    value_0 = value_1 #这里设置默认值为0.001，在getPercentage()函数中使用
    #设置术语词权重
    HEW = 2
    MEW = 1.5
    LEW = 1.3
    #设置程度词权重
    HDW = 1.5
    MDW = 1.3
    LDW = 0.7

    # 自定义分词词典
    filename = '../dictionary/splitWordsDict/splitWordsDict.txt'
    jieba.load_userdict(filename)

    #读取停用词
    stopWord = readStopWords()

    #读取情感词
    sentimentWordsList = readSentimentWords()

    #读取程度词
    degWordH, degWordM, degWordL = readDegreeWords()

    #读取术语词
    highImpactList, middleImpactList, lowImpactList = terminologyWords()

    #读取评价对象
    threeObject_A = objectList_A()

    # 处理有斜线的评价对象，例如美元/欧元
    specialObject = readSpecialObject()

    # #读取属性, （没有加入属性）
    # attrList = readAttribute()

    # 读取模型
    clf, word_vec = fetchModel()

    while(1):
        #1从数据库读取新闻
        idValue, newsTime, newsContent = fetchNews()
        if (idValue != 0) and (newsTime!='') and (newsContent!=''):
            print('idValue, newsTime', idValue, newsTime)
            #2对新闻分句,得到分句列表
            sentenceList = splitNewsContent(newsContent)
            #3寻找评价对象以及对应的情感强度值； 4计算综合强度值
            objectIntensityDict, totalIntensity = getObjectIntensity(newsContent,sentenceList, threeObject_A, specialObject, sentimentWordsList, highImpactList, middleImpactList, lowImpactList,degWordH, degWordM, degWordL, stopWord)
            #5更新数据库
            updateRecord(idValue,objectIntensityDict, totalIntensity)
            time.sleep(5)
        else:
            print('idValue, newsTime', idValue, newsTime)
            time.sleep(60)   #设置等待时间，等待新的新闻到来，60s检测一次
            try:
                db.commit()
            except Exception as e:
                if not cursor:
                    try:
                        # 重新建立数据库连接
                        db, cursor = connAgain()
                        db.commit()
                    except Exception as e:
                        print(e)
                        db.commit()
                else:
                    print(e)
                    try:
                        db.commit()
                    except:
                        continue



