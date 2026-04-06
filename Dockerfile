FROM python:3.12-slim

WORKDIR /usr/src/app

COPY ./req.txt ../req.txt

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ../req.txt

COPY ./video_platform ./

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver ${DOCKER_DJANGO_URL}"]

ENV PYTHONPATH /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
