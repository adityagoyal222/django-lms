FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev build-essential

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/run.sh
# Path: docker-compose.yml
EXPOSE 8000

CMD ["./run.sh"]

# FROM python:3.9-alpine
# ENV PYTHONUNBUFFERED 1
# WORKDIR /app

# RUN apk update && \
#     apk add --no-cache mariadb-connector-c-dev build-base

# COPY requirements.txt /app/requirements.txt

# RUN pip install -r requirements.txt

# COPY . /app

# RUN chmod +x /app/run.sh

# EXPOSE 8000

# CMD ["./run.sh"]