FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y gcc libpq-dev
WORKDIR /taxi_ais
COPY .. /taxi_ais
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput