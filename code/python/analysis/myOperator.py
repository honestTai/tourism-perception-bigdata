import jieba
import collections
from snownlp import SnowNLP
from scrapy.util import move_stopwords, get_stopwords_list


def WCDataFromDataFrame(df):
    """
    dataframe计算词云图的key,value对
    :param df:
    :return:
    """
    name_str = df['name'].to_string()
    summary_str = df['summary'].to_string()
    text = name_str + summary_str
    text_cut = jieba.cut(text, use_paddle=True)  # 分词
    text_cut = move_stopwords(text_cut, get_stopwords_list())
    # 统计词频获取前200个
    word_counts = collections.Counter(text_cut)
    word_counts = word_counts.most_common(200)
    data = []
    for k, v in word_counts:
        data.append({'name': k, 'value': v})
    return data

def MapWCDataFromDataFrame(df):
    """
    dataframe计算词云图的key,value对
    :param df:
    :return:
    """
    content = df['content'].to_string()
    text = content
    text_cut = jieba.cut(text, use_paddle=True)  # 分词
    text_cut = move_stopwords(text_cut, get_stopwords_list())
    # 统计词频获取前200个
    word_counts = collections.Counter(text_cut)
    word_counts = word_counts.most_common(200)
    data = []
    for k, v in word_counts:
        data.append({'name': k, 'value': v})
    return data
def WCDataFromDataFrameBuying(df):
    """
    dataframe计算词云图的key,value对
    :param df:
    :return:
    """
    name_str = df['title'].to_string()
    feature_str = df['feature'].to_string()
    desc_str = df['descInfo'].to_string()
    text = name_str + feature_str + desc_str
    text_cut = jieba.cut(text, use_paddle=True)  # 分词
    text_cut = move_stopwords(text_cut, get_stopwords_list())
    # 统计词频获取前200个
    word_counts = collections.Counter(text_cut)
    word_counts = word_counts.most_common(200)
    data = []
    for k, v in word_counts:
        data.append({'name': k, 'value': v})
    return data


def PieDataFromDataFrame(df):
    """
    计算Pie数据的键值对
    :param df:
    :return:
    """
    data = []
    for n in df['category_str'].value_counts().index:
        if n == '':
            continue
        data.append({'name': n, 'value': df[df['category_str'] == n].shape[0]})
    return data

def MapPieDataFromDataFrame(df):
    """
    计算Pie数据的键值对
    :param df:
    :return:
    """
    data = []
    for n in df['touristTypeDisplay'].value_counts().index:
        if n == '':
            continue
        data.append({'name': n, 'value': df[df['touristTypeDisplay'] == n].shape[0]})
    return data


def MapPieScoreDataFromDataFrame(df):
    """
    计算Pie数据的键值对
    :param df:
    :return:
    """
    data = []
    for n in df['score'].value_counts().index:
        if n == '':
            continue
        data.append({'name': n, 'value': df[df['score'] == n].shape[0]})
    return data
def MapPieIpDataFromDataFrame(df):
    """
    计算Pie数据的键值对
    :param df:
    :return:
    """
    data = []
    for n in df['ipLocatedName'].value_counts().index:
        if n == '':
            continue
        data.append({'name': n, 'value': df[df['ipLocatedName'] == n].shape[0]})
    return data

def MapPieUserDataFromDataFrame(df):
    """
    计算Pie数据的键值对
    :param df:
    :return:
    """
    data = []
    for n in df['userMember'].value_counts().index:
        if n == '':
            continue
        data.append({'name': n, 'value': df[df['userMember'] == n].shape[0]})
    return data

def sentimentScoreFromDataFrame(df):
    """
    计算正负面的舆情
    :param df:
    :return:
    """
    df1 = df
    df1['text'] = df1['name'] + df1['summary']
    df1['score'] = df1['text'].apply(lambda x: SnowNLP(x).sentiments)
    positive = df1[df1['score'] > 0.6]
    passive = df1[df1['score'] < 0.3]
    return positive.shape[0], passive.shape[0]
