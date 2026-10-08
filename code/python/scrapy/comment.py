import json
import requests
import pandas as pd
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from config import engine

url = 'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList'

params = {
    "arg": {
        "channelType": 2,
        "collapseType": 0,
        "commentTagId": 0,
        "pageIndex": 1,
        "pageSize": 10,
        "sourceType": 1,
        "sortType": 1,
        "starType": 0
    },
    "head": {
        "cid": "09031177418889054251",
        "ctok": "",
        "cver": "1.0",
        "lang": "01",
        "sid": "8888",
        "syscode": "09",
        "auth": "",
        "xsid": "",
        "extension": []
    }
}

def fetch_data(poiId, page):
    """
    获取评论数据并保存到数据库

    参数:
    poiId(int): 景点ID
    page(int): 页码

    返回:
    无
    """
    params['arg']['poiId'] = int(poiId)
    params['arg']['pageIndex'] = page
    response = requests.post(url, data=json.dumps(params))
    data = response.json()
    if data['code'] == 200:
        resultList = data['result']['items']
        all_data = []
        for item in resultList:
            comment_data = {
                'commentId': item['commentId'],
                'content': item['content'],
                'ipLocatedName': item['ipLocatedName'],
                'publishTypeTag': item['publishTypeTag'],
                'score': item['score'],
                'scores': str(item['scores']),
                'touristTypeDisplay': item['touristTypeDisplay'],
                'userNick': item['userInfo']['userNick'],
                'userMember': item['userInfo']['userMember'],
                'att_id': str(poiId)
            }
            all_data.append(comment_data)
        df = pd.DataFrame(all_data)
        try:
            df.to_sql(name='comment', con=engine, if_exists='append', index=False)
            time.sleep(10)
        except IntegrityError:
            print('保存失败')
    else:
        print('请求失败')

def main():
    threads = []
    attIds = get_attIds()
    # attIds = ['76447']
    with ThreadPoolExecutor() as executor:
        for attId in attIds:
            for page in range(1, 3000):
                executor.submit(fetch_data, str(attId), page)
                # time.sleep(45)  # Adjust sleep time based on API limitations

def get_attIds():
    """
    获取所有景点ID列表

    参数:
    无

    返回:
    list: 景点ID列表
    """
    metadata = MetaData()
    atts = Table('djy_att', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(atts.c.poiId)
    result = query.all()
    session.close()
    return [row[0] for row in result]

if __name__ == '__main__':
    main()
