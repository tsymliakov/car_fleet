FROM python:3.10

RUN mkdir app

WORKDIR app

ADD . /app/

RUN apt-get update

RUN apt-get install -y binutils libproj-dev gdal-bin

RUN pip install -r requirements.txt

CMD python car_fleet/manage.py migrate

CMD python car_fleet/manage.py runserver 0.0.0.0:8000