# 获取携程网上所有有关都江堰景区的数据信息
# 导入requests和BeautifulSoup模块
import time
from sqlite3 import IntegrityError

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import engine
import threading


def get_attraction_info(cargetId):
    # 定义url的地址
    url = "https://you.ctrip.com/sight/dujiangyan911/" + cargetId
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'cookie':'CHANGE_ME_BEFORE_RUNNING'
    }
    # 发送请求，获取响应
    response = requests.get(url=url, headers=headers)
    # 定义需要存入db的内容
    data = {
        # 唯一的id
        'cargetId': '',
        # 景区的名字
        'name': '',
        # 景区的评分
        'commentScoreNum': '',
        # 景区的类型
        'titleTips': '',
        # 热度
        'heatView': '',
        # 地址
        'address': '',
        # 开放时间
        'baseInfoItem': '',
        # 介绍
        'descInfo': '',
        # image
        'img': '',
        # link
        'url': '',
        # 优惠政策
        'preferential': '',
        # 服务设施
        'service': '',
        # 景区关键词
        'hotTags': ''
    }
    # 判断响应状态码是否为200
    if response.status_code == 200:
        # 解析HTML内容，创建BeautifulSoup对象
        soup = BeautifulSoup(response.text, "html.parser")
        data['cargetId'] = cargetId
        name = soup.find("div", class_="titleView").find("div",class_="title").find('h1').text
        data['name'] = name
        data['heatView'] = soup.find("div", class_="heatScoreText").text
        title_tips_div = soup.find("div", class_="titleTips")
        if title_tips_div:
            title_tips_span = title_tips_div.find("span")
            data['titleTips'] = title_tips_span.text if title_tips_span else None
        else:
            data['titleTips'] = None
        data['commentScoreNum'] = soup.find("div", class_="commentScore").find("p",class_="commentScoreNum").text
        data['address'] = soup.find("div", class_="baseInfoItem").find("p", class_="baseInfoText").text
        data['baseInfoItem'] = soup.find("p", class_="baseInfoText cursor openTimeText").text
        data['descInfo'] = soup.find("div", class_="LimitHeightText").text
        img_element = soup.find("div", class_="LimitHeightText").find('img')
        data['img'] = img_element.attrs.get('src') if img_element else None
        data['url'] = url
        preferential = soup.find('div', class_='moduleTitle', text='优待政策')
        try:
            preferential = soup.find('div', class_='moduleTitle', text='优惠信息')
            preferential_str = ''
            for row in preferential.find_next('div', class_='moduleContent').find_all('div', class_='moduleContentRow'):
                preferential_str += row.text.strip() + ','
            data['preferential'] = preferential_str
        except AttributeError:
            data['preferential'] = ''
        try:
            service = soup.find('div', class_='moduleTitle', text='服务设施')
            service_str = ''
            for row in service.find_next('div', class_='moduleContent').find_all('div', class_='moduleContentRow'):
                service_str += row.text.strip() + ','
            data['service'] = service_str
        except AttributeError:
            data['service'] = ''
        data['hotTags'] = soup.find("div", class_="hotTags").text
        df = pd.DataFrame(data, index=[0])
        try:
            df.to_sql(name='djy_att', con=engine, if_exists='append', index=False)
        except IntegrityError:
            print("数据存在")
    else:
        # 响应状态码不为200，打印错误信息
        print("请求失败，错误码：", response.status_code)


def main():
    cargetId = ['62960.html', '4597.html', '1683224.html', '1700731.html', '62961.html']
    # cargetId = [ '1700731.html']
    threads = []
    for cargetId_item in cargetId:
        thread = threading.Thread(target=get_attraction_info, args=(str(cargetId_item),))
        thread.start()
        threads.append(thread)
        # 每隔10秒执行一次
        time.sleep(10)

    # 等待所有线程完成
    for thread in threads:
        thread.join()
if __name__ == '__main__':
    main()
