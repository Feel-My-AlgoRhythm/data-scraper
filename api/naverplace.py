import requests
import json

FIND_PLACE_URL = "https://map.naver.com/v5/api/search"
FIND_REVIEW_URL = "https://api.place.naver.com/place/graphql"


def find_detail(place_name):
    return requests.request(
        "GET", FIND_PLACE_URL,
        headers={}, params={
            "caller": "pcweb",
            "query": place_name,
            "type": "all",
            # "searchCoord": "127.07254197903751;37.54989869999944",
            "page": "1",
            "displayCount": "1",
            "isPlaceRecommendationReplace": "true",
            "lang": "ko"
        })


def find_review(place_id):
    return requests.request(
        "POST", FIND_REVIEW_URL,
        headers={'Content-Type': 'application/json'},
        data=json.dumps([
            {
                "operationName": "getVisitorReviewStats",
                "query": "query getVisitorReviewStats($id: String, $itemId: String, $businessType: String = \"place\") {\n  visitorReviewStats(input: {businessId: $id, itemId: $itemId, businessType: $businessType}) {\n    id\n    name\n    apolloCacheId\n    review {\n      avgRating\n      totalCount\n      scores {\n        count\n        score\n        __typename\n      }\n      starDistribution {\n        count\n        score\n        __typename\n      }\n      imageReviewCount\n      authorCount\n      maxSingleReviewScoreCount\n      maxScoreWithMaxCount\n      __typename\n    }\n    analysis {\n      themes {\n        code\n        label\n        count\n        __typename\n      }\n      menus {\n        label\n        count\n        __typename\n      }\n      votedKeyword {\n        totalCount\n        reviewCount\n        userCount\n        details {\n          category\n          code\n          iconUrl\n          iconCode\n          displayName\n          count\n          previousRank\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    visitorReviewsTotal\n    ratingReviewsTotal\n    __typename\n  }\n}\n",
                "variables": {
                    "businessType": "place",
                    "id": place_id
                }
            }
        ]))
