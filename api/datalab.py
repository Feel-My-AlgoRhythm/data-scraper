import requests
import api


def find_regions():
    return requests.request(
        "POST", api.SECRET_JSON['API_URL']['DATA_LAB']['FIND_GU'],
        headers={}, data={
            'sidoCd': api.SECRET_JSON['API_KEY']['DATA_LAB']['SggCd'],
        }
    )


def find_pois(sgg_cd):
    return requests.request(
        "POST", api.SECRET_JSON['API_URL']['DATA_LAB']['FIND_PLACE'],
        headers={}, data={
            'arrSggCd[]': api.SECRET_JSON['API_KEY']['DATA_LAB']['SggCd'],
            'SGG_CD': sgg_cd,
            'txtSGG_CD': '1',
            'txtSIDO_ARR': '1',
            'BASE_YM1': '202108',
            'BASE_YM2': '202207',
            'TMAP_CATE_MCLS_CD': '전체',
            'srchAreaDate': '1',
            'qid': 'BDT_03_04_003'
        }
    )
