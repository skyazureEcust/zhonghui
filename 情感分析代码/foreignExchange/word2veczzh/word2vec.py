import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import jieba
import numpy as np

def wordtovec():
    # print(word_vec[newsSegmentationList[1][2::]])
    # for segment in newsSegmentationList:
    model = gensim.models.KeyedVectors.load_word2vec_format('./news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    # seg_list = jieba.cut("新浪援引报道称，中国央行计划向中债信用增进公司提供100亿元人民币，为民企发债提供增信支持。")
    seg_list = jieba.cut("意大利两年期国债收益率日内下跌6个基点至1.399%，5年期下跌4个基点至2.75%，逆转稍早涨势。意大利/德国10年期国债收益率差收窄10个基点，至303.7个基点。")
    print(seg_list)

    # # 读取停用词
    # stopWord = readstopwords('../dictionary/stopwords.txt')
    # # seg_list = "/".join(seg_gen).split('/')
    # # 去停用词，生成去停用词之后的分词结果
    # new_seg_list = []
    # for w in seg_list:
    #     if w in stopWord:
    #         continue
    #     else:
    #         new_seg_list.append(w)
    # print(new_seg_list)
    # # for each in seg_list:
    # #     print(each)
    # return new_seg_list

    # vec_array = []
    vec_array = np.zeros(64, dtype=float)
    for segment in seg_list:
        print(segment)
        # vec_array = np.array()
	# for i in range(2,len(segment)):
        try:
            value = word_vec[segment]
            vec_array += value
            # vec = np.array(value, dtype=float)
		    # vec_array += vec
		    # print("value:", value, "vec:", vec)
        except Exception as e:
            print("error:", e)
            # vec_array = vec_array
	# print("vec_array:", vec_array, "typeof_vecarray", type(vec_array))
	# <class 'numpy.ndarray'>
    seg = vec_array.tolist()
    print('seg',seg)
    # print(len(seg))   # 66 = 2(index time ) + 64个词向量

wordtovec()