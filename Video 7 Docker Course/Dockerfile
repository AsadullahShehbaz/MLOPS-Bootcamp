FROM python:3.12-alpine
COPY . /code
WORKDIR /code 
ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask","run"]

