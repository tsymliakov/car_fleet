from datetime import datetime, timedelta
from json import load
from math import sqrt

from django.core.management.base import BaseCommand
from requests import request

from point.models import Point
from vehicle.models import Vehicle
from random import randint

from time import sleep

EARTH_СIRCUMFERENCE = 40000 * 1000

with open("settings.json", "r") as settings_file:
    api_key_openroute = load(settings_file)['api_key_openroute']


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
        model_points = [Point(time=self.curr_time,
                              vehicle=self.vehicle,
                              point=f'POINT({points[0][0] % 180} {points[0][1] % 90})')]

        for i in range(len(points) - 1)[1:]:
            x1 = points[i - 1][0]
            y1 = points[i - 1][1]

            x2 = points[i][0]
            y2 = points[i][1]

            distance = self.get_length_between_points(x1, y1, x2, y2)
            tdelta = self.get_timedelta(distance)

            self.curr_time += tdelta

            if i % 10 == 0:
                model_points.append(Point(time=self.curr_time,
                                          vehicle=self.vehicle,
                                          point=f'POINT({points[i][0] % 180} {points[i][1] % 90})'))

        Point.objects.bulk_create(model_points)

    def handle(self, *args, **options):
        self.vehicle = Vehicle.objects.get(id=469)  # Vehicle.objects.get(id=options['id'])
        self.length = options['length'] or 10000
        self.max_speed = options['max_speed'] or 20
        self.max_acceleration = options['max_acceleration'] or 5
        self.between_points = options['between_points'] or 25
        self.points_deviation = options['points_deviation']
        self.timestamp = options['timestamp'] or 1

        x, y = 37.4, 55.5  # Moscow GPS coordinates

        curr_point = self.get_point_on_road(x, y, randint(0, 5))

        self.current_length = 0
        self.start_speed = 0
        self.curr_time = datetime.now()

        while self.current_length < self.length:
            sleep(self.timestamp)

            next_point = self.get_point_on_road(x, y, randint(0, 10))

            points = self.get_route(*curr_point, *next_point)

            self.dot_points(points)

    def get_point_on_road(self, x, y, order):
        r = request(method="GET",
                    url=f"https://api.openrouteservice.org/geocode/reverse?api_key={api_key_openroute}&point.lon={x}&point.lat={y}&boundary.circle.radius={self.between_points * 10}&size=51")
        point_on_road = r.json()['features'][order]['geometry']['coordinates']

        return point_on_road[0], point_on_road[1]

    def get_route(self, x1, y1, x2, y2):
        r = request(method="GET",
                    url=f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key_openroute}&start={x1},{y1}&end={x2},{y2}")
        points = r.json()['features'][0]['geometry']['coordinates']
        return points
