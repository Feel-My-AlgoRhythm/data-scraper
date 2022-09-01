import api.datalab
import api.naverplace
import glob
from google.cloud import bigquery
from google.oauth2 import service_account


# TODO API 예외처리 추가
def place_crawler(request):
    key_path = glob.glob("./config/*.json")[0]
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    query = """
            SELECT *
            FROM `feel-my-algorhythm.travel_rhythm.region`
            LIMIT 20
        """
    # INSERT INTO feel-my-algorhythm.travel_rhythm.region VALUES('강서구', '11500');
    query_job = client.query(query)  # Make an API request.

    print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        print(row)
        print(row['sggCd'])
        print(row['sggNm'])

    print("[REQUEST] DATALAB:FIND_REGIONS >>>")
    region_list = api.datalab.find_regions()
    print("[RESPONSE] DATALAB:FIND_REGIONS >>>", region_list.status_code, region_list.text)

    for region in region_list.json()['list']:
        print(region["sggNm"], region["sggCd"])

    # for region in region_list.json()['list']:
    #     print("[REQUEST] DATALAB:FIND_POIS >>>", region["sggNm"], region["sggCd"])
    #     pois_list = api.datalab.find_pois(region["sggCd"])
    #     print("[RESPONSE] DATALAB:FIND_POIS >>>", pois_list.status_code, pois_list.text)
    #
    #     for poi in pois_list.json()['list']:
    #         print("[REQUEST] NAVER_PLACE:FIND_DETAIL >>>", poi["ITS_BRO_NM"])
    #         naver_place = api.naverplace.find_detail(poi["ITS_BRO_NM"])
    #         print("[RESPONSE] NAVER_PLACE:FIND_DETAIL >>>", naver_place.status_code, naver_place.text)
    #
    #         print("[REQUEST] NAVER_PLACE:FIND_REVIEW >>>", naver_place.json()['result']['place']['list'][0]['id'])
    #         naver_review = api.naverplace.find_review(naver_place.json()['result']['place']['list'][0]['id'])
    #         print("[RESPONSE] NAVER_PLACE:FIND_REVIEW >>>", naver_review.status_code, naver_review.text)
    #
    #         print(naver_review.json()[0]['data']['visitorReviewStats'])
    #
    #         # TODO Save Database


place_crawler('')
