FROM python:3.8.5-alpine

WORKDIR /app

RUN apk update
RUN apk add musl-dev mariadb-dev gcc
RUN pip install mysqlclient

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]