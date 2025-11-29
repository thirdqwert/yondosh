FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
# продакшн
CMD /bin/bash -c "python manage.py migrate && gunicorn myapp.wsgi:application --bind 0.0.0.0:10000"
# разработка
# CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000



