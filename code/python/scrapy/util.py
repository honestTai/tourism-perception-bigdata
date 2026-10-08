import json
import time
from datetime import datetime, timedelta, date

import pandas as pd

from scrapy import config as cfg
import re


def replace_unit(number):
    """
    单位替换
    :return:
    """
    if '万' in number:
        number = number.replace('万', '')
        number = float(number) * 10000
        return str(number)
    elif '亿' in number:
        number = number.replace('亿', '')
        number = float(number) * 100000000
        return str(number)


def get_current_week(dt=None):
    """
    获取当前周的时间
    :param dt:
    :return:
    """
    monday, sunday = date.today(), date.today()
    if dt != '' and dt:
        monday, sunday = dt, dt
    one_day = timedelta(days=1)
    while monday.weekday() != 0:
        monday -= one_day
    while sunday.weekday() != 6:
        sunday += one_day
    return sunday


# 去掉停用词
def move_stopwords(sentence_list, stopwords_list):
    # 去停用词
    out_list = []
    for word in sentence_list:
        if word not in stopwords_list:
            if not remove_digits(word):
                continue
            if word is '\n':
                continue
            if word is ' ':
                continue
            if word != '\t':
                out_list.append(word)
    return out_list


def remove_digits(input_str):
    punc = u'0123456789.'
    output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
    return output_str


# 停用词表创建
def get_stopwords_list():
    stopwords = [line.strip() for line in
                 open(cfg.static_path + '/' + 'baidu_stopwords.txt', encoding='UTF-8').readlines()]
    return stopwords


def filterBySymbol(sentence, symbol='#'):
    """
    :param sentence:
    :param symbol:
    :return:
    """
    topics = []
    topic = ''
    tag = False
    for i in sentence:
        if i == symbol:
            # 匹配#字符条件
            tag = not tag
            if topic != '':
                topic = '#' + topic + '#'
                topics.append(topic)
                topic = ''
            continue
        if tag:
            topic += i
    return ','.join(topics)


def getWord(sentence):
    """
    网页富文本解析文字
    :param sentence:
    :return:
    """
    word = ''
    tag = 0
    for i in sentence:
        if i == '<':
            tag = 1
            continue
        elif i == '>':
            tag = 0
            continue
        elif tag == 0:
            word += i
    return word


def trans_format(time_string, from_format, to_format='%Y.%m.%d %H:%M:%S'):
    """
    @note 时间格式转化
    时间格式转换
    :param time_string:
    :param from_format:
    :param to_format:
    :return:
    """
    time_struct = time.strptime(time_string, from_format)
    times = time.strftime(to_format, time_struct)
    return times


