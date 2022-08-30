import requests
from datetime import datetime, timedelta

FIND_POIS_URL = "https://datalab.visitkorea.or.kr/visualize/getTempleteData.do"
FIND_REGIONS_URL = "https://datalab.visitkorea.or.kr/portal/getSggCdList.do"
SIDO_CD = "11"  # 행정구역 최상위 코드 (서울시: 11)


def find_regions():
    return requests.request(
        "POST", FIND_REGIONS_URL,
        headers={}, data={
            'sidoCd': SIDO_CD,
        }
    )


def find_pois(sgg_cd):
    today = datetime.today()

    return requests.request(
        "POST", FIND_POIS_URL,
        headers={}, data={
            'SGG_CD': sgg_cd,
            'txtSGG_CD': '1',
            'txtSIDO_ARR': '1',
            'BASE_YM1': today - timedelta(days=365),
            'BASE_YM2': today,
            'TMAP_CATE_MCLS_CD': '전체',
            'srchAreaDate': '1',
            'qid': 'BDT_03_04_003'
        }
    )
