# FROM python:3.9-slim
# ENV PYTHONUNBUFFERED 1
# WORKDIR /app

# RUN apt-get update
# RUN apt-get install -y default-libmysqlclient-dev build-essential

# COPY requirements.txt /app/requirements.txt

# RUN pip install -r requirements.txt

# COPY . /app

# RUN chmod +x /app/run.sh
# # Path: docker-compose.yml
# EXPOSE 8000

# CMD ["./run.sh"]

FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk update \
    && apk add --no-cache mariadb-dev build-base \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        mariadb-connector-c-dev \
        pkgconfig

# Set environment variables
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient -lpthread -lz -lm -ldl"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN chmod +x /app/run.sh

EXPOSE 8000

CMD ["./run.sh"]



