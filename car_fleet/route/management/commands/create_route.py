from datetime import datetime, timedelta
from json import load
from math import sqrt

from django.core.management.base import BaseCommand
from requests import request

from point.models import Point
from route.models import Route
from vehicle.models import Vehicle
from random import randint

from time import sleep

EARTH_СIRCUMFERENCE = 40000 * 1000

with open("settings.json", "r") as settings_file:
    api_key_openroute = load(settings_file)['api_key_openroute']


def get_random_datetime():
    year = randint(2021, 2023)
    month = randint(1, 12)
    day = randint(1, 28)
    hour = randint(0, 23)
    minute = randint(0, 59)
    second = randint(0, 59)

    random_date = datetime(year, month, day, hour, minute, second)

    return random_date


class Command(BaseCommand):
    help = "Generates route for given vehicle."

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int)
        parser.add_argument('--length', type=int)
        parser.add_argument('--max-speed', type=int)
        parser.add_argument('--max-acceleration', type=int)
        parser.add_argument('--between-points', type=int)
        parser.add_argument('--points-deviation', type=int)
        parser.add_argument('--timestamp', type=int)
        parser.add_argument('--count', type=int)

    def get_length_between_points(self, x1, y1, x2, y2):
        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        length_degrees = sqrt(delta_x ** 2 + delta_y ** 2)
        length_meters = length_degrees / 360 * EARTH_СIRCUMFERENCE

        return length_meters

    def get_timedelta(self, distance):
        acceleration = randint(0, self.max_acceleration)
        end_speed = sqrt(self.start_speed ** 2 + 2 * acceleration * distance)

        if (end_speed - self.max_speed) > 0.01:
            end_speed = self.max_speed
            seconds = distance / end_speed
            return timedelta(seconds=seconds)

        try:
            seconds = distance / self.start_speed
        except ZeroDivisionError:
            seconds = self.timestamp - 1
        return timedelta(seconds=seconds)

    def dot_points(self, points):
        vehicles = Vehicle.objects.all()
        vehicle = vehicles[randint(0, len(vehicles))]


        for p in points:
            Point.objects.create(time=datetime.now(),
                                vehicle=vehicle,
                                point=f'POINT({p[0] % 180} {p[1] % 90})').save()

            sleep(self.timestamp)


        start = get_random_datetime()
        end = start + timedelta(self.timestamp * len(points))
        route = Route.objects.create(vehicle = vehicle, start=start, end=end)
        route.save()

    def handle(self, *args, **options):
        self.length = options['length'] or 10000
        self.max_speed = options['max_speed'] or 20
        self.max_acceleration = options['max_acceleration'] or 5
        self.between_points = options['between_points'] or 25
        self.points_deviation = options['points_deviation']
        self.timestamp = options['timestamp'] or 0.00001
        self.count = options['count'] or 1

        i = 0

        while i < self.count:
            route = self.create_route()
            less_route = route[::len(route) // 50]
            self.dot_points(less_route)
            i += 1

    def create_route(self):
        while True:
            start_city = self.get_random_city_coord()
            end_city = self.get_random_city_coord()

            start_lat, start_lng = start_city['lat'], start_city['lng']
            end_lat, end_lng = end_city['lat'], end_city['lng']

            try:
                route = self.get_route(start_lng, start_lat, end_lng, end_lat)
                break
            except:
                continue

        return route

    def get_random_city_coord(self):
        with open("ru_cities.json", "r") as c:
            cities = load(c)
        r = randint(0, len(cities) - 1)
        return cities[r]

    def get_point_on_road(self, x, y, order, deviation):
        r = request(method="GET",
                    url=f"https://api.openrouteservice.org/geocode/reverse?api_key={api_key_openroute}&point.lon={x}&point.lat={y}&boundary.circle.radius={deviation}&size={order + 1}")
        point_on_road = r.json()['features'][order]['geometry']['coordinates']

        return point_on_road[0], point_on_road[1]

    def get_route(self, x1, y1, x2, y2):
        r = request(method="GET",
                    url=f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key_openroute}&start={x1},{y1}&end={x2},{y2}")
        points = r.json()['features'][0]['geometry']['coordinates']
        return points
