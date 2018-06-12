
from math import radians, atan, tan, sin, cos, acos
#计算距离和相似度
#radians 角度转弧度
ra = 6378.140  # 赤道半径 (km)
rb = 6356.755  # 极半径 (km)
flatten = (ra - rb) / ra  # 地球扁率
def calcDistance(lon_a, lat_a, lon_b, lat_b):
    rad_lat_A = radians(lat_a)
    rad_lng_A = radians(lon_a)
    rad_lat_B = radians(lat_b)
    rad_lng_B = radians(lon_b)
    pA = atan(rb / ra * tan(rad_lat_A))
    pB = atan(rb / ra * tan(rad_lat_B))
    xx = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
    c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
    c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (xx + dr)
    return distance

from fuzzywuzzy import process
import pandas as pd


def calcRelativity(csv_file, keyWord, data):
    csv_file_tmp = csv_file.fillna("").astype(str)
    data = [x[1] for x in process.extractWithoutOrder(keyWord, data)]
    data = pd.DataFrame({
        'Relativity': data
        }
    )
    return data

def calcReverseDistance(lon_a, lat_a, lon_b, lat_b):
    return -calcDistance(lon_a, lat_a, lon_b, lat_b)