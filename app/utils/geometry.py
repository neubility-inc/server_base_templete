from shapely import wkb
from geoalchemy2.elements import WKBElement
from typing import Union


def parse_point_to_xy(point: Union[WKBElement, str]):
    x, y = None, None

    if type(point) == str:
        # POINT({x}, {y}) 형태의 String 파싱 -> 그외는 에러
        point = point.replace("POINT", "").split(" ")

        # point 스트링 변환 후 리스트 -->  ['(37.4021', '127.1086)']
        x, y = float(point[0][1:]), float(point[1][:-1])

    else:
        wkb_data = wkb.loads(bytes(point))
        x, y = wkb_data.x, wkb_data.y

    return x, y
