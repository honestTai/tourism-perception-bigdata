import ast
import collections
import json
import os
import time

import jieba
import pandas as pd
from datetime import timedelta


from snownlp import SnowNLP
from collections import defaultdict
from database.config import engine
from scrapy.util import get_current_week, replace_unit, move_stopwords, get_stopwords_list
from analysis.myOperator import WCDataFromDataFrame, PieDataFromDataFrame, sentimentScoreFromDataFrame, \
    WCDataFromDataFrameBuying, MapPieDataFromDataFrame, MapWCDataFromDataFrame, MapPieScoreDataFromDataFrame, \
    MapPieIpDataFromDataFrame, MapPieUserDataFromDataFrame


def hot_buying():
    """
    商家路线热度排名分析
    :return:
    """
    sql = 'select * from buying where score is not null order by score desc'
    df = pd.read_sql(sql=sql, con=engine)
    data = df.to_dict(orient='records')
    return data


def buying_word_cloud():
    """
    商家路线图谱
    :return:
    """
    sql = 'select * from buying where score is not null order by score desc'
    df = pd.read_sql(sql=sql, con=engine)
    data = WCDataFromDataFrameBuying(df)
    return data


def weekly_topic_category(mode='week', dt=None):
    """
    展示本周话题的分类环形图
    :return:
    """
    if mode == 'week':
        un_time = time.mktime((get_current_week(dt=dt) - timedelta(days=7)).timetuple())
        sql = 'select * from topic where create_at>%(limitTime)s'
        df = pd.read_sql(sql=sql, con=engine, params={'limitTime': un_time})
        data = df['category_str'].value_counts()
        d = []
        for name in data.index:
            d.append({'name': name, 'value': int(data[name])})
        data = d[1:]
    elif mode == 'month':
        un_time = time.mktime((get_current_week(dt=dt) - timedelta(days=30)).timetuple())
        sql = 'select * from topic where create_at>%(limitTime)s'
        df = pd.read_sql(sql=sql, con=engine, params={'limitTime': un_time})
        data = df['category_str'].value_counts()
        d = []
        for name in data.index:
            d.append({'name': name, 'value': int(data[name])})
        data = d[1:]
    else:
        return
    return data


def get_merchant_ranking_stats():
    """
    获取商家热度排名总数：
    1. 所有商家总数
    2. 所有得分为4分及以上商家总数，所有得分为3分及以下商家总数
    3. 3分商家占总数比例，4分商家占总数比例

    返回:
    dict: 商家热度排名统计信息
    """
    # 获取所有不为空的商家信息数据
    sql = 'SELECT * FROM buying WHERE score IS NOT NULL ORDER BY score DESC'
    df = pd.read_sql(sql=sql, con=engine)

    # 获取得分统计信息
    high_score_merchants, low_score_merchants = socrereCount(df)

    # 计算3分和4分商家占总数比例
    total_merchants = df.shape[0]
    rate_of_3_score = (low_score_merchants / total_merchants) * 100
    rate_of_4_score = (high_score_merchants / total_merchants) * 100

    # 构建结果字典
    data = {
        'total_merchants': total_merchants,
        'high_score_merchants': high_score_merchants,
        'low_score_merchants': low_score_merchants,
        'rate_of_3_score': f"{rate_of_3_score:.2f}%",  # 3分商家占总数比例
        'rate_of_4_score': f"{rate_of_4_score:.2f}%",  # 4分商家占总数比例
        'passive_total': high_score_merchants,
        'passive_rate': f"{rate_of_4_score:.2f}%"  # 4分商家占总数比例
    }

    return data

def socrereCount(df):
    """
    从数据框中获取得分统计信息

    参数:
    df (DataFrame): 商家数据框

    返回:
    tuple: 包含高得分商家数量和低得分商家数量的元组
    """
    # Convert 'score' column to numeric type
    df['score'] = pd.to_numeric(df['score'], errors='coerce')

    # Filter high and low score merchants
    high_score_merchants = df[df['score'] >= 4].shape[0]
    low_score_merchants = df[df['score'] <= 3].shape[0]

    return high_score_merchants, low_score_merchants


def PositiveOrPassive(dt):
    """
    正负舆情分析
    :return:
    """
    un_time = time.mktime((get_current_week(dt=dt) - timedelta(days=7)).timetuple())
    sql = 'select * from topic where create_at>%(limitTime)s'
    df = pd.read_sql(sql=sql, con=engine, params={'limitTime': un_time})
    # 去重空类型topic
    df.drop(df[df['category_str'] == ''].index, inplace=True)
    category = df['category_str'].value_counts().index
    category = list(category)[:10]
    positive_list, passive_list = [], []
    for cate in category:
        if cate == '':
            continue
        df1 = df[df['category_str'] == cate]
        positive, passive = sentimentScoreFromDataFrame(df1)
        positive_list.append(positive)
        passive_list.append(passive)
    return {'name': category, 'positive': positive_list, 'passive': passive_list}


def region():
    """
    客源分析
    :return:
    """

    sql = "select * from comment where ipLocatedName is not null and ipLocatedName != '' and ipLocatedName != '未知'"
    #
    df = pd.read_sql(sql=sql, con=engine)
    d = []
    province_data = []
    # 逐个遍历省份
    for province_name in df['ipLocatedName'].value_counts().index:
        # 添加市或省后的名称
        display_name = province_name + "市" if province_name in ['北京', '上海', '天津',
                                                                 '重庆'] else province_name + "省"

        # 舆情地图数据
        d.append({'name': display_name, 'value': df[df['ipLocatedName'] == province_name].shape[0]})
        temp = df[df['ipLocatedName'] == province_name]
        # category分类
        key_value1 = MapPieDataFromDataFrame(temp)
        # 词云图
        # 合并话题名和摘要
        key_value2 = MapWCDataFromDataFrame(temp)
        province_data.append({'name': display_name, 'pieCount': key_value1, 'wordCount': key_value2})
    return {'map': d, 'province': province_data}




def getCommentWord(df):
    text = df['content'].to_string()
    text_cut = jieba.cut(text, use_paddle=True)  # 分词
    text_cut = move_stopwords(text_cut, get_stopwords_list())
    # 统计词频获取前200个
    word_counts = collections.Counter(text_cut)
    word_counts = word_counts.most_common(200)
    data = []
    for k, v in word_counts:
        data.append({'name': k, 'value': v})
    return data


def getAllComments():
    cache_file = "LOCAL_WORKSPACE_PATH"

    if os.path.exists(cache_file):
        os.remove(cache_file)
    """
    获取所有评论内容
    :return:
    """
    df = pd.read_sql(sql='select * from comment',con=engine)
    if df.empty:
        return ''
    else:
      df.drop(df[df['content'] == ''].index, inplace=True)
      total=int(0)
      positive=int(0)
      neutral=int(0)
      passive=int(0)
      pa_data=[]
      po_data=[]
      neutralss=[]
      word=[]
      word2=[]
    #进行分组
      datas=df.to_dict("records")
      for data in datas:
          if data['content'] == ' ':
              continue
          score = SnowNLP(data['content']).sentiments
          if(score>0.6):
              po_data.append(data)
          if (score < 0.3):
              pa_data.append(data)
          if (0.3<score<0.6):
              neutralss.append(data)


      positive=len(po_data)
      passive=len(pa_data)
      neutral=len(neutralss)

    #词云图
      word=getCommentWord(pd.DataFrame(po_data))
      word2 = getCommentWord(pd.DataFrame(pa_data))

      result = {'total': positive + neutral + passive, 'positive': positive, 'neutral': neutral, 'passive': passive,
              'pa_top': pa_data, 'po_top': po_data,'word':word,'word2':word2}

      return result


def getPrice():
    # 获取所有的数据
    df = pd.read_sql(sql='SELECT * FROM buying WHERE score IS NOT NULL AND travel IS NOT NULL AND comment IS NOT NULL AND price IS NOT NULL', con=engine)

    #根据得分与出行数为判断，筛选出 feature，然后转为k-v的形式，k是feature v是得分与出行数的值
    #根据价格与得分，统计出价格与得分的趋势
    #根据价格与出行，统计出价格与出行的趋势

    # 自定义分组和筛选
    # 筛选出travel字段大于50的值
    travelData = df[df['travel'] > '50']
    travelData = travelData[travelData['title'].str.contains('都江堰|青城山', case=False, na=False)]
    text = ', '.join(travelData['feature'].astype(str))
    phrases = [phrase.strip() for phrase in text.split(',')]
    # 统计词频获取前200个
    word_counts = collections.Counter(phrases )
    word_counts = word_counts.most_common(200)
    #出行次数超过50次的，特点关键词词云图
    data = []
    for k, v in word_counts:
        data.append({'name': k, 'value': v})

    titleData = df[df['travel'] > '50']
    titleData = titleData[titleData['title'].str.contains('都江堰|青城山', case=False, na=False)]
    text = titleData['title'].to_string()
    text_cut = jieba.cut(text, use_paddle=True)  # 分词
    text_cut = move_stopwords(text_cut, get_stopwords_list())
    # 统计词频获取前200个
    word_counts = collections.Counter(text_cut)
    word_counts = word_counts.most_common(200)
    datas = []
    for k, v in word_counts:
        datas.append({'name': k, 'value': v})

    #价格与出行次数的趋势
    #获取所有的价格与对应的出行次数数组[{"price":100,"travel":100},{"price":100,"travel":100}]
    priceData = df[['price', 'travel', 'title']]
    filteredPriceData = priceData[priceData['title'].str.contains('都江堰|青城山', case=False, na=False)]
    # priceDataGrouped = priceData.groupby('price')['travel'].sum().reset_index()\
    priceDataList = filteredPriceData.to_dict(orient='records')

    #价格与评分的趋势
    scoreData = df[['price', 'score', 'title']]
    filteredScoreData = scoreData[scoreData['title'].str.contains('都江堰|青城山', case=False, na=False)]
    # priceDataGrouped = priceData.groupby('price')['travel'].sum().reset_index()\
    filteredScoreDataList = filteredScoreData.to_dict(orient='records')


    # 返回JSON数据
    result = {
        'words1':datas,
        'feature': data,
        'priceTravel':priceDataList,
        'socre':filteredScoreDataList
    }
    return result


#景区分析
def getAtt(param):
    # 判断 param 是否为空字典
    if not param:
        # 如果为空字典，直接返回空的 DataFrame 或者做其他处理
        return []

    # 获取 attId 的值
    att_id = param.get('attId')

    # 判断 att_id 是否存在
    if att_id is not None and att_id.strip():
        # 构建 SQL 查询语句
        sql_query = f"SELECT * FROM comment WHERE att_id = {att_id}"

        # 使用 pandas 的 read_sql_query 方法执行查询
        df = pd.read_sql_query(sql_query, con=engine)

        #出行分类进行分组，首先排除空值
        typeData = df[df['touristTypeDisplay'].notnull()]
        type_data = MapPieDataFromDataFrame(typeData)
        scoreData = df[df['score'].notnull()]
        score_data = MapPieScoreDataFromDataFrame(scoreData)
        ipData = df[df['ipLocatedName'].notnull()]
        ip_data = MapPieIpDataFromDataFrame(ipData)
        userData = df[df['ipLocatedName'].notnull()]
        user_data = MapPieUserDataFromDataFrame(userData)


        #趋势图：得分趋势散点；词云图：评论的词云图；具体得分占比柱状图
        commentData = df[df['content'].notnull()]
        text = commentData['content'].to_string()
        text_cut = jieba.cut(text, use_paddle=True)  # 分词
        text_cut = move_stopwords(text_cut, get_stopwords_list())
        # 统计词频获取前200个
        word_counts = collections.Counter(text_cut)
        word_counts = word_counts.most_common(200)
        datas = []
        for k, v in word_counts:
            datas.append({'name': k, 'value': v})

        # 使用 ast.literal_eval 解析字符串表示的字典
        df['scores'] = df['scores'].apply(ast.literal_eval)

        # 处理 socresData
        socresData = df['scores'].apply(
            lambda scores: [{'title': item['name'], 'score': item['score']} for item in scores]
        )

        # 将结果展开为一个平面的列表
        scoresData = [item for sublist in socresData for item in sublist]

        # 合并得分相同的数据
        merged_data = defaultdict(list)
        for item in scoresData:
            merged_data[item['score']].append(item['title'])

        # 将结果转为字典
        merged_data_dict = dict(merged_data)
        result = {
            'type_data': type_data,
            'score_data': score_data,
            'ip_data': ip_data,
            'user_data': user_data,
            'words':datas,
            'scoresData':merged_data_dict
        }
        return result

    # 如果 att_id 不存在，也可以做其他处理，例如返回空的 DataFrame
    return []


def attGetAll():
    df = pd.read_sql(sql='SELECT * FROM djy_att', con=engine)
    return df.to_dict(orient='records')