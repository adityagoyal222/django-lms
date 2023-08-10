FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

# Apply database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate


# Path: docker-compose.yml
EXPOSE 8000

CMD ["python", "manage.py", "runserver"]

