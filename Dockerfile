FROM python:3.11-alpine3.18
RUN apk add --no-cache \
        curl \
        gcc \
        libressl-dev \
        musl-dev \
        libffi-dev 
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "cat-weather-bot"]