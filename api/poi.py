import requests
import time
import math
import json
from tqdm import tqdm
from typing import List
from util.database import Database

class POIParser:
    def __init__(self):
        self.database = Database()
        self.api_prefix = "https://pcmap-api.place.naver.com/graphql"
        self.api_headers = {"Content-Type": "application/json"}
        self.poi_count = self._load_poi_count()

    def __del__(self):
        self.database.cursor.close()

    def __len__(self):
        return self.poi_count

    def load_reviews(self) -> int:
        r"""
        POI 리뷰 데이터를 스크랩하여 DB에 저장

        Returns:
            :obj:`int`: 스크랩한 리뷰의 수
        """

        poi_list = self._load_poi_list()
        for poi_id in tqdm(poi_list, desc="poi"):
            review_parser = POIReviewParser(poi_id)
            review_data = review_parser.data
            
            # TODO: POI 리뷰 데이터 DB 저장
            #print(review_data)

            time.sleep(1)

    def _load_poi_count(self) -> int:
        r"""
        유효한 전체 POI의 개수를 반환
        
        Returns:
            :obj:`int`: 유효 POI의 개수
        """

        query = f"""
            SELECT COUNT(*) AS CNT
            FROM place
            WHERE valid = 1
        """
        self.database.cursor.execute(query)
        return self.database.cursor.fetchone()['CNT']

    def _load_poi_list(self) -> List[int]:
        r"""
        리뷰 수집 대상 POI의 네이버 지도 ID 목록 반환
        
        Returns:
            :obj:`List[int]`: 네이버 지도 ID 목록
        """

        query = f"""
            SELECT b.naver_id
            FROM
                place a,
                place_detail b
            WHERE
                a.detail_id = b.place_detail_id
                AND a.valid = 1
            ORDER BY b.naver_id ASC
        """
        self.database.cursor.execute(query)
        poi_list = [x['naver_id'] for x in self.database.cursor.fetchall()]
        return poi_list
    
class POIReviewParser:
    def __init__(self, poi_id):
        self.poi_id = poi_id

        self.api_prefix = "https://pcmap-api.place.naver.com/graphql"
        self.api_headers = {"Content-Type": "application/json"}
        self.review_stats = self._load_review_stats()
        self.review_count = self.review_stats['count']
        self.page_size = 50
        self.review_data = self._load_review_data()
    
    def __len__(self):
        return len(self.review_data)

    @property
    def data(self):
        return self.review_data

    def _load_review_stats(self):
        r"""
        POI 리뷰의 통계 데이터 로드

        Returns:
            :obj:`List[Dict]`: POI 리뷰 통계
        """

        query = [{
            "operationName": "getVisitorReviewStats",
            "variables": {
                "businessType": "place",
                "id": self.poi_id,
            },
            "query": "query getVisitorReviewStats($id: String, $itemId: String, $businessType: String = \"place\") {\n  visitorReviewStats(input: {businessId: $id, itemId: $itemId, businessType: $businessType}) {\n    id\n    name\n    apolloCacheId\n    review {\n      avgRating\n      totalCount\n      scores {\n        count\n        score\n        __typename\n      }\n      starDistribution {\n        count\n        score\n        __typename\n      }\n      imageReviewCount\n      authorCount\n      maxSingleReviewScoreCount\n      maxScoreWithMaxCount\n      __typename\n    }\n    analysis {\n      themes {\n        code\n        label\n        count\n        __typename\n      }\n      menus {\n        label\n        count\n        __typename\n      }\n      votedKeyword {\n        totalCount\n        reviewCount\n        userCount\n        details {\n          category\n          code\n          iconUrl\n          iconCode\n          displayName\n          count\n          previousRank\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    visitorReviewsTotal\n    ratingReviewsTotal\n    __typename\n  }\n}\n",
        }]

        try:
            response = requests.post(
                url=self.api_prefix,
                headers=self.api_headers,
                data=json.dumps(query),
            )
            response_data = response.json()
        except:
            raise Exception(response, f"Error occurred while scraping review stats of POI {self.poi_id}.")

        # HTTP 응답 예외 처리
        response.raise_for_status()
        if len(response_data) == 0 or 'errors' in response_data[0]:
            raise Exception(response_data)
        
        # 데이터 예외 처리
        if response_data[0]['data']['visitorReviewStats'] is None:
            return {
                "count": 0,
            }

        return {
            "count": response_data[0]['data']['visitorReviewStats']['review']['totalCount'],
        }

    def _load_review_data(self):
        r"""
        POI 리뷰 데이터 로드

        전체 리뷰 페이지 스크랩

        Returns:
            :obj:`List[Dict]`: POI 리뷰 데이터
        """

        if self.review_count == 0:
            return []

        max_page = math.ceil(self.review_count / self.page_size)
        query = []

        # 페이지 별 질의문 생성
        for page in tqdm(range(1, max_page+1), desc="review", leave=False):
            query.append({
                "operationName": "getVisitorReviews",
                "variables": {
                    "input": {
                        "businessId": self.poi_id,
                        "item": "0",
                        "page": page,
                        "size": self.page_size,
                        "isPhotoUsed": False,
                        "includeContent": True,
                        "getUserStats": True,
                        "includeReceiptPhotos": True,
                    }
                },
                "query": "query getVisitorReviews($input: VisitorReviewsInput) {\n  visitorReviews(input: $input) {\n    items {\n      id\n      rating\n      author {\n        id\n        nickname\n        from\n        imageUrl\n        objectId\n        url\n        review {\n          totalCount\n          imageCount\n          avgRating\n          __typename\n        }\n        theme {\n          totalCount\n          __typename\n        }\n        __typename\n      }\n      body\n      thumbnail\n      media {\n        type\n        thumbnail\n        class\n        __typename\n      }\n      tags\n      status\n      visitCount\n      viewCount\n      visited\n      created\n      reply {\n        editUrl\n        body\n        editedBy\n        created\n        replyTitle\n        __typename\n      }\n      originType\n      item {\n        name\n        code\n        options\n        __typename\n      }\n      language\n      highlightOffsets\n      apolloCacheId\n      translatedText\n      businessName\n      showBookingItemName\n      showBookingItemOptions\n      bookingItemName\n      bookingItemOptions\n      votedKeywords {\n        code\n        iconUrl\n        iconCode\n        displayName\n        __typename\n      }\n      userIdno\n      isFollowing\n      followerCount\n      followRequested\n      loginIdno\n      receiptInfoUrl\n      __typename\n    }\n    starDistribution {\n      score\n      count\n      __typename\n    }\n    hideProductSelectBox\n    total\n    showRecommendationSort\n    itemReviewStats {\n      score\n      count\n      itemId\n      starDistribution {\n        score\n        count\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            })
        
        try:
            response = requests.post(
                url=self.api_prefix,
                headers=self.api_headers,
                data=json.dumps(query),
            )
            response_data = response.json()
        except:
            raise Exception(response, f"Error occurred while scraping reviews of POI {self.poi_id}.")

        # HTTP 응답 예외 처리
        response.raise_for_status()
        if len(response_data) == 0 or 'errors' in response_data[0]:
            raise Exception(response_data)

        # 전체 페이지 데이터 병합
        review_data = [
            self._transform_review(x['data']['visitorReviews']['items'])
            for x in response_data
        ]
        return review_data
    
    def _transform_review(self, review_raw_data):
        r"""
        POI 리뷰의 RAW 데이터를 DB 필드에 맞게 변환

        Arguments:
            review_raw_data(:obj:`Dict`): POI 리뷰 RAW 데이터

        Returns:
            :obj:`Dict`: 변환된 POI 리뷰 데이터
        """

        # TODO: POI 리뷰 데이터 변환
        return review_raw_data
