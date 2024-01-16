FROM python:3.11-alpine3.18
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "cat-weather-bot"]