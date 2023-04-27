FROM --platform=linux/amd64 python:3.8

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

EXPOSE 8080

CMD uvicorn app:app --host 0.0.0.0 --port 8080 --reload