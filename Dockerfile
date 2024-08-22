FROM python:3.12-alpine3.19
WORKDIR /app
COPY . .
RUN pip install --upgrade pip \
&& pip install --no-cache-dir .
ENTRYPOINT ["cat-weather-bot"]
