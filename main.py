import api.datalab
import api.naverplace


# TODO API 예외처리 추가
def place_crawler(request):
    region_list = api.datalab.find_regions()
    print(len(region_list.json()['list']), region_list.text)

    for region in region_list.json()['list']:
        print(region["sggNm"], region["sggCd"])
        pois_list = api.datalab.find_pois(region["sggCd"])
        print(len(pois_list.json()['list']), pois_list.text)

        for poi in pois_list.json()['list']:
            naver_place = api.naverplace.find_detail(poi["ITS_BRO_NM"])
            print("@@@@@@@@", naver_place.text)
            print(naver_place.json()['result']['place']['list'][0])
            naver_review = api.naverplace.find_review(naver_place.json()['result']['place']['list'][0]['id'])
            print("@@@@@@@@", naver_review.text)
            print(naver_review.json()[0]['data']['visitorReviewStats'])

            # TODO Save Database


place_crawler('')
