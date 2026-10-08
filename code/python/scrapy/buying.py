# https://vacations.ctrip.com/list/around/sc28.html?s=2&st=%E9%83%BD%E6%B1%9F%E5%A0%B0&startcity=28&sv=%E9%83%BD%E6%B1%9F%E5%A0%B0&filter=adlex40002871adlex40002745adlex40000674adlex40001715adlex40002822adlex40002824


# 获取携程网上所有有关都江堰景区的数据信息
# 导入requests和BeautifulSoup模块
import time
from sqlite3 import IntegrityError

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import engine
import threading
import json
import requests
import pandas as pd
from sqlalchemy.exc import IntegrityError
from concurrent.futures import ThreadPoolExecutor
import time

from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from config import engine

url = 'https://sec-m.ctrip.com/restapi/soa2/20684/productSearch?_fxpcqlniredt=09031177418889054251'

params = {
	"contentType": "json",
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
	"client": {
		"version": "857006",
		"channel": 116,
		"locale": "zh-CN",
		"currency": "CNY",
		"source": "NVacationMobile",
		"cid": "1704939035725.6565u2gFTHhQ",
		"location": {
			"lat": "",
			"lon": "",
			"cityId": 28,
			"cityType": 3,
			"locatedCityId": 0
		},
		"extras": {}
	},
	"marketingInfo": {
		"allianceId": 4899,
		"sid": 155997
	},
	"destination": {
		"poid": 0,
		"type": "",
		"keyword": "都江堰"
	},
	"filtered": {
		"tab": "512",
		"preItems": [],
		"items": [
			{
				"type": "PLAY_LINE_EX",
				"method": "OR",
				"items": [
					{
						"type": "PLAY_LINE_EX",
						"method": "FILTERED",
						"value": "40000674"
					},
					{
						"type": "PLAY_LINE_EX",
						"method": "FILTERED",
						"value": "40001715"
					},
					{
						"type": "PLAY_LINE_EX",
						"method": "FILTERED",
						"value": "40002745"
					},
					{
						"type": "PLAY_LINE_EX",
						"method": "FILTERED",
						"value": "40002822"
					},
					{
						"type": "PLAY_LINE_EX",
						"method": "FILTERED",
						"value": "40002824"
					},
					{
						"type": "PLAY_LINE_EX",
						"method": "FILTERED",
						"value": "40002871"
					}
				]
			}
		],
		"minPrice": 0,
		"maxPrice": 0,
		"beginDate": "",
		"endDate": "",
		"sort": 8,
		"pageIndex": 2,
		"pageSize": 100,
		"extras": {}
	},
	"searchOption": {
		"returnMode": "product",
		"filters": [],
		"needAdProduct": True,
		"needUpStream": False,
		"needRiskPolicyInfo": True
	},
	"imageOption": {
		"width": 200,
		"height": 313,
		"autoCrop": True
	},
	"productOption": {
		"needBasicInfo": True,
		"needPrice": True,
		"needVendor": True,
		"needComment": True,
		"needOrder": True,
		"needRanking": True,
		"tagOption": [
			"PRODUCT_TAG",
			"RECOMMEND_TAG",
			"FESTIVAL_TAG",
			"SCHEDULE_TAG",
			"PROMOTION_TAG",
			"BARGAIN_TAG",
			"FAVORITE_TAG"
		]
	},
	"productKeys": [],
	"requestSource": "tour",
	"debug": False,
	"extras": {
		"USE_NEW_LEVEL": "true",
		"USE_NEW_PRICE": "true",
		"needUserDiscountPrice": "true",
		"FILTERED_SCOPE": "custom",
		"USE_GP_FLOOR": "true",
		"HIDE_DEPARTURE_DATE": "true",
		"CURRENT-CHANNEL": "ALL",
		"CURRENT-PAGE": "ALL",
		"TAB_GROUP": "B",
		"NEED_ALL_FILTERS": "true",
		"NEED_PRE_SALE_FILTER": "true",
		"NEED_MIX_FILTER": "true"
	}
}


def fetch_data(page):
    try:
        params['filtered']['pageIndex'] = int(page)

        response = requests.post(url, data=json.dumps(params))
        response.raise_for_status()

        data = response.json()
        if data['ResponseStatus']['Ack'] == 'Success':
            resultList = data['products']
            all_data = []

            for item in resultList:
                statistics = item.get('statistics')

                # if statistics is None or not statistics:
                #     continue

                features = item['tagGroups'][0]['tags']
                feature_str = ','.join(feature['tagName'].strip() for feature in features)

                data = {
                    'pid': item.get('id', None),
                    'title': item['basicInfo'].get('mainName', None),
                    'descInfo': item['basicInfo'].get('name', None),
                    'score': statistics['commentInfo'].get('score', None) if statistics.get('commentInfo') else None,
                    'travel': statistics['orderInfo']['touristCounts'].get('TOTAL', None) if statistics.get(
                        'orderInfo') else None,
                    'comment': statistics['commentInfo'].get('count', None) if statistics.get('commentInfo') else None,
                    'retail': item['vendorInfo'].get('brandName', None),
                    'price': item['priceInfo'].get('originalPrice', None),
                    'img': item['basicInfo']['mediaInfo']['images'][0].get('url', None) if item['basicInfo'][
                        'mediaInfo'] else None,
                    'url': item['basicInfo']['detailUrl'].get('H5', None) + item.get('id', None) if item['basicInfo'][
                        'detailUrl'] else None,
                    'feature': feature_str
                }
                all_data.append(data)

            if all_data:
                df = pd.DataFrame(all_data)
                df.to_sql(name='buying', con=engine, if_exists='append', index=False)
                time.sleep(10)
                print('保存成功')
            else:
                print('未找到有效数据')
        else:
            print('请求失败:', data)
    except requests.exceptions.RequestException as e:
        print(f'请求错误: {e}')
    except IntegrityError:
        print('保存失败: 数据已存在')
    except Exception as e:
        print(f'发生未知错误: {e}')

def main():
    threads = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        for page in range(1, 18):
            thread = executor.submit(fetch_data, str(page))
            threads.append(thread)


    for thread in threads:
        thread.result()

if __name__ == '__main__':
    main()
