from geopy import distance


def get_distance_km(point1: tuple, point2: tuple) -> float:
    return distance.distance(point1, point2).km
