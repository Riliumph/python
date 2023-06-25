FROM python:3.11.4-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code
# volumeは実行時に張られるためコピーが必要
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/
