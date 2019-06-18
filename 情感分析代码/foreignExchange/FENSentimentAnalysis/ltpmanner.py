#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys, os
#
# ROOTDIR = os.path.join(os.path.dirname(__file__), os.pardir)
# sys.path = [os.path.join(ROOTDIR, "lib")] + sys.path
#
# # Set your own model path;LTP模型文件路径
# # MODELDIR=os.path.join(ROOTDIR, "../pyltp-master/ltp_data_v3.4.0")
# # MODELDIR=os.path.join(ROOTDIR, "F:\WorkSpace\PyCharm_WorkSpace\exchange\ltp_data_v3.4.0")
# MODELDIR=os.path.join(ROOTDIR, "../ltp_data_v3.4.0")

# from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
from pyltp import SentenceSplitter

#分句
def newssplitsentence(newsContent):
    # paragraph = '中国进出口银行与中国银行加强合作。中国进出口银行与中国银行加强合作！'
    # print(newsContent)
    sentence = []
    for sen in SentenceSplitter.split(newsContent):
        sentence.append(sen)
    return sentence
    # print(sentence)
    # print('-----------------------------------------------------')


# #分词
# def splitwords(sentence):
#     # segmentor = Segmentor() #初始化实例
#     # segmentor.load(os.path.join(MODELDIR, "cws.model"))  #加载模型
#     # words = segmentor.segment(sentence) #分词
#     # # print("\t".join(words))
#     # wordsList = []
#     # for each in words:  # 分词
#     #     wordsList.append(each)
#     # segmentor.release()  #释放模型
#     # return words,wordsList
#
#     segmentor = Segmentor()  # 初始化实例
#     cws_model_path = os.path.join(MODELDIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
#     segmentor.load_with_lexicon(cws_model_path, '../dictionary/splitworddict.txt')  # 加载模型，第二个参数是您的外部词典文件路径
#     words = segmentor.segment(sentence)
#     # print("\t".join(words))
#     wordsList = []
#     for each in words:  # 分词
#         wordsList.append(each)
#     segmentor.release()  #释放模型
#     return words,wordsList
#
# #词性标注
# def wordpostag(words):
#     postagger = Postagger() #初始化实例s
#     postagger.load(os.path.join(MODELDIR, "pos.model")) #加载模型
#     postags = postagger.postag(words)   #词性标注
#     # list-of-string parameter is support in 0.1.5
#     # postags = postagger.postag(["中国","进出口","银行","与","中国银行","加强","合作"])
#     # print("\t".join(postags))
#     posList = []
#     for each in postags:  # 词性标注
#         posList.append(each)
#     postagger.release()
#     return postags,posList
#
# #依存句法分析
# def syntaxparser(words, postags):
#     parser = Parser()  # 初始化实例
#     parser.load(os.path.join(MODELDIR, "parser.model"))   # 加载模型
#     arcs = parser.parse(words, postags)  # 句法分析
#     # print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
#     arcsDict = {}
#     for each in arcs:  # 句法分析
#         arcsDict[each.head] = each.relation
#     parser.release()
#     return arcs,arcsDict
#
# #命名实体识别
# def nameidentityrecognizer(words,postags):
#     recognizer = NamedEntityRecognizer()
#     recognizer.load(os.path.join(MODELDIR, "ner.model"))
#     netags = recognizer.recognize(words, postags) # 命名实体识别
#     # print("\t".join(netags))
#     nerList = []
#     for each in netags:  # 命名实体识别
#         nerList.append(each)
#     recognizer.release()
#     return netags,nerList
#
# #语义角色标注
# def  sementicrolelabeller(words, postags,arcs):
#     labeller = SementicRoleLabeller()
#     labeller.load(os.path.join(MODELDIR, "pisrl_win.model"))  #windows系统使用
#     # labeller.load(os.path.join(MODELDIR, "pisrl.model"))  #linux系统。。
#     roles = labeller.label(words, postags, arcs)  # 语义角色标注
#     # 打印结果
#     for role in roles:
#         print(role.index, "".join(
#                 ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
#
#     labeller.release()
#
# def stopwords(words):
#     #读取停用词
#     stopWord = []
#     for word in open('../dictionary/stopwords.txt', 'r', encoding='utf-8').readlines():
#         stopWord.append(word)
#     # seg_list = "/".join(seg_gen).split('/')
#     #去停用词，生成去停用词之后的分词结果
#     new_seg_list = []
#     for w in words:
#         if w in stopWord:
#             continue
#         else:
#             new_seg_list.append(w)
#     # print(new_seg_list)
#     return new_seg_list


# def prepare_raw_news():
#     #  #logger.info("In("In Prepare Raw News...")
#     raw_news_data =  = CommonUtil.read_exc_excel(RAW_NEWS_PATH)
#     raw_news_table = raw_news_ws_data.sheet_by__by_index(0)
#     raw_news_rows = raw_news_ws_table.nrows
#
#     for rowN in range(0, raw_news_rows):
#         news_item = list()
#         news_index = int(raw_news_ws_table.cell_val_value(rowN, 0))
#         news_time =  = CommonUtil.get_dat_datetime_from_cell(raw_news_ws_table.cell_val_value(rowN, 1))
#         news_content = raw_news_ws_table.cell_val_value(rowN, 2)
#         news_ws_item.append(new(news_index)
#         news_ws_item.append(new(news_time)
#         news_ws_item.append(new(news_content)
#         newsList.append(new(news_item)
#         # print(newsList)
#         #  #logger.info("Pr("Prepare Raw News...Done!")
