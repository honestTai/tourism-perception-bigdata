import json
import requests
import pandas as pd
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from config import engine

url = 'https://m.ctrip.com/restapi/soa2/20047/listComments'

params = {
	"head": {
		"cid": "09031177418889054251",
		"ctok": "",
		"cver": "1.0",
		"lang": "01",
		"sid": "8888",
		"syscode": "09",
		"auth": "",
		"extension": []
	},
	"ucpBizId": 2,
	"scene": "PRODUCT_QUERY",
	"queryId": 15542990,
	"paging": {
		"pageSize": 1800,
		"pageNo": 1
	},
	"sortType": 3,
	"tagTerms": []
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
    params['queryId'] = int(poiId)
    params['paging']['pageNo'] = page
    response = requests.post(url, data=json.dumps(params))
    data = response.json()
    if data['ResponseStatus']['Ack'] == 'Success':
        resultList = data['comments']
        if resultList :
            all_data = []
            for item in resultList:
                comment_data = {
                    'commentId': item.get('commentId', None),
                    'content': item.get('content', None),
                    'ipLocatedName': item.get('ipAttributionName', None),
                    'publishTypeTag': item.get('commentTime', None),
                    'score': item.get('score', None),
                    'scores': str(item.get('subItems', None)),
                    'touristTypeDisplay': item['tourTypeInfo'].get('tourTypeName',
                                                                   None) if 'tourTypeInfo' in item else None,
                    'userNick': item['userInfo'].get('displayName', None) if 'userInfo' in item else None,
                    'userMember': item['userInfo'].get('curLevelName', None) if 'userInfo' in item else None,
                    'att_id': str(poiId)
                }

                all_data.append(comment_data)
            df = pd.DataFrame(all_data)

            try:
                df.to_sql(name='comment', con=engine, if_exists='append', index=False)
                print(df.size)
                # time.sleep(10)
            except IntegrityError as e:
                print(f'保存失败: {e}')
        else:
            print('评论为空')
    else:
        print('请求失败')

def main():
    threads = []
    attIds = get_attIds()

    with ThreadPoolExecutor() as executor:
        for attId in attIds:
            executor.submit(fetch_data, str(attId), 1)

def get_attIds():
    metadata = MetaData()
    atts = Table('buying', metadata, autoload=True, autoload_with=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(atts.c.pid)
    result = query.all()
    session.close()
    return [row[0] for row in result]

if __name__ == '__main__':
    main()
