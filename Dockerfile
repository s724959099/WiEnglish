FROM python:3.7
COPY ./web /app
WORKDIR /app
RUN pip install -r requirements.txt