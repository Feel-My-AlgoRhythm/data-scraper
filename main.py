import api.datalab
import api.naverplace


# TODO API 예외처리 추가
def place_crawler(request):
    print("[REQUEST] DATALAB:FIND_REGIONS >>>")
    region_list = api.datalab.find_regions()
    print("[RESPONSE] DATALAB:FIND_REGIONS >>>", region_list.status_code, region_list.text)

    for region in region_list.json()['list']:
        print("[REQUEST] DATALAB:FIND_POIS >>>", region["sggNm"], region["sggCd"])
        pois_list = api.datalab.find_pois(region["sggCd"])
        print("[RESPONSE] DATALAB:FIND_POIS >>>", pois_list.status_code, pois_list.text)

        for poi in pois_list.json()['list']:
            print("[REQUEST] NAVER_PLACE:FIND_DETAIL >>>", poi["ITS_BRO_NM"])
            naver_place = api.naverplace.find_detail(poi["ITS_BRO_NM"])
            print("[RESPONSE] NAVER_PLACE:FIND_DETAIL >>>", naver_place.status_code, naver_place.text)

            print("[REQUEST] NAVER_PLACE:FIND_REVIEW >>>", naver_place.json()['result']['place']['list'][0]['id'])
            naver_review = api.naverplace.find_review(naver_place.json()['result']['place']['list'][0]['id'])
            print("[RESPONSE] NAVER_PLACE:FIND_REVIEW >>>", naver_review.status_code, naver_review.text)

            print(naver_review.json()[0]['data']['visitorReviewStats'])

            # TODO Save Database


place_crawler('')
