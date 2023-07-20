from datetime import datetime, timedelta
from math import cos, sin
from django.core.management.base import BaseCommand
from point.models import Point
from vehicle.models import Vehicle
from random import randint

from time import sleep


EARTH_CIRCUMFERENCE = 40000 * 1000


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

    def get_length_to_next_point(self, start_speed):
        acceleration =  randint(self.max_acceleration * (- 2), self.max_acceleration)
        end_speed = start_speed + acceleration * self.timestamp

        if (end_speed - self.max_speed) > 0.01:
            acceleration_time = abs(self.max_speed - start_speed) / acceleration
            inc_speed_segment_len = (start_speed + self.max_speed) / 2 * acceleration_time
            const_speed_segment_len = (self.timestamp - acceleration_time) * self.max_speed
            end_speed = self.max_speed
            segment_len = inc_speed_segment_len + const_speed_segment_len
            return (segment_len, end_speed)
        if end_speed < 0:
            acceleration_time = start_speed / acceleration
            inc_speed_segment_len = start_speed / 2 * acceleration_time
            end_speed = 0
            return (inc_speed_segment_len, end_speed)

        segment_len = start_speed * self.timestamp + 0.5 * acceleration * (self.timestamp ** 2)
        return (segment_len, end_speed)

    def dot_the_points(self, lengthstamps, start_point):
        x = start_point.point[0]
        y = start_point.point[1]
        time = start_point.time
        full_length = sum(lengthstamps)
        point = start_point

        for l in lengthstamps:
            angle = randint(0, 90)
            l_in_degrees = 360 * l / EARTH_CIRCUMFERENCE
            delta_x = l_in_degrees * sin(angle)
            delta_y = l_in_degrees * sin(90 - angle)
            try:
                time = time + timedelta(seconds=self.timestamp * (l / full_length))
            except ZeroDivisionError:
                 time = time + timedelta(seconds=self.timestamp)
            point = Point(time=time, vehicle=self.vehicle,  point=f'POINT({(x + delta_x) % 180} {(y + delta_y) % 90})')
            point.save()

        return point

    def handle(self, *args, **options):
        self.vehicle = Vehicle.objects.get(id=1) # Vehicle.objects.get(id=options['id'])
        self.length = options['length'] or 10000
        self.max_speed = options['max_speed'] or 20
        self.max_acceleration = options['max_acceleration'] or 5
        self.between_points = options['between_points'] or 10
        self.points_deviation = options['points_deviation']
        self.timestamp = options['timestamp'] or 1

        start_speed = 0
        start_point = Point(time=datetime.now(),
                            vehicle=self.vehicle,
                            point=f'POINT({randint(-180,180)} {randint(-90,90)})')

        current_length = 0

        while current_length < self.length:
            sleep(self.timestamp)
            length_to_next_point, start_speed = self.get_length_to_next_point(start_speed)
            lengthstamps = []

            if length_to_next_point <= self.between_points:
                lengthstamps.append(length_to_next_point)

            while length_to_next_point > self.between_points:
                lengthstamps.append(self.between_points)
                length_to_next_point -= self.between_points

            self.dot_the_points(lengthstamps, start_point)

            current_length += length_to_next_point
