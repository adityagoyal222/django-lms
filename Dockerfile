FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev build-essential


COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt



COPY . /app

#RUN chmod +x /app/tail.sh
RUN chmod +x /app/run.sh

# Path: docker-compose.yml
EXPOSE 8000

CMD ["./run.sh"]
