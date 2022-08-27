import requests
import json

with open('secret.json') as JSON_FILE:
    SECRET_JSON = json.load(JSON_FILE)


def find_datalab_cities():
    return requests.request(
        "POST", SECRET_JSON['API_URL']['DATA_LAB']['FIND_GU'],
        headers={}, data={
            'sidoCd': SECRET_JSON['API_KEY']['DATA_LAB']['SggCd']
        }
    )


def find_datalab_pois(arrSggSidoCd):
    return requests.request(
        "POST", SECRET_JSON['API_URL']['DATA_LAB']['FIND_PLACE'],
        headers={}, data={
            'arrSggCd[]': SECRET_JSON['API_KEY']['DATA_LAB']['SggCd'],
            'arrSggSidoCd[]': arrSggSidoCd,
            'txtSGG_CD': '1',
            'txtSIDO_ARR': '1',
            'SGG_CD': '11215',
            'SIDO_ARR': '11215',
            'BASE_YM1': '202108',
            'BASE_YM2': '202207',
            'TMAP_CATE_MCLS_CD': '전체',
            'srchAreaDate': '1',
            'qid': 'BDT_03_04_003'
        }
    )


def find_naverplace_info():
    # TODO
    pass


def find_naver_place_review():
    # TODO
    pass


def save_database():
    # TODO
    pass


def place_crawler(request):
    # 1
    response = find_datalab_cities()
    if response.status_code != 200:
        print("[ERROR] find_datalab_cities")
        return
    print(response.txt)
    # print(response.json()['list'])

    # 2
    response = find_datalab_pois('11215')
    if response.status_code != 200:
        print("[ERROR] find_datalab_pois")
    print(response.text)


place_crawler('')
