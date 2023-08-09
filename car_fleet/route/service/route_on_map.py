def get_points_for_url(points):
    point_params = []

    for i, p in enumerate(points):
        latitude = p.point.x
        longitude = p.point.y
        point_params.append(f"{latitude},{longitude}")

    return ','.join(point_params)
