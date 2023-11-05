FROM python:3.11-alpine

WORKDIR /app
RUN apk update && apk add mysql mysql-dev mysql-client gcc mariadb-connector-c-dev musl-dev 
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["uat_app.py"]
