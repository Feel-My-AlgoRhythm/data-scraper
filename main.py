import api.datalab


# TODO API 예외처리 추가
def place_crawler(request):
    region_list = api.datalab.find_regions()
    print(len(region_list.json()['list']), region_list.text)

    for region in region_list.json()['list']:
        print(region["sggNm"], region["sggCd"])
        pois_list = api.datalab.find_pois(region["sggCd"])
        print(len(pois_list.json()['list']), pois_list.text)

        for poi in pois_list.json()['list']:
            poi["ITS_BRO_NM"]
            # TODO Naver Place
            # TODO Save Database


place_crawler('')
