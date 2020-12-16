FROM python:3.9-alpine
ENV PYTHONBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apk del build-deps
ADD monthly_book/ /app/