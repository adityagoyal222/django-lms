FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app

RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev build-essential

# Install Node.js
# RUN apt-get update && apt-get install -y curl
# RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
# RUN apt-get install -y nodejs

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt



COPY . /app

#RUN chmod +x /app/tail.sh
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