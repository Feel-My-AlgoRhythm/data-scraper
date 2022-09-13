import time
from tqdm import tqdm
from typing import List
from util.database import Database
from src.poi_review import POIReviewParser

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
