import math
import pandas as pd

def haversine(lat1, lon1, lat2, lon2):
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Earth's radius (in km)
    R = 6371.0
    
    # Distance in km
    distance = R * c
    return distance

def find_haversine(lat1, lon1):
    df = pd.read_csv('./coordinate_list.csv')
    min_dis = 100000000
    final_lat , final_lon = lat1, lon1

    for i in df.iterrows():
        lat2, lon2 = float(i[1][0]), float(i[1][1])
        dis = haversine(lat1, lon1, lat2, lon2)
        if dis < min_dis:
            min_dis = dis
            final_lat, final_lon = lat2, lon2
    return final_lat, final_lon, dis