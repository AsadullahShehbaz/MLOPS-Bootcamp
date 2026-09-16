# syntax=docker/dockerfile:1
FROM python:3.14-slim

COPY . /app

WORKDIR /app 

# install app dependencies
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python","app.py"]