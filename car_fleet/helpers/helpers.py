import math


EARTH_RADIUS = 6372795


def get_distance_between_points(p1, p2):
    """
    Returns distance in meters between two points.
    For example (56.007598, 37.200619), (56.003873, 37.197282).
    """
    llat1 = p1[0]
    llong1 = p1[1]

    llat2 = p2[0]
    llong2 = p2[1]

    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    distance = ad * EARTH_RADIUS

    return distance


def get_distance(points):
    distance = 0
    try:
        curr_point = points[0]
    except:
        return distance

    for p in points:
        distance += get_distance_between_points(curr_point, p)

    return distance
