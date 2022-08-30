class Place:

    def __init__(self, region_list, pois_list, naver_place, naver_review):
        # datalab regions
        self.ssg_cd
        self.ssg_nm

        # datalab pois
        self.bro_nm
        self.addr_road_nm  # ?
        self.area_nm  # ?
        self.kto_cate_mcls_nm
        self.kto_cate_slcs_nm

        # naver place detail
        self.type
        self.id

        # naver place review
        self.avg_rating
        self.total_count

    def to_insert_query(self):
        pass


# https://velog.io/@jahoy/Python으로-클린-아키텍처-적용하기2
# https://towardsdev.com/ingesting-data-from-google-cloud-storage-into-python-5ba0d6f3e866