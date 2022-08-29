import api.datalab


def place_crawler(request):
    region_list = api.datalab.find_regions()
    print(region_list.text)

    for region in region_list.json()['list']:
        print(region["sggNm"], region["sggCd"])
        pois_list = api.datalab.find_pois(region["sggCd"])
        print(pois_list.text)

        for poi in pois_list.json()['list']:
            poi["ITS_BRO_NM"]


place_crawler('')
