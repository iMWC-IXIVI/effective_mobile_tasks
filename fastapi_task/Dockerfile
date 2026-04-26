FROM python:3.12-slim


WORKDIR /usr/src/app

COPY ./req.txt ../req.txt

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r ../req.txt

COPY ./app ./

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host ${FASTAPI_HOST} --port ${FASTAPI_PORT} --reload"]


ENV PYTHONPATH /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
